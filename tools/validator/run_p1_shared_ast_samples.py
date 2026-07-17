\
from pathlib import Path

from kdsl_parser_v2 import DocumentNodeV2, KNOWN_ENVELOPES
from kdsl_p1_contract import P1L_FIELD_ORDER, parse_contract, render_p1

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent
EXAMPLE = REPO_ROOT / 'examples/adps/p1l-investigate.example.md'
EXPECTED_CONSUMERS = (
    'kdsl_p1.py',
    'kdsl_p1l.py',
    'kdsl_p1_auto.py',
    'kdsl_p1_roundtrip.py',
    'run_p1_contract_samples.py',
    'kdsl_packet_normalize_p1.py',
    'kdsl_packet_p1_property.py',
)


def check(name, condition, detail=''):
    ok = bool(condition)
    print(('PASS' if ok else 'FAIL') + ': ' + name)
    if not ok and detail:
        print('  ' + detail)
    return ok


def main():
    results = []
    source_text = EXAMPLE.read_text(encoding='utf-8')
    parsed_contract = parse_contract(source_text, expected='P1L')
    scope = parsed_contract.source_scope or ''

    results.append(check('P1L is registered in shared KNOWN_ENVELOPES', 'P1L' in KNOWN_ENVELOPES))

    raw_document = DocumentNodeV2.parse(scope, context='raw-envelope')
    raw_envelopes = raw_document.envelopes('P1L')
    results.append(
        check(
            'shared raw-envelope parser recognizes one P1L envelope',
            not raw_document.errors and len(raw_envelopes) == 1,
            repr([issue.format() for issue in raw_document.errors]),
        )
    )
    results.append(
        check(
            'shared P1L field projection preserves canonical order',
            len(raw_envelopes) == 1
            and tuple(field.name for field in raw_envelopes[0].fields) == P1L_FIELD_ORDER,
        )
    )

    active_document = DocumentNodeV2.parse(source_text, context='active-document')
    results.append(
        check(
            'active-document markdown fence isolation remains intact',
            not active_document.envelopes('P1L'),
        )
    )

    duplicate_document = DocumentNodeV2.parse(scope + '\n' + scope, context='raw-envelope')
    results.append(
        check(
            'duplicate shared P1L envelopes are rejected',
            any(issue.code == 'PARSER_DUPLICATE_ENVELOPE' for issue in duplicate_document.errors),
        )
    )

    legacy = 'P1|M:contract_rev=0.1,loss=L|T:I|S:scope|G:ro|V:none|X:missing|O:std'
    legacy_result = parse_contract(legacy, expected='P1')
    results.append(
        check(
            'legacy colon P1 rejection is owned by canonical contract module',
            any('legacy operational P1 colon syntax' in error for error in legacy_result.errors),
            repr(legacy_result.errors),
        )
    )

    if parsed_contract.model is None:
        results.append(check('canonical P1 render source is available', False, repr(parsed_contract.errors)))
    else:
        p1_line = render_p1(parsed_contract.model)
        p1_document = DocumentNodeV2.parse(p1_line, context='raw-envelope')
        results.append(
            check(
                'P1 compact line is not promoted to an AST envelope',
                not p1_document.envelopes(),
            )
        )

    results.append(check('checker-local P1 bootstrap module removed', not (ROOT / 'kdsl_p1_bootstrap.py').exists()))

    remaining = []
    for path in ROOT.glob('*.py'):
        if path.name == 'run_p1_shared_ast_samples.py':
            continue
        if 'kdsl_p1_bootstrap' in path.read_text(encoding='utf-8'):
            remaining.append(path.name)
    results.append(check('no bootstrap imports remain', not remaining, repr(remaining)))

    consumer_failures = []
    for name in EXPECTED_CONSUMERS:
        content = (ROOT / name).read_text(encoding='utf-8')
        if 'kdsl_p1_contract' not in content:
            consumer_failures.append(name)
    results.append(
        check(
            'all known P1/P1L consumers use canonical contract module',
            not consumer_failures,
            repr(consumer_failures),
        )
    )

    failed = sum(not item for item in results)
    print('SUMMARY:')
    print('  total: ' + str(len(results)))
    print('  failed: ' + str(failed))
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
