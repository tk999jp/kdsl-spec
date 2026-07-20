from __future__ import annotations

import argparse
from pathlib import Path

STATE_MARKERS = {"開始:", "境界:", "中断:", "再開:", "終了:"}
PROHIBITED_K1_KEYS = {"目的", "成功条件", "対象", "非対象", "権限"}


def _items(value: str) -> set[str]:
    value = value.strip()
    if not value or value == "なし":
        return set()
    return {item.strip() for item in value.split("／") if item.strip()}


def _parse_cases(text: str) -> dict[str, dict[str, dict[str, str]]]:
    cases: dict[str, dict[str, dict[str, str]]] = {}
    current_case: str | None = None
    current_state: str | None = None

    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("```"):
            continue
        if line.startswith("事例:"):
            current_case = line.split(":", 1)[1].strip()
            cases[current_case] = {"meta": {}}
            current_state = None
            continue
        if current_case is None:
            continue
        if line in STATE_MARKERS:
            current_state = line[:-1]
            cases[current_case][current_state] = {}
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        target = cases[current_case][current_state] if current_state else cases[current_case]["meta"]
        target[key.strip()] = value.strip()

    return cases


def _require_fields(case: str, state_name: str, state: dict[str, str], fields: tuple[str, ...]) -> list[str]:
    return [f"{case}/{state_name}:field欠落:{field}" for field in fields if field not in state]


def _lint_k1_shape(case: str, state_name: str, state: dict[str, str]) -> list[str]:
    errors = _require_fields(
        case,
        state_name,
        state,
        ("状態", "現在", "完了", "未完", "検証", "実機", "次", "停止理由"),
    )
    for key in sorted(PROHIBITED_K1_KEYS & set(state)):
        errors.append(f"{case}/{state_name}:K1契約再定義:{key}")
    return errors


def _lint_complete(case: str, state_name: str, state: dict[str, str]) -> list[str]:
    errors: list[str] = []
    if state.get("状態") != "完了":
        errors.append(f"{case}/{state_name}:状態!=完了")
    if _items(state.get("未完", "")):
        errors.append(f"{case}/{state_name}:未完あり")
    if state.get("検証") != "成功":
        errors.append(f"{case}/{state_name}:検証未成功")
    if state.get("実機") not in {"不要", "確認済"}:
        errors.append(f"{case}/{state_name}:実機未確定")
    return errors


def _lint_normal(case: dict[str, dict[str, str]]) -> list[str]:
    errors: list[str] = []
    meta = case.get("meta", {})
    start = case.get("開始", {})
    end = case.get("終了", {})

    required = _items(meta.get("必須", ""))
    forbidden = _items(meta.get("禁止", ""))
    if not {"KDSL_PROMPT", "K1"}.issubset(required):
        errors.append("通常:標準必須block不一致")
    if not {"P1L", "P1", "PF1"}.issubset(forbidden):
        errors.append("通常:不要block禁止不足")

    errors += _lint_k1_shape("通常", "開始", start)
    errors += _lint_k1_shape("通常", "終了", end)
    if start.get("状態") != "計画" or start.get("検証") != "未実行":
        errors.append("通常:開始状態不正")
    errors += _lint_complete("通常", "終了", end)

    initial_work = _items(start.get("未完", ""))
    completed_work = _items(end.get("完了", ""))
    if not initial_work.issubset(completed_work):
        errors.append("通常:開始未完が終了完了へ収束しない")
    return errors


