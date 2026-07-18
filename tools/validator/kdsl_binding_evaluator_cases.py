from __future__ import annotations

from kdsl_binding_evaluator_cases_base import run_base_cases
from kdsl_binding_evaluator_cases_state import run_state_cases


def main() -> int:
    results = run_base_cases() + run_state_cases()
    failed = len([item for item in results if not item])
    print('total: ' + str(len(results)))
    print('failed: ' + str(failed))
    return 1 if failed else 0
