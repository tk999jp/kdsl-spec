from __future__ import annotations

import sys

from kdsl_binding_evidence_core import emit, load_text, match_reference, parse_definition, parse_reference


def main(argv: list[str]) -> int:
    if len(argv) not in {2, 3}:
        print('usage: python kdsl_binding_evidence.py <evidence-file> [compact-reference]')
        return 2
    result = parse_definition(load_text(argv[1]))
    if len(argv) == 3 and result.model is not None:
        reference, errors = parse_reference(argv[2])
        result.errors.extend(errors)
        if reference is not None and not errors:
            result.errors.extend(match_reference(reference, result.model))
            if not result.errors:
                result.info.append('compact P1L runtime_control reference matched exact identity')
    return emit(result)


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
