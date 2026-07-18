from __future__ import annotations

from pathlib import Path

from kdsl_document_lint import lint_paths, lint_text
from r1_result_lint import lint_text as lint_r1

ROOT = Path(__file__).resolve().parents[2]

ACTIVE_DOCUMENTS = [
    ROOT / "templates/base/kdsl_base_dev.md",
    ROOT / "templates/tasks/task_corrective_impl.md",
    ROOT / "templates/tasks/task_investigation_only.md",
    ROOT / "templates/tasks/task_docs_state_closeout.md",
    ROOT / "templates/result/r1_result_spec.md",
    ROOT / "examples/kanji/midfd-dev-prompt.kdsl.md",
    ROOT / "examples/kanji/blog-meta.kdsl.md",
]

VALID_DEV = """KDSL_PROMPT:
format: KDSL
profile: dev-prompt
mode: min
safety: normal
局面: 修正
目的: 表示不具合修正
対象: MainForm.cs
作業: 原因限定→実装→試験
検証: targeted test
報告: KDSL_RESULT
"""
INVALID_ENGLISH = """KDSL_PROMPT:
GOAL: fix
WORK: edit
VERIFY: test
"""
INVALID_LEXICON = """format: KDSL
lexicon:kanji-v1
目的: 圧縮
作業: 変換
"""
INVALID_AUTHORITY = """目的: 修正
AUTHORITY:
  edit: allow
作業: 実装
"""
VALID_COMPACT = """format: KDSL
profile: compact-prompt
目的: 記事meta生成
材料: 本文
出力: 要約／title
規則: 本文外事実追加禁止
確認: 指定形式のみ
"""
VALID_R1 = """KDSL_RESULT:
状態: success
局面: 修正
要約: 表示補正完了
変更: MainForm.cs
理由: 表示条件誤り
実行: dotnet test
検証: 10件pass
実機: v / U実機観測
危険: なし
次: 提案なし
commit: actual abc123
"""
INVALID_R1_ENGLISH = """KDSL_RESULT:
STATUS: success
PHASE: fix
S: done
FILES: a
WHY: b
CMD: c
VERIFY: d
RT: v
RISK: none
NEXT: none
COMMIT: x
"""
INVALID_RT = """KDSL_RESULT:
状態: success
局面: 修正
要約: 完了
変更: a
理由: b
実行: test
検証: pass
実機: v / build pass
危険: なし
次: 提案なし
commit: none
"""


def expect(name: str, errors: list[str], should_pass: bool) -> list[str]:
    if should_pass and errors:
        return [f"{name}:期待pass:{'|'.join(errors)}"]
    if not should_pass and not errors:
        return [f"{name}:期待failだがpass"]
    return []


def main() -> int:
    failures: list[str] = []
    failures += expect("valid-dev", lint_text(VALID_DEV), True)
    failures += expect("invalid-english", lint_text(INVALID_ENGLISH), False)
    failures += expect("invalid-lexicon", lint_text(INVALID_LEXICON), False)
    failures += expect("invalid-authority", lint_text(INVALID_AUTHORITY), False)
    failures += expect("valid-compact", lint_text(VALID_COMPACT), True)
    failures += expect("valid-r1", lint_r1(VALID_R1), True)
    failures += expect("invalid-r1-english", lint_r1(INVALID_R1_ENGLISH), False)
    failures += expect("invalid-rt", lint_r1(INVALID_RT), False)
    failures.extend(lint_paths(ACTIVE_DOCUMENTS, ROOT))
    if failures:
        for failure in failures:
            print("FAIL", failure)
        return 1
    print(f"PASS cases=8 documents={len(ACTIVE_DOCUMENTS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
