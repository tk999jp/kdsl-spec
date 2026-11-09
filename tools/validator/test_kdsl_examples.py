"""Small deterministic regression for the reviewed KDSL examples.

Marker checks only; decision oracles live in test_kdsl_semantics.py. Neither test suite proves LLM equivalence.
"""

import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "examples" / "kanji" / "behavior_cases.json"


def compact_length(value: str) -> int:
    return len(re.sub(r"\s+", "", value))


class KDSLRebuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.samples = json.loads(DATA.read_text(encoding="utf-8"))

    def test_case_coverage(self):
        self.assertEqual(8, len(self.samples))
        self.assertEqual(8, len({c["id"] for c in self.samples}))

    def test_samples_compact_and_preserve_markers(self):
        for case in self.samples:
            for mode in ("min", "dense"):
                with self.subTest(case=case["id"], mode=mode):
                    result = case[mode]
                    self.assertLess(compact_length(result), compact_length(case["natural"]))
                    for marker in case["required"] + case["protected"]:
                        self.assertIn(marker, result)

    def test_branching_scope_not_collapsed(self):
        case = next(c for c in self.samples if c["id"] == "condition-scope")
        for mode in ("min", "dense"):
            value = case[mode]
            self.assertIn("src dir空かつ移動成功→src dir削除", value)
            self.assertIn("src dir非空または移動失敗→保持", value)
            self.assertIn("条件確認→成立時のみ削除", value)

    def test_critical_scope_and_states(self):
        cases = {c["id"]: c for c in self.samples}
        checks = {
            "dev-bytes": ("丸め禁止", "KB・MB", "stage", "commit", "push"),
            "blog-meta": ("120字", "主要題5", "SEO title案5", "tag5-8"),
            "creative-seed": ("事実化禁止", "異方向3案"),
            "condition-scope": ("空かつ移動成功→", "非空または移動失敗→保持", "成立時のみ削除"),
            "literal-preservation": ("MoveItemAsync", "未実行→実行済扱禁止"),
            "condition-precedence": ("Aかつ(BまたはC)→実行", "A不成立→実行禁止"),
            "explicit-approval": ("commit=承認待", "未push差分破棄"),
            "runtime-separation": ("test成功", "未確認", "RT:v扱禁止"),
        }
        self.assertEqual(set(cases), set(checks))
        for case_id, spans in checks.items():
            for mode in ("min", "dense"):
                with self.subTest(case=case_id, mode=mode):
                    self.assertTrue(all(span in cases[case_id][mode] for span in spans))

    def test_technical_identifiers_are_unchanged(self):
        case = next(c for c in self.samples if c["id"] == "literal-preservation")
        for marker in case["protected"]:
            self.assertIn(marker, case["natural"])
            self.assertIn(marker, case["min"])
            self.assertIn(marker, case["dense"])

    def test_canonical_core_separate_from_agent(self):
        spec = (ROOT / "spec/core/kdsl-spec.md").read_text(encoding="utf-8")
        core = (ROOT / "spec/core/kdsl-core.md").read_text(encoding="utf-8")
        for term in ("第一目的:=漢字圧縮", "成立条件:=", "KDSL-Intl", "KDSL-DP直接実行禁止"):
            self.assertIn(term, spec)
        for token in ("→", "=>", ":=", "未確認", "API名", "`/`は選択／orを意味しない"):
            self.assertIn(token, core)


if __name__ == "__main__":
    unittest.main()
