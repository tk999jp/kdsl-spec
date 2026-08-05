from __future__ import annotations

import re
import tomllib
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORPUS = ROOT / "examples" / "behavior" / "standalone-cases.toml"

REQUIRED_KINDS = {
    "min",
    "dense",
    "result-only",
    "compare",
    "lint",
    "compact",
    "intl",
}


def deployed_size(text: str) -> int:
    return len(re.sub(r"\s+", "", text))


def main() -> int:
    errors: list[str] = []

    if not CORPUS.exists():
        print("KDSL standalone behavior: failed")
        print(f"missing:{CORPUS.relative_to(ROOT)}")
        return 1

    data = tomllib.loads(CORPUS.read_text(encoding="utf-8"))
    cases = data.get("case", [])
    if data.get("version") != 1:
        errors.append("corpus-version:expected-1")
    if len(cases) < 8:
        errors.append(f"case-count:{len(cases)}<8")

    ids = [case.get("id", "") for case in cases]
    if len(ids) != len(set(ids)):
        errors.append("case-id:duplicate")
    if any(not case_id for case_id in ids):
        errors.append("case-id:missing")

    kinds = {case.get("kind") for case in cases}
    missing_kinds = REQUIRED_KINDS - kinds
    if missing_kinds:
        errors.append("kind-missing:" + ",".join(sorted(missing_kinds)))

    groups: dict[str, dict[str, dict[str, object]]] = defaultdict(dict)
    marker_count = 0
    identifier_count = 0

    for case in cases:
        case_id = str(case.get("id", "<missing>"))
        kind = str(case.get("kind", ""))
        source = str(case.get("input", "")).strip()
        output = str(case.get("output", "")).strip()

        if not source:
            errors.append(f"{case_id}:input-empty")
        if not output:
            errors.append(f"{case_id}:output-empty")
            continue

        for needle in case.get("required", []):
            marker_count += 1
            if needle not in output:
                errors.append(f"{case_id}:required:{needle}")

        for needle in case.get("forbidden", []):
            if needle in output:
                errors.append(f"{case_id}:forbidden:{needle}")

        for identifier in case.get("identifiers", []):
            identifier_count += 1
            if identifier not in source:
                errors.append(f"{case_id}:identifier-not-in-input:{identifier}")
            if identifier not in output:
                errors.append(f"{case_id}:identifier-not-preserved:{identifier}")

        prefix = case.get("prefix")
        if prefix and not output.startswith(str(prefix)):
            errors.append(f"{case_id}:prefix:{prefix}")

        if kind == "result-only":
            for forbidden in ("```", "変換しました", "以下", "説明"):
                if forbidden in output:
                    errors.append(f"{case_id}:result-lock:{forbidden}")
        elif kind == "compare":
            for heading in ("元文:", "min:", "dense:", "削減点:", "意味risk:", "推奨:"):
                if heading not in output:
                    errors.append(f"{case_id}:compare-heading:{heading}")
        elif kind == "lint":
            if "変換: 未実施" not in output:
                errors.append(f"{case_id}:lint-transform-state")
            if "format: KDSL" in output:
                errors.append(f"{case_id}:lint-converted")
        elif kind == "compact":
            if "profile: compact-prompt" not in output:
                errors.append(f"{case_id}:compact-profile")
            for heading in ("目的:", "材料:", "出力:", "規則:", "確認:"):
                if heading not in output:
                    errors.append(f"{case_id}:compact-heading:{heading}")
        elif kind == "intl":
            if "KDSL-Intl" not in output or "canonical" not in output:
                errors.append(f"{case_id}:intl-boundary")
        elif kind == "min":
            if "mode: min" not in output:
                errors.append(f"{case_id}:mode-min")
        elif kind == "dense":
            if "mode:dense" not in output:
                errors.append(f"{case_id}:mode-dense")

        group = case.get("group")
        if group:
            groups[str(group)][kind] = case

    pair_count = 0
    for group, pair in groups.items():
        if "min" not in pair or "dense" not in pair:
            errors.append(f"group:{group}:min-dense-pair-required")
            continue
        pair_count += 1
        min_case = pair["min"]
        dense_case = pair["dense"]
        recommended = min_case.get("recommended_mode")
        if recommended != dense_case.get("recommended_mode"):
            errors.append(f"group:{group}:recommendation-mismatch")
            continue

        min_size = deployed_size(str(min_case["output"]))
        dense_size = deployed_size(str(dense_case["output"]))
        expected = "dense" if dense_size < min_size else "min"
        if recommended != expected:
            errors.append(
                f"group:{group}:recommended:{recommended}!={expected}"
                f":min={min_size}:dense={dense_size}"
            )

    if pair_count < 2:
        errors.append(f"mode-pair-count:{pair_count}<2")

    if errors:
        print("KDSL standalone behavior: failed")
        for error in errors:
            print(error)
        return 1

    print(
        "KDSL standalone behavior: passed "
        f"cases={len(cases)} kinds={len(kinds)} "
        f"markers={marker_count} identifiers={identifier_count} pairs={pair_count}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
