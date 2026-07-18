from __future__ import annotations

import argparse
from pathlib import Path

AUTH_RAILS = (
    "読取",
    "編集",
    "試験",
    "stage",
    "commit",
    "push",
    "release",
    "public履歴",
    "破壊操作",
)
AUTH_VALUES = {"可", "不可", "承認待", "対象外"}
P1L_FIELDS = (
    "版",
    "実行方式",
    "目的",
    "成功条件",
    "正本",
    "対象",
    "非対象",
    "権限",
    "承認境界",
    "作業",
    "試験",
    "検証",
    "実機要否",
    "停止条件",
    "完了条件",
    "報告",
)
K1_FIELDS = ("状態", "現在", "完了", "未完", "検証", "実機", "次遷移", "停止理由")
K1_STATES = {"計画", "実行中", "検証中", "実機待", "完了", "停止", "失敗"}
K1_VERIFY = {"未実行", "一部", "成功", "失敗"}
K1_RUNTIME = {"不要", "未確認", "確認済"}
PF1_FIELDS = (
    "project",
    "正本",
    "既定profile",
    "既定mode",
    "Phase方針",
    "権限既定",
    "承認必須",
    "試験方針",
    "実機方針",
    "報告方針",
)
BLOCK_MARKERS = {"P1L:", "K1:", "PF1:"}


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
    errors: list[str] = []
    for rail in AUTH_RAILS:
        if rail not in authority:
            errors.append(f"{prefix}権限rail欠落:{rail}")
        elif authority[rail] not in AUTH_VALUES:
            errors.append(f"{prefix}権限値不正:{rail}={authority[rail]}")
    extra = sorted(set(authority) - set(AUTH_RAILS))
    if extra:
        errors.append(f"{prefix}未定義権限rail:{','.join(extra)}")
    return errors


def lint_p1l(text: str) -> list[str]:
    fields, authority = _parse_block(text, "P1L:", "権限")
    errors: list[str] = []
    if not fields:
        return ["P1L欠落"]
    for key in P1L_FIELDS:
        if key not in fields:
            errors.append(f"P1L field欠落:{key}")
    errors.extend(_lint_authority(authority, "P1L"))
    if fields.get("版") != "kdsl-agent@1":
        errors.append("P1L版不一致")
    if fields.get("実行方式") not in {"agent再帰", "単発"}:
        errors.append("P1L実行方式不正")
    if fields.get("実機要否") not in {"要", "不要"}:
        errors.append("P1L実機要否不正")
    if fields.get("報告") != "R1":
        errors.append("P1L報告不一致")
    return errors


def lint_p1(text: str) -> list[str]:
    line = next((line.strip() for line in text.splitlines() if line.strip().startswith("P1|")), "")
    if not line:
        return ["P1欠落"]
    fields: dict[str, str] = {}
    for part in line.split("|")[1:]:
        if ":" not in part:
            continue
        key, value = part.split(":", 1)
        fields[key.strip()] = value.strip()
    errors: list[str] = []
    for key in P1L_FIELDS:
        if key not in fields:
            errors.append(f"P1 field欠落:{key}")
    if fields.get("版") != "kdsl-agent@1":
        errors.append("P1版不一致")
    authority: dict[str, str] = {}
    for item in fields.get("権限", "").split(","):
        if "=" in item:
            key, value = item.split("=", 1)
            authority[key.strip()] = value.strip()
    errors.extend(_lint_authority(authority, "P1"))
    return errors


def lint_k1(text: str) -> list[str]:
    fields, _ = _parse_block(text, "K1:")
    errors: list[str] = []
    if not fields:
        return ["K1欠落"]
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
    return errors


def lint_pf1(text: str) -> list[str]:
    fields, authority = _parse_block(text, "PF1:", "権限既定")
    errors: list[str] = []
    if not fields:
        return ["PF1欠落"]
    for key in PF1_FIELDS:
        if key not in fields:
            errors.append(f"PF1 field欠落:{key}")
    errors.extend(_lint_authority(authority, "PF1"))
    if fields.get("既定profile") != "dev-prompt":
        errors.append("PF1既定profile不一致")
    if fields.get("既定mode") not in {"readable", "min", "dense", "lock"}:
        errors.append("PF1既定mode不正")
    return errors


def lint_text(text: str) -> list[str]:
    errors: list[str] = []
    has_p1 = any(line.strip().startswith("P1|") for line in text.splitlines())
    if "P1L:" in text:
        errors.extend(lint_p1l(text))
    if has_p1:
        errors.extend(lint_p1(text))
    if "K1:" in text:
        errors.extend(lint_k1(text))
    if "PF1:" in text:
        errors.extend(lint_pf1(text))
    if not any(("P1L:" in text, "K1:" in text, "PF1:" in text, has_p1)):
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
