from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "prompts" / "kdsl-converter-standalone.md"

REQUIRED = (
    "# KDSL Standalone Converter",
    "種別: standalone compiled prompt",
    "用途: ChatGPT Project instructions／単独instruction",
    "状態: 非正本／配布・投入用",
    "正本競合→正本優先",
    "spec/core/kdsl-spec.md",
    "spec/core/kdsl-core.md",
    "spec/core/kdsl-modes.md",
    "spec/profiles/kdsl-converter-prompt.md",
    "spec/lint/kdsl-lint-checklist.md",
    "KDSL:=日本語promptを漢字語幹／記号／最小制御語へ再構成する漢字圧縮DSL",
    "第一目的:=漢字圧縮",
    "KDSL本体:=漢字圧縮",
    "KDSL-Intl:=非漢字言語／ASCII／英語KEY向け派生subset",
    "A. 漢字KDSL mode:min",
    "B. 漢字KDSL mode:dense",
    "C. dense結果のみ",
    "D. 比較付き",
    "E. lintのみ",
    "F. CompactPrompt",
    "G. KDSL-Intl",
    "KEY翻訳だけで完了禁止",
    "条件→／変換=>／優先>／状態:=／衝突×／並列/",
    "安全契機:=ユーザー明示重大条件の限定保護",
    "command／path／URL／repo名／branch名／tag名／package名",
    "KDSL_PROMPT前自然文禁止",
    "C:結果のみ→KDSL本文以外禁止",
    "出力前必須:",
    "英語KEY退行なし",
    "未確認／未実行反転なし",
    "入力外安全条件追加なし",
)

FORBIDDEN = (
    "KDSL:=言語中立",
    "KDSL-Intl:=KDSL本体",
    "英語KEY:=既定",
    "漢字表現:=optional",
    "Safety Gate Registry:=KDSL",
)

MAX_LINES = 500
MAX_NON_WHITESPACE = 8_000


def main() -> int:
    errors: list[str] = []

    if not TARGET.exists():
        print("KDSL standalone lint: failed")
        print("missing:prompts/kdsl-converter-standalone.md")
        return 1

    text = TARGET.read_text(encoding="utf-8")

    for needle in REQUIRED:
        if needle not in text:
            errors.append(f"required:{needle}")

    for needle in FORBIDDEN:
        if needle in text:
            errors.append(f"forbidden:{needle}")

    line_count = len(text.splitlines())
    if line_count > MAX_LINES:
        errors.append(f"line-count:{line_count}>{MAX_LINES}")

    deployed_size = len(re.sub(r"\s+", "", text))
    if deployed_size > MAX_NON_WHITESPACE:
        errors.append(f"non-whitespace-size:{deployed_size}>{MAX_NON_WHITESPACE}")

    if text.count("状態: 非正本／配布・投入用") != 1:
        errors.append("non-canonical-marker:must-appear-once")

    if errors:
        print("KDSL standalone lint: failed")
        for error in errors:
            print(error)
        return 1

    print(
        "KDSL standalone lint: passed "
        f"lines={line_count} non_whitespace={deployed_size} required={len(REQUIRED)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
