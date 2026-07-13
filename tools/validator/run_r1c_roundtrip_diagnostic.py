import tempfile
from pathlib import Path

from run_r1c_roundtrip_samples import optional_doc, run_cli


def main():
    results = []
    with tempfile.TemporaryDirectory() as tmp:
        optional_path = Path(tmp) / 'optional.md'
        optional_path.write_text(optional_doc(), encoding='utf-8')
        results.append(
            run_cli(
                'optional evidence and authority structural pass',
                optional_path,
                0,
                ('optional JSON blocks preserved',),
            )
        )

    failed = sum(not result for result in results)
    print('SUMMARY:')
    print(f'  total: {len(results)}')
    print(f'  failed: {failed}')
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
