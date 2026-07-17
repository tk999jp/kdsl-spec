from __future__ import annotations

import sys
from pathlib import Path

from kdsl_p1_contract import (
    P1_SCHEMA_ID,
    P1L_SCHEMA_ID,
    compare_models,
    load_text,
    parse_contract,
    parse_p1_line,
    render_p1,
    source_digest,
)


def round_trip_text(text: str):
    source = parse_contract(text, require=True)
    if source.errors or source.model is None:
        return source, None, ['source contract failed validation']

    try:
        rendered = render_p1(source.model)
    except (KeyError, TypeError, ValueError) as exc:
        return source, None, ['P1 rendering failed: ' + str(exc)]

    reconstructed_result = parse_p1_line(rendered)
    if reconstructed_result.errors or reconstructed_result.model is None:
        return source, rendered, [
            'rendered P1 failed reconstruction',
            *reconstructed_result.errors,
        ]

    mismatches = compare_models(source.model, reconstructed_result.model)
    if source.kind == 'P1' and source.source_scope != rendered:
        mismatches.append('source P1 is not canonical rendering')
    return source, rendered, mismatches


def emit(source, rendered, mismatches):
    status = 'structural_pass' if not mismatches else 'fail'
    schema = P1L_SCHEMA_ID if source.kind == 'P1L' else P1_SCHEMA_ID
    print('P1_STRUCTURAL_ROUND_TRIP_RESULT:')
    print('STATUS: ' + status)
    print('SOURCE_KIND: ' + str(source.kind or 'none'))
    print('SOURCE_SCHEMA: ' + schema)
    print('SOURCE_DIGEST: ' + str(source_digest(source)))
    print('TARGET_SCHEMA: ' + P1_SCHEMA_ID)
    print('EXECUTABLE: no')
    print('SEMANTIC_EQUIVALENCE: not_proven')
    print('EXECUTION_AUTHORITY: none')
    print('CHECKS:')
    checks = [
        'all P1L required projections preserved',
        'canonical P1 segment order preserved',
        'nested field order and exact values preserved',
        'scope/context/guard/stop/verify/runtime/output preserved',
        'all eight authority rails preserved',
        'normalization and binding boundaries preserved',
        'exact Unicode strings preserved through JSON rendering',
    ]
    for item in checks if not mismatches else ['source parsed', 'P1 rendering attempted', 'reconstruction compared']:
        print('  - ' + item)
    print('ERRORS:')
    for item in mismatches or ['none']:
        print('  - ' + item)
    print('P1_RENDERED:')
    print(rendered or 'none')
    return 0 if not mismatches else 2


def main(argv):
    if len(argv) != 2:
        print('usage: python kdsl_p1_roundtrip.py <p1l-or-p1-file>')
        return 2
    path = Path(argv[1])
    source, rendered, mismatches = round_trip_text(load_text(path))
    return emit(source, rendered, mismatches)


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
