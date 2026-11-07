"""Small deterministic regression for the reviewed KDSL examples.

No parser/LLM oracle: semantic equivalence and runtime behavior require independent checks.
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
        self.assertEqual(5, len(self.samples))
        self.assertEqual(5, len({c["id"] for c in self.samples}))

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
