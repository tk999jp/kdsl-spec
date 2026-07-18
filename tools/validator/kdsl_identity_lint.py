from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REQUIRED = {
    "spec/core/kdsl-spec.md": [
        "KDSL:=日本語promptを漢字語幹／記号／最小制御語へ再構成する",
        "KDSL本体:=漢字圧縮",
        "KDSL-Intl:=非漢字言語",
        "漢字表現をoptional lexiconへ降格禁止",
    ],
    "spec/profiles/kdsl-profile-dev-prompt.md": [
        "漢字圧縮 > 要件保持",
        "KDSL_RESULT:",
        "状態:",
    ],
    "spec/profiles/kdsl-converter-prompt.md": [
        "surface: 漢字圧縮",
        "KEY翻訳だけで終了禁止",
        "英語KEYへの自動退行禁止",
    ],
    "spec/r1/r1-result-spec.md": [
        "R1は成果物・仕様書・引継書・次期roadmapではない",
        "build／diff／lint／test／CI pass != RT:v",
    ],
}

FORBIDDEN = {
    "spec/core/kdsl-spec.md": [
        "KDSL-CP漢:=",
        "lexicon: kanji-v1",
        "KDSLは言語中立",
    ],
    "spec/profiles/kdsl-profile-dev-prompt.md": [
        "GOAL:",
        "WORK:",
        "VERIFY:",
        "SUCCESS_CRITERIA:",
    ],
}


def main() -> int:
    errors: list[str] = []
    for rel, needles in REQUIRED.items():
        path = ROOT / rel
        if not path.exists():
            errors.append(f"missing:{rel}")
            continue
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"required:{rel}:{needle}")

    for rel, needles in FORBIDDEN.items():
        path = ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle in text:
                errors.append(f"forbidden:{rel}:{needle}")

    examples = list((ROOT / "examples" / "kanji").glob("*.md"))
    if not examples:
        errors.append("missing:examples/kanji")
    else:
        joined = "\n".join(p.read_text(encoding="utf-8") for p in examples)
        if "目的:" not in joined or ("守:" not in joined and "成功条件:" not in joined):
            errors.append("examples:kanji structure missing")

    if errors:
        print("KDSL identity lint: failed")
        for error in errors:
            print(error)
        return 1

    print("KDSL identity lint: passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
