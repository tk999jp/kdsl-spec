from __future__ import annotations

import argparse
import re
from pathlib import Path

REQUIRED = ["状態", "局面", "要約", "変更", "理由", "実行", "検証", "実機", "危険", "次", "commit"]
ENGLISH = {"STATUS", "PHASE", "S", "FILES", "WHY", "CMD", "VERIFY", "RT", "RISK", "NEXT", "COMMIT"}
FIELD_RE = re.compile(r"^([^\s:#][^:\n]*):[ \t]*(.*)$")
AMBIGUOUS_CHANGE_RE = re.compile(
    r"(主要(?:file|ファイル)|総件数|ほか\d+件|他\d+件|targeted tests?|変更ファイル|変更点|"
    r"\.\.\.|…)",
    re.IGNORECASE,
)
ABSOLUTE_PATH_RE = re.compile(r"^(?:[A-Za-z]:[\\/]|/|\\\\)")


def parse_field_blocks(text: str) -> list[tuple[str, list[str]]]:
    fields: list[tuple[str, list[str]]] = []
    in_result = False
    current: list[str] | None = None

    for raw in text.splitlines():
        stripped = raw.strip()
        if stripped == "KDSL_RESULT:":
            in_result = True
            current = None
            continue
        if not in_result or not stripped or stripped.startswith("```"):
            continue
        match = FIELD_RE.match(stripped)
        if match:
            key = match.group(1).strip()
            values = [match.group(2).strip()] if match.group(2).strip() else []
            fields.append((key, values))
            current = values
            continue
        if current is not None:
            current.append(stripped)

    return fields


def _lint_change_lines(lines: list[str]) -> list[str]:
    errors: list[str] = []
    if not lines:
        return ["変更値欠落"]
    if lines == ["なし"]:
        return errors
    if "なし" in lines:
        errors.append("変更なしとpath混在")

    for line in lines:
        if AMBIGUOUS_CHANGE_RE.search(line):
            errors.append(f"変更path省略／説明混入:{line}")
            continue
        if ABSOLUTE_PATH_RE.search(line):
            errors.append(f"変更pathがrepo相対でない:{line}")
        if "\\" in line:
            errors.append(f"変更path区切り不正:{line}")
        if line.startswith("./") or line.startswith("../") or "/../" in line:
            errors.append(f"変更path正規化不足:{line}")
        if any(token in line for token in ("*", "[", "]")):
            errors.append(f"変更pathが具体pathでない:{line}")
    if len(lines) != len(set(lines)):
        errors.append("変更path重複")
    return errors


def lint_text(text: str) -> list[str]:
    errors: list[str] = []
    if "KDSL_RESULT:" not in text:
        return ["KDSL_RESULT欠落"]
    fields = parse_field_blocks(text)
    keys = [key for key, _ in fields]
    english = [key for key in keys if key in ENGLISH]
    if english:
        errors.append("英語R1 field:" + ",".join(english))
    actual = [key for key in keys if key in REQUIRED]
    if actual != REQUIRED:
        errors.append("日本語R1 field順不一致:" + ",".join(actual))

    values = {key: lines for key, lines in fields}
    errors.extend(_lint_change_lines(values.get("変更", [])))

    runtime = " ".join(values.get("実機", []))
    if re.search(r"(?:^|\b)(?:v|RT:v)(?:\b|$)", runtime):
        if not re.search(r"U実機|対象環境|runtime(?:確認|log)|実機観測", runtime, re.IGNORECASE):
            errors.append("RT:v根拠不足")
        if re.search(r"build|lint|unit test|CI", runtime, re.IGNORECASE) and not re.search(
            r"U実機|対象環境|runtime(?:確認|log)|実機観測", runtime, re.IGNORECASE
        ):
            errors.append("自動検証をRT:v扱い")

    next_value = " ".join(values.get("次", []))
    if next_value and not re.search(r"提案|なし|不要|na|未定", next_value, re.IGNORECASE):
        errors.append("次欄が提案境界不明")
    commit = " ".join(values.get("commit", []))
    if re.search(r"自動(?:commit|コミット)|commit許可|allow", commit, re.IGNORECASE):
        errors.append("commit権限混同")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="日本語KDSL_RESULT lint")
    parser.add_argument("path", type=Path)
    args = parser.parse_args(argv)
    errors = lint_text(args.path.read_text(encoding="utf-8"))
    if errors:
        for error in errors:
            print("ERROR", error)
        return 1
    print("PASS R1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
