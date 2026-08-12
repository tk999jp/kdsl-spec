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
    "examples/kanji/agent-operational-proof.kdsl.md",
    "tools/validator/kdsl_document_lint.py",
    "tools/validator/r1_result_lint.py",
    "tools/validator/kdsl_agent_lint.py",
    "tools/validator/kdsl_agent_operational_regression.py",
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
        "同一事項競合→後発確定>先発確定>仮説／提案／状態観測",
        "撤回済／置換済判断→再採用禁止",
        "対象外の観測可能意味変更禁止",
        "圧縮成立:=重複統合→正本参照化→助詞削減→漢字語幹化→条件記号化→最小制御語化",
        "同一長値・固定条件は原則一回だけ定義",
        "source／test／Docs／State相互一致!=上位契約変更根拠",
    ),
    "spec/core/kdsl-core.md": (
        "直近記述のみ→確定扱禁止",
        "状態観測／実装／test／Docs／State／結果証跡→明示なし契約正本扱禁止",
        "内部rename／refactor可; 対象外動作同値必須",
        "正本参照化",
        "AI判断!=U確定",
    ),
    "spec/core/kdsl-modes.md": (
        "dense非膨張:",
        "同一長値・固定条件→正本一回定義→短名参照",
    ),
    "spec/profiles/kdsl-profile-dev-prompt.md": (
        "agent: required",
        "通常投入は `KDSL_PROMPT＋K1`",
        "P1は任意短縮",
        "形式lint pass!=Codex Agent実効性",
        "直近U確定 > canonical contract > 確認済実機契約",
        "現実装が確定契約違反→scope内復元可",
        "確定契約testの削除／期待値反転／弱体化禁止",
        "期待値変更→上位根拠必須",
        "AI判断→U確定扱い禁止",
        "test pass != 契約適合",
    ),
    "spec/profiles/kdsl-profile-compact-prompt.md": (
        "目的:", "材料:", "出力:", "規則:", "確認:",
    ),
    "spec/profiles/kdsl-converter-prompt.md": (
        "契約世代／正本／意味scope照合",
        "撤回済／置換済判断→再採用禁止",
        "対象外の観測可能意味変更を許可する表現追加禁止",
        "→正本参照化",
        "dense:",
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
    "spec/lint/kdsl-lint-checklist.md": (
        "後発確定保持／撤回済判断復活なし",
        "状態観測の契約正本昇格なし",
        "契約変更と契約違反復元の混同なし",
        "契約test弱体化許可なし",
        "正本参照不足:",
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
