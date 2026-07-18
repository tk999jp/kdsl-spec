from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_FILES = (
    "spec/core/kdsl-spec.md",
    "spec/core/kdsl-core.md",
    "spec/core/kdsl-modes.md",
    "spec/profiles/kdsl-profile-dev-prompt.md",
    "spec/profiles/kdsl-profile-compact-prompt.md",
    "spec/profiles/kdsl-converter-prompt.md",
    "spec/profiles/kdsl-profile-intl.md",
    "spec/agent/kdsl-agent-execution.md",
    "spec/r1/r1-result-spec.md",
    "spec/lint/kdsl-lint-checklist.md",
    "spec/lint/kdsl-agent-lint.md",
    "spec/bridge/kdsl-adps-bridge.md",
    "docs/reviews/kdsl-v2-asset-audit.md",
    "tools/validator/kdsl_document_lint.py",
    "tools/validator/r1_result_lint.py",
    "tools/validator/kdsl_agent_lint.py",
    "tools/validator/run_canonical_samples.py",
)

REQUIRED = {
    "spec/core/kdsl-spec.md": (
        "KDSL:=日本語promptを漢字語幹／記号／最小制御語へ再構成する",
        "第一目的は**漢字圧縮**",
        "KDSL本体:=漢字圧縮",
        "KDSL-Intl:=非漢字言語",
        "profile: dev-prompt|compact-prompt|converter|lint",
        "agent: required|optional",
        "安全契機:=Uが明示した重大条件の限定保護",
        "標準Agent:=KDSL_PROMPT＋K1",
        "P1:=任意短縮転送表現",
    ),
    "spec/profiles/kdsl-profile-dev-prompt.md": (
        "agent: required",
        "通常投入は `KDSL_PROMPT＋K1`",
        "P1は任意短縮",
        "形式lint pass!=Codex Agent実効性",
    ),
    "spec/profiles/kdsl-profile-compact-prompt.md": (
        "目的:", "材料:", "出力:", "規則:", "確認:",
    ),
    "spec/agent/kdsl-agent-execution.md": (
        "Agent目的:=U明示scopeを必要最小契約で調査→実装→検証→完了",
        "標準必須:",
        "KDSL_PROMPT＋K1",
        "P1!=可逆性保証",
        "Agent層!=汎用安全framework",
    ),
    "spec/r1/r1-result-spec.md": (
        "KDSL_RESULT:", "状態:", "実機:", "次:", "commit:",
    ),
    "docs/reviews/kdsl-v2-asset-audit.md": (
        "監査対象: PR #1〜#145", "採否未決: 0", "PR範囲未監査: 0", "Agent再審査",
    ),
}

FORBIDDEN_ACTIVE = (
    "lexicon:kanji-v1",
    "lexicon: kanji-v1",
    "KDSL-CP漢:=",
    "KDSLは言語中立",
    "Safety Gate Registry:=",
    "P1:=P1L可逆短縮",
    "P1:=P1Lの可逆短縮",
)

ACTIVE_SPECS = (
    "spec/core/kdsl-spec.md",
    "spec/profiles/kdsl-profile-dev-prompt.md",
    "spec/profiles/kdsl-profile-compact-prompt.md",
    "spec/profiles/kdsl-converter-prompt.md",
    "spec/agent/kdsl-agent-execution.md",
    "spec/r1/r1-result-spec.md",
)


def main() -> int:
    errors: list[str] = []
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            errors.append(f"missing:{rel}")

    for rel, needles in REQUIRED.items():
        path = ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"required:{rel}:{needle}")

    for rel in ACTIVE_SPECS:
        path = ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for needle in FORBIDDEN_ACTIVE:
            if needle in text:
                errors.append(f"forbidden:{rel}:{needle}")

    examples = list((ROOT / "examples" / "kanji").glob("*.md"))
    if len(examples) < 3:
        errors.append("examples/kanji:3件未満")
    for path in examples:
        text = path.read_text(encoding="utf-8")
        if "目的:" not in text:
            errors.append(f"example目的欠落:{path.name}")
        if any(f"\n{alias}:" in text for alias in "役目材出則守調確"):
            errors.append(f"example未定義alias:{path.name}")

    if errors:
        print("KDSL identity lint: failed")
        for error in errors:
            print(error)
        return 1
    print("KDSL identity lint: passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())