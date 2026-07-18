from __future__ import annotations

import argparse
from pathlib import Path

K1_FIELDS = ("状態", "現在", "完了", "未完", "検証", "実機", "次", "停止理由")
K1_STATES = {"計画", "実行中", "検証中", "実機待", "完了", "停止", "失敗"}
K1_VERIFY = {"未実行", "一部", "成功", "失敗"}
K1_RUNTIME = {"不要", "未確認", "確認済"}
RESUME_FIELDS = ("run", "契約", "baseline")
P1L_FIELDS = (
    "版", "目的", "成功条件", "正本", "対象", "非対象", "権限", "承認境界",
    "作業", "検証", "実機要否", "停止条件", "完了条件", "報告",
)
AUTH_VALUES = {"可", "不可", "承認待", "対象外"}
PF1_FIELDS = (
    "project", "正本", "既定profile", "既定mode", "Phase方針", "権限既定",
    "承認必須", "試験方針", "実機方針", "報告方針",
)
BLOCK_MARKERS = {"P1L:", "K1:", "PF1:", "KDSL_RESULT:"}


def _parse_block(text: str, marker: str, nested_key: str | None = None) -> tuple[dict[str, str], dict[str, str]]:
    fields: dict[str, str] = {}
    nested: dict[str, str] = {}
    in_block = False
    in_nested = False
    for raw in text.splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if not in_block:
            if stripped == marker:
                in_block = True
            continue
        if stripped in BLOCK_MARKERS and stripped != marker:
            break
        if stripped.startswith("P1|"):
            break
        if not stripped:
            continue
        if line.startswith("  "):
            if in_nested and ":" in line:
                key, value = stripped.split(":", 1)
                nested[key.strip()] = value.strip()
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        fields[key] = value.strip()
        in_nested = nested_key is not None and key == nested_key
    return fields, nested


def _lint_authority(authority: dict[str, str], prefix: str) -> list[str]:
    if not authority:
        return [f"{prefix}権限値欠落"]
    return [
        f"{prefix}権限値不正:{rail}={value}"
        for rail, value in authority.items()
        if value not in AUTH_VALUES
    ]


def lint_p1l(text: str) -> list[str]:
    fields, authority = _parse_block(text, "P1L:", "権限")
    errors: list[str] = []
    for key in P1L_FIELDS:
        if key not in fields:
            errors.append(f"P1L field欠落:{key}")
    if fields.get("版") != "kdsl-agent@1.1":
        errors.append("P1L版不一致")
    if fields.get("実機要否") not in {"要", "不要"}:
        errors.append("P1L実機要否不正")
    if fields.get("報告") != "R1":
        errors.append("P1L報告不一致")
    errors.extend(_lint_authority(authority, "P1L"))
    return errors


def lint_p1(text: str) -> list[str]:
    line = next((line.strip() for line in text.splitlines() if line.strip().startswith("P1|")), "")
    required = ("版", "目的", "成功", "正本", "対象", "権限", "作業", "検証", "停止", "完了", "報告")
    fields: dict[str, str] = {}
    for part in line.split("|")[1:]:
        if ":" in part:
            key, value = part.split(":", 1)
            fields[key.strip()] = value.strip()
    errors = [f"P1 field欠落:{key}" for key in required if key not in fields]
    if fields.get("版") != "kdsl-agent@1.1":
        errors.append("P1版不一致")
    return errors


def lint_k1(text: str) -> list[str]:
    fields, _ = _parse_block(text, "K1:")
    errors: list[str] = []
    for key in K1_FIELDS:
        if key not in fields:
            errors.append(f"K1 field欠落:{key}")
    if fields.get("状態") not in K1_STATES:
        errors.append("K1状態不正")
    if fields.get("検証") not in K1_VERIFY:
        errors.append("K1検証状態不正")
    if fields.get("実機") not in K1_RUNTIME:
        errors.append("K1実機状態不正")
    if any(key in fields for key in ("目的", "対象", "権限")):
        errors.append("K1契約再定義禁止")
    if fields.get("状態") == "完了":
        if fields.get("未完") != "なし":
            errors.append("K1完了時未完あり")
        if fields.get("検証") != "成功":
            errors.append("K1完了時検証未成功")
        if fields.get("実機") not in {"不要", "確認済"}:
            errors.append("K1完了時実機未確定")
    if "再開: required" in text or "handoff: required" in text:
        for key in RESUME_FIELDS:
            if not fields.get(key):
                errors.append(f"K1再開識別欠落:{key}")
    return errors


def lint_pf1(text: str) -> list[str]:
    fields, authority = _parse_block(text, "PF1:", "権限既定")
    errors: list[str] = []
    for key in PF1_FIELDS:
        if key not in fields:
            errors.append(f"PF1 field欠落:{key}")
    if fields.get("既定profile") != "dev-prompt":
        errors.append("PF1既定profile不一致")
    if fields.get("既定mode") not in {"readable", "min", "dense", "lock"}:
        errors.append("PF1既定mode不正")
    errors.extend(_lint_authority(authority, "PF1"))
    return errors


def lint_text(text: str) -> list[str]:
    errors: list[str] = []
    agent_required = "agent: required" in text
    has_k1 = "K1:" in text
    has_p1l = "P1L:" in text
    has_p1 = any(line.strip().startswith("P1|") for line in text.splitlines())
    has_pf1 = "PF1:" in text

    if agent_required and not has_k1:
        errors.append("Agent必須時K1欠落")
    if has_p1l and has_p1:
        errors.append("P1L／P1同時記載禁止")
    if has_k1:
        errors.extend(lint_k1(text))
    if has_p1l:
        errors.extend(lint_p1l(text))
    if has_p1:
        errors.extend(lint_p1(text))
    if has_pf1:
        errors.extend(lint_pf1(text))
    if not any((agent_required, has_k1, has_p1l, has_p1, has_pf1)):
        errors.append("Agent契約block欠落")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="KDSL Agent契約lint")
    parser.add_argument("path", type=Path)
    args = parser.parse_args(argv)
    errors = lint_text(args.path.read_text(encoding="utf-8"))
    if errors:
        for error in errors:
            print("ERROR", error)
        return 1
    print("PASS Agent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())