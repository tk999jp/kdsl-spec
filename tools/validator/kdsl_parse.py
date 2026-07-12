import argparse
import json
import sys

from kdsl_parser import DiagnosticBag, DocumentNode, load_text


def parse_args(argv):
    parser = argparse.ArgumentParser(description='Parse KDSL-family envelopes into a source-spanned AST.')
    parser.add_argument('path')
    parser.add_argument('--envelope', required=True)
    parser.add_argument('--json', action='store_true', dest='as_json')
    return parser.parse_args(argv[1:])


def main(argv):
    args = parse_args(argv)
    text = load_text(args.path)
    document = DocumentNode.parse(text)
    envelope = document.find_envelope(args.envelope)
    bag = DiagnosticBag()
    for issue in document.issues:
        bag.add_issue(issue)

    if envelope is None:
        bag.error('PARSER_ENVELOPE_MISSING', f'envelope not found: {args.envelope}')
        return bag.emit()

    for issue in envelope.issues:
        bag.add_issue(issue)

    payload = {
        'envelope': envelope.marker,
        'span': envelope.span.format(),
        'field_count': len(envelope.fields),
        'fields': [
            {
                'name': field.name,
                'span': field.span.format(),
                'inline': field.inline_value,
                'value': field.value_text(combine_multiline=True),
                'raw': field.raw_text,
            }
            for field in envelope.fields
        ],
        'duplicates': envelope.duplicates,
    }

    if args.as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print('PARSE_RESULT:')
        print('ENVELOPE: ' + envelope.marker)
        print('SPAN: ' + envelope.span.format())
        print('FIELD_COUNT: ' + str(len(envelope.fields)))
        print('FIELDS: ' + ','.join(envelope.field_order))
        print('DUPLICATES: ' + (','.join(envelope.duplicates) if envelope.duplicates else 'none'))

    if not bag.errors and not bag.warnings:
        bag.note('PARSER_AST_READY', f'{envelope.marker} parsed with source spans')
    return bag.emit()


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
