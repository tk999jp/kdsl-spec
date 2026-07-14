from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass
from pathlib import Path

ADAPTER_MODULE = 'kdsl_parser_adapter'
ALLOWED_DIRECT_IMPORTS: dict[str, set[str]] = {}
PROHIBITED_INSTALLERS = {'install_r1c'}

LEGACY_HELPERS = {
    'kdsl_packet': {
        'extract_packet_scope',
        'parse_top_level',
        'blocks_from_entries',
        'parse_nested_scalars',
        'parse_list_field',
        'parse_sequence_items',
    },
    'kdsl_packet_normalization': {
        'extract_scope',
        'parse_top_level',
        'blocks_from_entries',
        'parse_nested_scalars',
        'parse_list_records',
        'parse_nested_lists',
        'extract_multiline',
    },
    'kdsl_safety_gate': {
        'extract_gate_block',
        'parse_registry',
        'aggregate_state',
        'authority_is_unverified',
        'is_blank',
    },
}


@dataclass(frozen=True)
class ImportRecord:
    path: str
    module: str
    symbols: tuple[str, ...]


@dataclass
class InventoryResult:
    direct_adapter: list[ImportRecord]
    legacy_consumers: list[ImportRecord]
    semantic_consumers: list[ImportRecord]
    errors: list[str]

    @property
    def retirement_blocked(self) -> bool:
        return bool(self.direct_adapter or self.legacy_consumers)


def parse_imports(path: Path, root: Path) -> tuple[list[ImportRecord], list[str]]:
    errors: list[str] = []
    records: list[ImportRecord] = []
    try:
        tree = ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    except (OSError, SyntaxError, UnicodeDecodeError) as exc:
        return [], [f'{path}: parse failed: {exc}']

    relative = path.relative_to(root).as_posix() if path.is_relative_to(root) else path.name
    for node in ast.walk(tree):
        if not isinstance(node, ast.ImportFrom) or not node.module:
            continue
        symbols = tuple(sorted(alias.name for alias in node.names))
        records.append(ImportRecord(relative, node.module, symbols))
    return records, errors


def classify(paths: list[Path], root: Path, repository_mode: bool) -> InventoryResult:
    direct: list[ImportRecord] = []
    legacy: list[ImportRecord] = []
    semantic: list[ImportRecord] = []
    errors: list[str] = []

    for path in paths:
        records, parse_errors = parse_imports(path, root)
        errors.extend(parse_errors)
        for record in records:
            basename = Path(record.path).name
            if record.module == ADAPTER_MODULE:
                direct.append(record)
                imported = set(record.symbols)
                prohibited = sorted(imported & PROHIBITED_INSTALLERS)
                for symbol in prohibited:
                    errors.append(f'{record.path}: prohibited adapter installer import: {symbol}')

                allowed = ALLOWED_DIRECT_IMPORTS.get(basename)
                if allowed is None:
                    errors.append(
                        f'{record.path}: unauthorized direct adapter import: '
                        + ', '.join(record.symbols)
                    )
                else:
                    unexpected = sorted(imported - allowed)
                    missing = sorted(allowed - imported)
                    if unexpected:
                        errors.append(
                            f'{record.path}: unexpected adapter installer symbols: '
                            + ', '.join(unexpected)
                        )
                    if missing:
                        errors.append(
                            f'{record.path}: expected adapter installer missing: '
                            + ', '.join(missing)
                        )
                continue

            helper_set = LEGACY_HELPERS.get(record.module)
            if helper_set is None:
                continue
            structural = tuple(sorted(set(record.symbols) & helper_set))
            nonstructural = tuple(sorted(set(record.symbols) - helper_set))
            if structural:
                legacy.append(ImportRecord(record.path, record.module, structural))
            if nonstructural:
                semantic.append(ImportRecord(record.path, record.module, nonstructural))

    if repository_mode:
        by_basename = {
            Path(record.path).name: set(record.symbols)
            for record in direct
        }
        for basename, expected in sorted(ALLOWED_DIRECT_IMPORTS.items()):
            actual = by_basename.get(basename)
            if actual is None:
                errors.append(f'{basename}: expected direct adapter installer import is absent')
            elif actual != expected:
                errors.append(
                    f'{basename}: direct adapter installer set mismatch: '
                    f'expected={sorted(expected)!r} actual={sorted(actual)!r}'
                )

    return InventoryResult(
        direct_adapter=sorted(direct, key=lambda item: (item.path, item.module, item.symbols)),
        legacy_consumers=sorted(legacy, key=lambda item: (item.path, item.module, item.symbols)),
        semantic_consumers=sorted(semantic, key=lambda item: (item.path, item.module, item.symbols)),
        errors=sorted(set(errors)),
    )


def find_python_files(target: Path) -> tuple[list[Path], Path, bool]:
    if target.is_file():
        return [target], target.parent, False
    files = sorted(
        path
        for path in target.rglob('*.py')
        if '__pycache__' not in path.parts and path.is_file()
    )
    return files, target, True


def print_records(title: str, records: list[ImportRecord]) -> None:
    print(title + ':')
    if not records:
        print('  - none')
        return
    for record in records:
        print(
            '  - '
            + record.path
            + ' <- '
            + record.module
            + ': '
            + ','.join(record.symbols)
        )


def emit(result: InventoryResult, repository_mode: bool) -> int:
    status = 'fail' if result.errors else 'pass'
    print('PARSER_ADAPTER_INVENTORY_RESULT:')
    print('STATUS: ' + status)
    print('MODE: ' + ('repository' if repository_mode else 'single-file'))
    print_records('DIRECT_ADAPTER_IMPORTERS', result.direct_adapter)
    print_records('LEGACY_STRUCTURAL_HELPER_CONSUMERS', result.legacy_consumers)
    print_records('NONSTRUCTURAL_MODULE_CONSUMERS', result.semantic_consumers)
    print('ERRORS:')
    for item in result.errors or ['none']:
        print('  - ' + item)
    print('RETIREMENT:')
    print('  state: ' + ('blocked' if result.retirement_blocked else 'candidate'))
    if result.retirement_blocked:
        print('  reason: direct adapter installers or legacy structural helper consumers remain')
    else:
        print('  reason: inventory found no direct installer or known legacy structural helper consumer')
    print(
        'BOUNDARY: inventory pass != semantic equivalence/safety proof/'
        'adapter retirement proof/U approval/RT:v/authority/release readiness'
    )
    return 2 if result.errors else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'target',
        nargs='?',
        default=str(Path(__file__).resolve().parent),
        help='Python file or directory to inventory',
    )
    args = parser.parse_args()
    target = Path(args.target).resolve()
    if not target.exists():
        print('PARSER_ADAPTER_INVENTORY_RESULT:')
        print('STATUS: fail')
        print('ERRORS:')
        print('  - target does not exist: ' + str(target))
        return 2

    paths, root, repository_mode = find_python_files(target)
    result = classify(paths, root, repository_mode)
    return emit(result, repository_mode)


if __name__ == '__main__':
    raise SystemExit(main())
