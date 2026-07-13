from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path

from kdsl_parser_adapter_inventory import (
    InventoryResult,
    classify,
    find_python_files,
)


@dataclass(frozen=True)
class DecisionRecord:
    path: str
    module: str
    symbols: tuple[str, ...]
    decision: str
    reason: str


@dataclass
class MatrixResult:
    records: list[DecisionRecord]
    errors: list[str]

    @property
    def blocking_records(self) -> list[DecisionRecord]:
        return [
            record
            for record in self.records
            if record.decision in {'retain-temporarily', 'migrate-or-replace'}
        ]

    @property
    def retirement_state(self) -> str:
        return 'blocked' if self.blocking_records else 'candidate'


def build_matrix(inventory: InventoryResult) -> MatrixResult:
    records: list[DecisionRecord] = []
    errors = list(inventory.errors)

    for record in inventory.direct_adapter:
        records.append(
            DecisionRecord(
                path=record.path,
                module=record.module,
                symbols=record.symbols,
                decision='retain-temporarily',
                reason='installed helper API compatibility remains under Phase 6D review',
            )
        )

    for record in inventory.legacy_consumers:
        filename = Path(record.path).name.lower()
        if 'parity' in filename:
            decision = 'retain-parity-only'
            reason = 'legacy structural helper is used only to compare the prior extraction contract'
        else:
            decision = 'migrate-or-replace'
            reason = 'consumer imports legacy structural helper and requires dedicated evidence before removal'
        records.append(
            DecisionRecord(
                path=record.path,
                module=record.module,
                symbols=record.symbols,
                decision=decision,
                reason=reason,
            )
        )

    for record in inventory.semantic_consumers:
        records.append(
            DecisionRecord(
                path=record.path,
                module=record.module,
                symbols=record.symbols,
                decision='retain-semantic-api',
                reason='import does not use the bounded legacy structural-helper set',
            )
        )

    records.sort(key=lambda item: (item.path, item.module, item.symbols, item.decision))
    for record in records:
        if record.decision not in {
            'retain-temporarily',
            'migrate-or-replace',
            'retain-parity-only',
            'retain-semantic-api',
        }:
            errors.append(
                f'{record.path}: unclassified dependency decision: {record.decision}'
            )

    return MatrixResult(records=records, errors=sorted(set(errors)))


def emit_text(result: MatrixResult, repository_mode: bool) -> int:
    status = 'fail' if result.errors else 'pass'
    print('PARSER_ADAPTER_CONSUMER_MATRIX_RESULT:')
    print('STATUS: ' + status)
    print('MODE: ' + ('repository' if repository_mode else 'single-file'))
    print('RECORDS:')
    if not result.records:
        print('  - none')
    for record in result.records:
        print(
            '  - '
            + record.path
            + ' <- '
            + record.module
            + ': '
            + ','.join(record.symbols)
            + ' => '
            + record.decision
            + ' / '
            + record.reason
        )
    print('COUNTS:')
    for decision in (
        'retain-temporarily',
        'migrate-or-replace',
        'retain-parity-only',
        'retain-semantic-api',
    ):
        count = sum(record.decision == decision for record in result.records)
        print(f'  {decision}: {count}')
    print('ERRORS:')
    for item in result.errors or ['none']:
        print('  - ' + item)
    print('RETIREMENT:')
    print('  state: ' + result.retirement_state)
    if result.blocking_records:
        print('  blocking_records: ' + str(len(result.blocking_records)))
    else:
        print('  blocking_records: 0')
    print(
        'BOUNDARY: matrix pass != consumer migration/semantic equivalence/'
        'adapter retirement proof/U approval/RT:v/authority/release readiness'
    )
    return 2 if result.errors else 0


def emit_json(result: MatrixResult, repository_mode: bool) -> int:
    payload = {
        'status': 'fail' if result.errors else 'pass',
        'mode': 'repository' if repository_mode else 'single-file',
        'records': [asdict(record) for record in result.records],
        'errors': result.errors,
        'retirement': {
            'state': result.retirement_state,
            'blocking_records': len(result.blocking_records),
        },
        'boundary': (
            'matrix pass != consumer migration/semantic equivalence/'
            'adapter retirement proof/U approval/RT:v/authority/release readiness'
        ),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 2 if result.errors else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'target',
        nargs='?',
        default=str(Path(__file__).resolve().parent),
        help='Python file or directory to classify',
    )
    parser.add_argument('--json', action='store_true', dest='as_json')
    args = parser.parse_args()

    target = Path(args.target).resolve()
    if not target.exists():
        result = MatrixResult([], ['target does not exist: ' + str(target)])
        return emit_json(result, False) if args.as_json else emit_text(result, False)

    paths, root, repository_mode = find_python_files(target)
    inventory = classify(paths, root, repository_mode)
    result = build_matrix(inventory)
    return emit_json(result, repository_mode) if args.as_json else emit_text(result, repository_mode)


if __name__ == '__main__':
    raise SystemExit(main())
