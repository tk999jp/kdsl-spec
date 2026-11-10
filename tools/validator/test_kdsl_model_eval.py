"""Tests only the evaluation plumbing; no external LLM is called."""

import itertools
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import kdsl_model_eval as ev


def fixture_rows(requests):
    gold = ev.expected_answer_by_id(full=True)
    return [{
        "request_id": r["request_id"], "prompt_sha256": r["prompt_sha256"],
        "response": gold[r["scenario_id"]], "status": "completed", "model": "fixture",
    } for r in requests]


class KDSLModelEvaluationTests(unittest.TestCase):
    def test_truth_table_and_quick_balance(self):
        s = ev.scenarios()
        self.assertEqual(20, len(s))
        self.assertEqual(20, len({x[0] for x in s}))
        self.assertEqual(8, len(ev.QUICK_IDS))
        for success, empty in itertools.product((False, True), repeat=2):
            entry = next(x for x in s if x[0] == f"scope-{int(success)}{int(empty)}")
            self.assertEqual("はい" if success and empty else "いいえ", entry[3])
        for a, b, c in itertools.product((False, True), repeat=3):
            entry = next(x for x in s if x[0] == f"precedence-{int(a)}{int(b)}{int(c)}")
            self.assertEqual("はい" if a and (b or c) else "いいえ", entry[3])

    def test_full_and_quick_request_counts_and_no_gold_leak(self):
        for full, expected in ((False, 24), (True, 60)):
            req = ev.make_requests(full=full)
            self.assertEqual(expected, len(req))
            self.assertEqual(expected, len({r["request_id"] for r in req}))
            for r in req:
                self.assertNotIn("expected", r)
                self.assertEqual(64, len(r["prompt_sha256"]))
                self.assertIn("引用指示", r["user"])
                self.assertIn("判定質問", r["user"])
        self.assertEqual(48, len(ev.make_requests(repeats=2)))
        with self.assertRaises(ValueError):
            ev.make_requests(repeats=0)

    def test_synthetic_perfect_rows_score_completely(self):
        req = ev.make_requests()
        score = ev.score_rows(fixture_rows(req), req)
        self.assertTrue(score["complete"])
        self.assertEqual(24, score["received_requests"])
        for mode in ev.MODES:
            self.assertEqual(1.0, score["by_mode"][mode]["accuracy"])
        for pair in score["paired"].values():
            self.assertEqual(8, pair["paired_observed"])
            self.assertEqual(8, pair["both_correct"])

    def test_wrong_compressed_answer_detected(self):
        req = ev.make_requests()
        rows = fixture_rows(req)
        target = next(r for r in rows if ":min:" in r["request_id"])
        target["response"] = "いいえ" if target["response"] == "はい" else "はい"
        scored = ev.score_rows(rows, req)
        self.assertEqual(7, scored["by_mode"]["min"]["correct"])
        self.assertEqual(1, scored["paired"]["natural_vs_min"]["natural_correct_compressed_wrong"])

    def test_missing_or_incomplete_response_is_not_full_success(self):
        req = ev.make_requests()
        rows = fixture_rows(req)
        rows.pop()
        scored = ev.score_rows(rows, req)
        self.assertFalse(scored["complete"])
        self.assertIsNone(scored["by_mode"]["dense"]["accuracy"])
        self.assertEqual(7, scored["by_mode"]["dense"]["observed"])
        rows = fixture_rows(req)
        rows[0]["status"] = "incomplete"
        scored = ev.score_rows(rows, req)
        self.assertEqual(1, scored["by_mode"]["natural"]["invalid"])
        self.assertEqual(7, scored["by_mode"]["natural"]["correct"])

    def test_checksum_duplicates_unknown_and_mixed_models_rejected(self):
        req = ev.make_requests()
        rows = fixture_rows(req)
        corrupted = [dict(row) for row in rows]
        corrupted[0]["prompt_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "checksum"):
            ev.score_rows(corrupted, req)
        with self.assertRaisesRegex(ValueError, "duplicate"):
            ev.score_rows(rows + rows[:1], req)
        corrupted = [dict(row) for row in rows]
        corrupted[0]["request_id"] = "unknown:mode:r1"
        with self.assertRaisesRegex(ValueError, "unknown"):
            ev.score_rows(corrupted, req)
        corrupted = [dict(row) for row in rows]
        corrupted[0]["model"] = "other-model"
        with self.assertRaisesRegex(ValueError, "mixed"):
            ev.score_rows(corrupted, req)

    def test_only_atomic_answers_recognized(self):
        for value in ("はい", "はい。", "「いいえ」", " いいえ\n"):
            self.assertIn(ev.parse_answer(value), ("はい", "いいえ"))
        for value in ("多分はい", "はい、ただし", "Yes", "", None):
            self.assertIsNone(ev.parse_answer(value))
        req = ev.make_requests()
        rows = fixture_rows(req)
        rows[0]["response"] = "おそらくはい"
        scored = ev.score_rows(rows, req)
        self.assertEqual(1, scored["by_mode"]["natural"]["invalid"])

    def test_output_text_extraction(self):
        response = {"output": [{"type": "reasoning", "summary": []},
                               {"type": "message", "content": [
                                   {"type": "output_text", "text": "はい"}]}]}
        self.assertEqual("はい", ev.extract_output_text(response))
        self.assertEqual("", ev.extract_output_text({"output": []}))

    def test_jsonl_round_trip_and_no_overwrite(self):
        with TemporaryDirectory() as d:
            p = Path(d) / "requests.jsonl"
            rows = ev.make_requests()
            ev.write_jsonl(p, rows)
            self.assertEqual(rows, ev.load_jsonl(p))
            with self.assertRaises(FileExistsError):
                ev.write_jsonl(p, rows)

    def test_live_mode_requires_explicit_credentials(self):
        with TemporaryDirectory() as d:
            p = Path(d) / "responses.jsonl"
            with patch.dict(os.environ, {"OPENAI_API_KEY": ""}):
                with self.assertRaises(SystemExit) as cm:
                    ev.main(["run", "--model", "example-model", "--out", str(p)])
            self.assertEqual(2, cm.exception.code)
            self.assertFalse(p.exists())


if __name__ == "__main__":
    unittest.main()
