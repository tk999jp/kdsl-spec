import argparse
import json
import sys
from pathlib import Path

from kdsl_parser_v2 import DocumentNodeV2, collect_value_kinds, node_to_data


def parse_args(argv):
    parser = argparse.ArgumentParser(description='Parse KDSL-family documents into the additive typed AST v2.')
    parser.add_argument('path')
    parser.add_argument('--context', choices=('active-document', 'raw-envelope'), default='active-document')
    parser.add_argument('--json', action='store_true', dest='as_json')
    return parser.parse_args(argv[1:])


def load_text(path):
    if path == '-':
        return sys.stdin.read()
    return Path(path).read_text(encoding='utf-8')


def main(argv):
    args = parse_args(argv)
    document = DocumentNodeV2.parse(load_text(args.path), context=args.context)
    envelopes = document.envelopes()
    headers = document.headers()
    value_kinds = collect_value_kinds(document)

    if args.as_json:
        print(json.dumps(node_to_data(document), ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print('PARSER_V2_RESULT:')
        print('STATUS: ' + ('fail' if document.errors else ('warn' if document.warnings else 'pass')))
        print('CONTEXT: ' + document.context)
        print('CHILD_COUNT: ' + str(len(document.children)))
        print('HEADER_COUNT: ' + str(len(headers)))
        print('HEADERS: ' + (','.join(header.key for header in headers) if headers else 'none'))
        print('ENVELOPE_COUNT: ' + str(len(envelopes)))
        print('ENVELOPES: ' + (','.join(envelope.marker for envelope in envelopes) if envelopes else 'none'))
        print('VALUE_KINDS: ' + (','.join(value_kinds) if value_kinds else 'none'))
        print('DIAGNOSTICS:')
        for issue in document.issues or [None]:
            if issue is None:
                print('  - none')
            else:
                print(f'  - {issue.severity}: {issue.format()}')

    if not document.errors and not document.warnings:
        print('PARSER_V2_AST_READY')
    return document.exit_code


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
