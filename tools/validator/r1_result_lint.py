from __future__ import annotations

import argparse
import re
from pathlib import Path

REQUIRED = ["状態", "局面", "要約", "変更", "理由", "実行", "検証", "実機", "危険", "次", "commit"]
ENGLISH = {"STATUS", "PHASE", "S", "FILES", "WHY", "CMD", "VERIFY", "RT", "RISK", "NEXT", "COMMIT"}
FIELD_RE = re.compile(r"(?m)^([^\s:#][^:\n]*):[ \t]*(.*)$")


def parse_fields(text: str) -> list[tuple[str, str]]:
    return [(match.group(1).strip(), match.group(2).strip()) for match in FIELD_RE.finditer(text)]


def lint_text(text: str) -> list[str]:
    errors: list[str] = []
    if "KDSL_RESULT:" not in text:
        return ["KDSL_RESULT欠落"]
    fields = parse_fields(text)
    keys = [key for key, _ in fields if key != "KDSL_RESULT"]
    english = [key for key in keys if key in ENGLISH]
    if english:
        errors.append("英語R1 field:" + ",".join(english))
    actual = [key for key in keys if key in REQUIRED]
    if actual != REQUIRED:
        errors.append("日本語R1 field順不一致:" + ",".join(actual))
    values = {key: value for key, value in fields}
    runtime = values.get("実機", "")
    if re.search(r"(?:^|\b)(?:v|RT:v)(?:\b|$)", runtime):
        if not re.search(r"U実機|対象環境|runtime(?:確認|log)|実機観測", runtime, re.IGNORECASE):
            errors.append("RT:v根拠不足")
        if re.search(r"build|lint|unit test|CI", runtime, re.IGNORECASE) and not re.search(
            r"U実機|対象環境|runtime(?:確認|log)|実機観測", runtime, re.IGNORECASE
        ):
            errors.append("自動検証をRT:v扱い")
    next_value = values.get("次", "")
    if next_value and not re.search(r"提案|なし|不要|na|未定", next_value, re.IGNORECASE):
        errors.append("次欄が提案境界不明")
    commit = values.get("commit", "")
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
