from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterable

ENGLISH_KEYS = re.compile(
    r"(?m)^\s*(?:PHASE|GOAL|SUCCESS_CRITERIA|EVIDENCE|SOURCE_OF_TRUTH|"
    r"AUTHORITY|APPROVAL_BOUNDARY|SCOPE|NON_GOALS|WORK|TEST|VERIFY|"
    r"STOP_CONDITIONS|REPORT|STATUS|FILES|WHY|CMD|RT|RISK|NEXT|COMMIT|"
    r"Goal|Input|Output|Guard|Check)\s*:"
)
KANJI_KEYS = re.compile(
    r"(?m)^\s*(?:局面|目的|成功条件|根拠|正本|権限|承認境界|対象|非対象|"
    r"作業|試験|検証|停止条件|報告|材料|出力|規則|確認|状態|要約|変更|"
    r"理由|実行|実機|危険|次|commit)\s*:"
)
UNDEFINED_ALIASES = re.compile(r"(?m)^\s*(?:役|目|材|出|則|守|調|確)\s*:")
FORBIDDEN = (
    "lexicon:kanji-v1",
    "lexicon: kanji-v1",
    "KDSL-CP漢",
    "Safety Gate Registry",
    "SAFETY_GATES:",
    "PACKET_DRAFT:",
)
OVER_SAFETY = re.compile(r"(?m)^\s*AUTHORITY\s*:")


def lint_text(text: str, *, intl: bool = False, require_keys: bool = True) -> list[str]:
    errors: list[str] = []
    if not intl:
        matches = sorted({match.group(0).strip() for match in ENGLISH_KEYS.finditer(text)})
        if matches:
            errors.append("英語構造KEY:" + ",".join(matches))
        aliases = sorted({match.group(0).strip() for match in UNDEFINED_ALIASES.finditer(text)})
        if aliases:
            errors.append("未定義一字alias:" + ",".join(aliases))
        for token in FORBIDDEN:
            if token in text:
                errors.append("旧v2構造:" + token)
        if OVER_SAFETY.search(text):
            errors.append("過剰安全block:AUTHORITY")
        if require_keys and not KANJI_KEYS.search(text):
            errors.append("日本語構造KEYなし")
    return errors


def lint_paths(paths: Iterable[Path], root: Path) -> list[str]:
    errors: list[str] = []
    for path in paths:
        if not path.exists():
            errors.append(f"不存在:{path.as_posix()}")
            continue
        text = path.read_text(encoding="utf-8")
        intl = "examples/intl/" in path.as_posix() or "profile-intl" in path.name
        for error in lint_text(text, intl=intl):
            try:
                rel = path.relative_to(root)
            except ValueError:
                rel = path
            errors.append(f"{rel.as_posix()}:{error}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="KDSL漢字identity文書lint")
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    errors = lint_paths(args.paths, args.root)
    if errors:
        for error in errors:
            print("ERROR", error)
        return 1
    print(f"PASS documents={len(args.paths)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
