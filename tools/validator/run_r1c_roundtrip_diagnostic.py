import tempfile
from pathlib import Path

from run_r1c_roundtrip_samples import optional_doc, run_cli, safety_gate_doc


def main():
    results = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        optional_path = tmp_path / 'optional.md'
        optional_path.write_text(optional_doc(), encoding='utf-8')
        results.append(
            run_cli(
                'optional evidence and authority structural pass',
                optional_path,
                0,
                ('optional JSON blocks preserved',),
            )
        )

        safety_path = tmp_path / 'safety.md'
        safety_path.write_text(safety_gate_doc(), encoding='utf-8')
        results.append(
            run_cli(
                'optional Safety Gates structural pass',
                safety_path,
                0,
                ('STATUS: structural_pass', 'optional SAFETY_GATES registry/entry/order preserved'),
            )
        )

    failed = sum(not result for result in results)
    print('SUMMARY:')
    print(f'  total: {len(results)}')
    print(f'  failed: {failed}')
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
