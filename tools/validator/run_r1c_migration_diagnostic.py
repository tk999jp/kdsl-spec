from run_samples import SAMPLES, run_sample

SELECTED_NAMES = {
    'r1c repository success example valid',
    'r1c repository blocked example valid',
}


def main():
    selected = [sample for sample in SAMPLES if sample['name'] in SELECTED_NAMES]
    failed = 0
    for sample in selected:
        if not run_sample(sample):
            failed += 1
    print('SUMMARY:')
    print(f'  total: {len(selected)}')
    print(f'  failed: {failed}')
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
