"""Closed-scope behavior oracles for four KDSL regression examples.

These tests check observable decisions, not just preserved substrings.
They deliberately do NOT parse arbitrary KDSL or prove LLM equivalence.
"""

import itertools
import json
from pathlib import Path
import re
import unittest

CASES = Path(__file__).resolve().parents[2] / "examples/kanji/behavior_cases.json"
TERMS = ("src dir非空", "src dir空", "移動失敗", "移動成功", "かつ", "または", "A", "B", "C", "(", ")")


def condition(expr, variables):
    """Evaluate only the boolean expressions used in these test fixtures."""
    tokens = []
    remaining = expr.strip()
    while remaining:
        term = next((s for s in TERMS if remaining.startswith(s)), None)
        if term is None:
            raise ValueError("unsupported condition: " + remaining)
        tokens.append(term)
        remaining = remaining[len(term):].lstrip()
    cursor = 0

    def atom():
        nonlocal cursor
        if cursor >= len(tokens):
            raise ValueError("missing operand")
        token = tokens[cursor]
        cursor += 1
        if token == "(":
            value = disjunction()
            if cursor >= len(tokens) or tokens[cursor] != ")":
                raise ValueError("unclosed parenthesis")
            cursor += 1
            return value
        if token not in variables:
            raise ValueError("unknown variable: " + token)
        return variables[token]

    def conjunction():
        nonlocal cursor
        value = atom()
        while cursor < len(tokens) and tokens[cursor] == "かつ":
            cursor += 1
            rhs = atom()
            value = value and rhs
        return value

    def disjunction():
        nonlocal cursor
        value = conjunction()
        while cursor < len(tokens) and tokens[cursor] == "または":
            cursor += 1
            rhs = conjunction()
            value = value or rhs
        return value

    result = disjunction()
    if cursor != len(tokens):
        raise ValueError("trailing condition tokens")
    return result


def scope_matches(text):
    """Expected rule: deletion iff source empty AND move succeeded."""
    m = re.search(r"条件:\s*(.*?)→src dir削除\s*[／/]\s*(.*?)→保持", text)
    if not m or "条件確認→成立時のみ削除" not in text:
        return False
    for empty, success in itertools.product((False, True), repeat=2):
        env = {"src dir空": empty, "src dir非空": not empty,
               "移動成功": success, "移動失敗": not success}
        if condition(m.group(1), env) != (empty and success):
            return False
        if condition(m.group(2), env) != (not (empty and success)):
            return False
    return True


def precedence_matches(text):
    """Expected rule: execute iff A AND (B OR C)."""
    m = re.search(r"条件:\s*(.*?)→実行(?:[／/;]|\n|$)", text)
    if not m or "A不成立→実行禁止" not in text:
        return False
    for a, b, c in itertools.product((False, True), repeat=3):
        if condition(m.group(1), {"A": a, "B": b, "C": c}) != (a and (b or c)):
            return False
    return True


def approval_matches(text):
    """Editing/testing allowed; commit awaiting approval; no diff disposal."""
    permission = re.search(r"commit\s*=\s*(承認待|可|必須|禁止)", text)
    return bool(permission and permission.group(1) == "承認待"
                and re.search(r"編集[／/]試験=可", text)
                and re.search(r"禁止:\s*未push差分破棄", text))


def runtime_matches(text):
    """Build/test passed, but physical runtime remains unverified."""
    actual = re.search(r"実機:\s*(未確認|確認済)", text)
    return bool(actual and actual.group(1) == "未確認"
                and re.search(r"検証:\s*build[／/]test成功", text)
                and "RT:v扱禁止" in text)


CHECKS = {
    "condition-scope": scope_matches,
    "condition-precedence": precedence_matches,
    "explicit-approval": approval_matches,
    "runtime-separation": runtime_matches,
}

# Mutants change outcome, permission, state or the limiting condition.
MUTATIONS = {
    "condition-scope": (("空かつ移動成功", "空または移動成功"),
                        ("非空または移動失敗", "非空かつ移動失敗"),
                        ("成立時のみ削除", "削除")),
    "condition-precedence": (("Aかつ(BまたはC)", "Aまたは(BかつC)"),
                             ("実行禁止", "実行可")),
    "explicit-approval": (("commit=承認待", "commit=可"),
                          ("禁止:未push差分破棄", "許可:未push差分破棄")),
    "runtime-separation": (("未確認", "確認済"),
                           ("RT:v扱禁止", "RT:v扱可")),
}


class KDSLSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = {case["id"]: case
                     for case in json.loads(CASES.read_text(encoding="utf-8"))}

    def test_curated_decisions_match_oracles(self):
        for case_id, check in CHECKS.items():
            for mode in ("min", "dense"):
                with self.subTest(case=case_id, mode=mode):
                    self.assertTrue(check(self.cases[case_id][mode]))

    def test_semantic_mutations_fail_behavior_oracles(self):
        tested = 0
        for case_id, changes in MUTATIONS.items():
            for mode in ("min", "dense"):
                for before, after in changes:
                    with self.subTest(case=case_id, mode=mode, mutation=after):
                        source = self.cases[case_id][mode]
                        # Adapt only optional spacing after a section colon.
                        # Do not strip source whitespace: "src dir" is part of a term.
                        needle = before if before in source else before.replace(":", ": ")
                        self.assertIn(needle, source)
                        mutant = source.replace(needle, after, 1)
                        self.assertFalse(CHECKS[case_id](mutant))
                        tested += 1
        self.assertEqual(18, tested)

    def test_equivalent_condition_reorder_remains_valid(self):
        for mode in ("min", "dense"):
            scope = self.cases["condition-scope"][mode]
            equivalent = scope.replace("src dir空かつ移動成功", "移動成功かつsrc dir空")
            self.assertTrue(scope_matches(equivalent))
            p = self.cases["condition-precedence"][mode]
            equivalent = p.replace("Aかつ(BまたはC)", "(BまたはC)かつA")
            self.assertTrue(precedence_matches(equivalent))

    def test_parser_rejects_unsupported_or_ill_formed_expression(self):
        for expr in ("Aまたは?", "Aかつ", "(AかつB", "AとB", "A B"):
            with self.subTest(expr=expr):
                with self.assertRaises(ValueError):
                    condition(expr, {"A": True, "B": False})


if __name__ == "__main__":
    unittest.main()
