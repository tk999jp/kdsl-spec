import sys

from kdsl_parser import DocumentNode, load_text, parse_top_level_legacy
from kdsl_parser_v2_compat import R1CCompatibilityView


def compare(text):
    errors = []
    info = []

    legacy_document = DocumentNode.parse(text)
    legacy_envelope = legacy_document.find_envelope('KDSL_RESULT')
    view = R1CCompatibilityView.from_text(text)

    legacy_present = legacy_envelope is not None
    v2_present = view is not None
    if legacy_present != v2_present:
        errors.append(
            f'envelope presence mismatch: legacy={legacy_present} v2={v2_present}'
        )
        return errors, info

    if legacy_envelope is None or view is None:
        info.append('KDSL_RESULT absent in both parsers')
        return errors, info

    legacy_scope = tuple(legacy_envelope.raw_lines)
    legacy_entries, legacy_duplicates = parse_top_level_legacy(
        legacy_scope,
        'KDSL_RESULT',
        combine_multiline_json=True,
    )
    legacy_entries_tuple = tuple(legacy_entries)
    legacy_duplicates_tuple = tuple(legacy_duplicates)

    if legacy_scope != view.scope_lines:
        errors.append('scope line mismatch')
    if legacy_entries_tuple != view.entries:
        errors.append(
            'entry mismatch:\n'
            f'legacy={legacy_entries_tuple!r}\n'
            f'v2={view.entries!r}'
        )
    if legacy_duplicates_tuple != view.duplicates:
        errors.append(
            'duplicate-field mismatch: '
            f'legacy={legacy_duplicates_tuple!r} v2={view.duplicates!r}'
        )

    if not errors:
        info.append('scope lines match')
        info.append('field order/value/relative-line entries match')
        info.append('duplicate field list matches')
        info.append('raw-source compatibility retained')
    return errors, info


def emit(errors, info):
    print('R1C_PARSER_PARITY_RESULT:')
    print('STATUS: ' + ('fail' if errors else 'pass'))
    print('ERRORS:')
    for item in errors or ['none']:
        print('  - ' + item)
    print('INFO:')
    for item in info or ['none']:
        print('  - ' + item)
    print('BOUNDARY: structural parity only; no semantic/authority/RT proof')
    return 2 if errors else 0


def main(argv):
    path = argv[1] if len(argv) > 1 else '-'
    errors, info = compare(load_text(path))
    return emit(errors, info)


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
