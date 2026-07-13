from run_r1c_roundtrip_samples import BLOCKED, INVALID, NEEDS_USER, SUCCESS, run_cli


def main():
    results = [
        run_cli(
            'success example structural pass',
            SUCCESS,
            0,
            ('STATUS: structural_pass', 'SEMANTIC_EQUIVALENCE: not_proven'),
        ),
        run_cli(
            'blocked result structural pass',
            BLOCKED,
            0,
            ('STATUS: structural_pass', 'RT state/basis preserved'),
        ),
        run_cli(
            'needs-user result structural pass',
            NEEDS_USER,
            0,
            ('STATUS: structural_pass', 'NEXT proposal_only boundary preserved'),
        ),
        run_cli(
            'invalid R1C rejected',
            INVALID,
            2,
            ('STATUS: fail', 'source R1C failed validator'),
        ),
    ]
    failed = sum(not result for result in results)
    print('SUMMARY:')
    print(f'  total: {len(results)}')
    print(f'  failed: {failed}')
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
