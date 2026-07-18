from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from kdsl_binding_evaluator_input import evaluate_inputs
from kdsl_binding_evaluator_model import compact_reference


def load_json(path: str) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(value, dict):
        raise ValueError('facts JSON must be an object')
    return value


def main(argv: list[str]) -> int:
    if len(argv) != 6:
        print('usage: evaluator <contract> <k1> <pf1> <facts.json> <output>')
        return 2
    try:
        model, text, errors = evaluate_inputs(
            Path(argv[1]).read_text(encoding='utf-8'),
            Path(argv[2]).read_text(encoding='utf-8'),
            Path(argv[3]).read_text(encoding='utf-8'),
            load_json(argv[4]),
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        model, text, errors = None, '', [str(exc)]
    print('BINDING_EVALUATION:')
    if errors or model is None:
        print('STATUS: blocked')
        for item in errors:
            print('ERROR: ' + item)
        print('EXECUTABLE: false')
        return 2
    output = Path(argv[5])
    output.write_text(text, encoding='utf-8')
    print('STATUS: generated')
    print('OUTPUT: ' + str(output))
    print('REFERENCE: ' + compact_reference(model))
    print('EXECUTABLE: false')
    return 0