def _parse_authority(value: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for item in _items(value):
        if "=" in item:
            key, val = item.split("=", 1)
            result[key.strip()] = val.strip()
    return result


def _lint_approval(case: dict[str, dict[str, str]]) -> list[str]:
    errors: list[str] = []
    meta = case.get("meta", {})
    start = case.get("開始", {})
    boundary = case.get("境界", {})
    authority = _parse_authority(meta.get("権限", ""))

    expected = {
        "読取": "可",
        "編集": "可",
        "試験": "可",
        "commit": "承認待",
        "push": "承認待",
    }
    for key, value in expected.items():
        if authority.get(key) != value:
            errors.append(f"承認境界:権限不一致:{key}")

    errors += _lint_k1_shape("承認境界", "開始", start)
    errors += _lint_k1_shape("承認境界", "境界", boundary)
    if boundary.get("状態") != "停止":
        errors.append("承認境界:境界状態!=停止")
    if boundary.get("検証") != "成功":
        errors.append("承認境界:境界前検証未成功")

    completed = _items(boundary.get("完了", ""))
    if not {"調査", "実装", "試験", "検証"}.issubset(completed):
        errors.append("承認境界:価値作業未完")
    pending = _items(boundary.get("未完", ""))
    if not pending or not pending.issubset({"commit", "push"}):
        errors.append("承認境界:未完が承認操作以外を含む")
    boundary_op = meta.get("境界操作", "")
    if boundary_op not in pending:
        errors.append("承認境界:境界操作が未完にない")
    if boundary.get("停止理由") != f"{boundary_op}承認待":
        errors.append("承認境界:停止理由不一致")
    return errors


def _lint_resume(case: dict[str, dict[str, str]]) -> list[str]:
    errors: list[str] = []
    meta = case.get("meta", {})
    names = ("開始", "中断", "再開", "終了")
    states = {name: case.get(name, {}) for name in names}

    if meta.get("再開") != "required":
        errors.append("中断再開:required欠落")

    identifiers = ("run", "契約", "baseline")
    for name, state in states.items():
        errors += _lint_k1_shape("中断再開", name, state)
        errors += _require_fields("中断再開", name, state, identifiers)

    for key in identifiers:
        values = {states[name].get(key, "") for name in names}
        if "" in values or len(values) != 1:
            errors.append(f"中断再開:識別不一致:{key}")

    if states["開始"].get("状態") != "計画":
        errors.append("中断再開:開始状態不正")
    if states["中断"].get("状態") != "実行中" or states["再開"].get("状態") != "実行中":
        errors.append("中断再開:中断／再開状態不正")
    if states["再開"].get("現在") != states["中断"].get("次"):
        errors.append("中断再開:未完位置から再開していない")
    if _items(states["再開"].get("完了", "")) != _items(states["中断"].get("完了", "")):
        errors.append("中断再開:既完了作業が変化")
    if _items(states["再開"].get("未完", "")) != _items(states["中断"].get("未完", "")):
        errors.append("中断再開:未完作業が変化")

    start_pending = _items(states["開始"].get("未完", ""))
    interrupted_done = _items(states["中断"].get("完了", ""))
    interrupted_pending = _items(states["中断"].get("未完", ""))
    if not interrupted_done or not interrupted_done.issubset(start_pending):
        errors.append("中断再開:中断完了が開始作業外")
    if not interrupted_pending or not interrupted_pending < start_pending:
        errors.append("中断再開:中断時未完が縮小していない")

    errors += _lint_complete("中断再開", "終了", states["終了"])
    if not start_pending.issubset(_items(states["終了"].get("完了", ""))):
        errors.append("中断再開:開始作業が終了完了へ収束しない")
    return errors


def _lint_run_changed(case: dict[str, dict[str, str]]) -> list[str]:
    errors: list[str] = []
    meta = case.get("meta", {})
    start = case.get("開始", {})
    end = case.get("終了", {})
    candidates = _items(meta.get("候補", ""))
    expected_changed = _items(meta.get("期待変更", ""))
    expected_unchanged = _items(meta.get("期待除外", ""))

    if not candidates:
        errors.append("Run差分:候補欠落")
        return errors
    if set(start) != candidates:
        errors.append("Run差分:開始state候補不一致")
    if set(end) != candidates:
        errors.append("Run差分:終了state候補不一致")
    if expected_changed & expected_unchanged:
        errors.append("Run差分:期待変更／除外重複")
    if expected_changed | expected_unchanged != candidates:
        errors.append("Run差分:期待分類不足")

    actual_changed = {path for path in candidates if start.get(path) != end.get(path)}
    if actual_changed != expected_changed:
        errors.append(
            "Run差分:RunChanged不一致:"
            + "期待=" + "／".join(sorted(expected_changed))
            + ":実際=" + "／".join(sorted(actual_changed))
        )

    required_changed = {
        "src/Clean.cs",
        "src/DirtyChanged.cs",
        "src/New.cs",
        "src/Delete.cs",
        "src/OldName.cs",
        "src/NewName.cs",
    }
    required_unchanged = {
        "src/DirtyUnchanged.cs",
        "src/Restored.cs",
        "tests/ExecutedOnlyTests.cs",
    }
    if not required_changed.issubset(expected_changed):
        errors.append("Run差分:変更代表事例不足")
    if not required_unchanged.issubset(expected_unchanged):
        errors.append("Run差分:除外代表事例不足")
    return errors


def lint_text(text: str) -> list[str]:
    cases = _parse_cases(text)
    errors: list[str] = []
    for required in ("通常", "承認境界", "中断再開", "Run差分"):
        if required not in cases:
            errors.append(f"事例欠落:{required}")
    if errors:
        return errors
    errors += _lint_normal(cases["通常"])
    errors += _lint_approval(cases["承認境界"])
    errors += _lint_resume(cases["中断再開"])
    errors += _lint_run_changed(cases["Run差分"])
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="KDSL Agent運用状態遷移／Run差分回帰")
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=Path("examples/kanji/agent-operational-proof.kdsl.md"),
    )
    args = parser.parse_args(argv)
    errors = lint_text(args.path.read_text(encoding="utf-8"))
    if errors:
        for error in errors:
            print("ERROR", error)
        return 1
    print("PASS scenarios=4 normal=1 approval=1 resume=1 run_changed=1 runtime=unverified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
