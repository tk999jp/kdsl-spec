from __future__ import annotations

import ast
from pathlib import Path

from kdsl_parser_v2_safety_gate_compat import SafetyGateCompatibilityView

ROOT = Path(__file__).resolve().parent

HELPER_CONSUMERS = {
    'kdsl_safety_gate_inheritance.py': {
        'structural': set(),
        'semantic': {'REGISTRY', 'aggregate_state', 'authority_is_unverified', 'is_blank'},
    },
    'kdsl_safety_gate_graph.py': {
        'structural': set(),
        'semantic': {'REGISTRY', 'aggregate_state', 'authority_is_unverified', 'is_blank'},
    },
    'kdsl_r1c_optional.py': {
        'structural': set(),
        'semantic': {
            'KNOWN_IDS',
            'KNOWN_STATES',
            'REGISTRY',
            'REQUIRED_FIELDS',
            'authority_is_unverified',
            'is_blank',
        },
    },
}

MIGRATED_CONSUMERS = {
    'kdsl_safety_semantics.py': {'SafetyGateCompatibilityView'},
    'kdsl_safety_gate_inheritance.py': {'SafetyGateCompatibilityView'},
    'kdsl_safety_gate_graph.py': {'SafetyGateCompatibilityView'},
    'kdsl_r1c_optional.py': {'SafetyGateCompatibilityView'},
}

WRAPPERS = {
    'run_safety_semantics_samples.py',
    'run_safety_semantics_examples.py',
    'kdsl_validate.py',
}


def imports_from(path: Path, module: str) -> set[str]:
    tree = ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == module:
            imported.update(alias.name for alias in node.names)
    return imported


def record(name: str, ok: bool, detail: str = '') -> bool:
    print(('PASS' if ok else 'FAIL') + ': ' + name)
    if detail:
        print('  ' + detail)
    return ok


def main() -> int:
    results: list[bool] = []

    actual_consumers = {
        path.name
        for path in ROOT.glob('*.py')
        if imports_from(path, 'kdsl_safety_gate')
    }
    results.append(
        record(
            'exact remaining Safety Gate semantic helper consumer set',
            actual_consumers == set(HELPER_CONSUMERS),
            'actual=' + repr(sorted(actual_consumers)),
        )
    )

    structural_ok = True
    structural_detail: list[str] = []
    semantic_ok = True
    semantic_detail: list[str] = []
    for filename, expected in HELPER_CONSUMERS.items():
        imported = imports_from(ROOT / filename, 'kdsl_safety_gate')
        expected_structural = expected['structural']
        expected_semantic = expected['semantic']
        actual_structural = imported & {'extract_gate_block', 'parse_registry'}
        actual_semantic = imported - actual_structural
        if actual_structural != expected_structural:
            structural_ok = False
        if actual_semantic != expected_semantic:
            semantic_ok = False
        structural_detail.append(filename + '=' + repr(sorted(actual_structural)))
        semantic_detail.append(filename + '=' + repr(sorted(actual_semantic)))

    results.append(
        record(
            'no remaining consumer imports legacy Safety Gate structural helpers',
            structural_ok,
            '; '.join(structural_detail),
        )
    )
    results.append(
        record(
            'exact semantic utility imports per remaining consumer',
            semantic_ok,
            '; '.join(semantic_detail),
        )
    )

    graph_gate_imports = imports_from(ROOT / 'kdsl_safety_gate_graph.py', 'kdsl_safety_gate')
    inheritance_gate_imports = imports_from(ROOT / 'kdsl_safety_gate_inheritance.py', 'kdsl_safety_gate')
    graph_compat_imports = imports_from(
        ROOT / 'kdsl_safety_gate_graph.py',
        'kdsl_parser_v2_safety_gate_compat',
    )
    inheritance_compat_imports = imports_from(
        ROOT / 'kdsl_safety_gate_inheritance.py',
        'kdsl_parser_v2_safety_gate_compat',
    )
    results.append(
        record(
            'graph and inheritance share migrated structural and retained semantic boundaries',
            graph_gate_imports == inheritance_gate_imports
            and graph_gate_imports == HELPER_CONSUMERS['kdsl_safety_gate_graph.py']['semantic']
            and graph_compat_imports == {'SafetyGateCompatibilityView'}
            and inheritance_compat_imports == {'SafetyGateCompatibilityView'},
            'semantic=' + repr(sorted(graph_gate_imports))
            + ' graph_compat=' + repr(sorted(graph_compat_imports))
            + ' inheritance_compat=' + repr(sorted(inheritance_compat_imports)),
        )
    )

    r1c_gate_imports = imports_from(ROOT / 'kdsl_r1c_optional.py', 'kdsl_safety_gate')
    r1c_compat_imports = imports_from(
        ROOT / 'kdsl_r1c_optional.py',
        'kdsl_parser_v2_safety_gate_compat',
    )
    results.append(
        record(
            'R1C optional uses CompatibilityView and retains only semantic helpers',
            'parse_registry' not in r1c_gate_imports
            and r1c_gate_imports == HELPER_CONSUMERS['kdsl_r1c_optional.py']['semantic']
            and r1c_compat_imports == {'SafetyGateCompatibilityView'},
            'semantic=' + repr(sorted(r1c_gate_imports))
            + ' compat=' + repr(sorted(r1c_compat_imports)),
        )
    )

    fields = set(SafetyGateCompatibilityView.__dataclass_fields__)
    properties = {
        name
        for name, value in SafetyGateCompatibilityView.__dict__.items()
        if isinstance(value, property)
    }
    channels = fields | properties
    required_channels = {
        'present',
        'block_text',
        'registry',
        'entry_dicts',
        'entry_field_orders',
    }
    results.append(
        record(
            'SafetyGateCompatibilityView exposes migration channels',
            required_channels <= channels,
            'channels=' + repr(sorted(required_channels & channels)),
        )
    )

    migrated_ok = True
    migrated_detail: list[str] = []
    for filename, expected in MIGRATED_CONSUMERS.items():
        gate_imports = imports_from(ROOT / filename, 'kdsl_safety_gate')
        compat_imports = imports_from(
            ROOT / filename,
            'kdsl_parser_v2_safety_gate_compat',
        )
        structural_gate_imports = gate_imports & {'extract_gate_block', 'parse_registry'}
        if structural_gate_imports or compat_imports != expected:
            migrated_ok = False
        migrated_detail.append(
            filename
            + ': legacy_structural=' + repr(sorted(structural_gate_imports))
            + ' compat=' + repr(sorted(compat_imports))
        )
    results.append(
        record(
            'all migrated consumers use CompatibilityView without legacy structural helpers',
            migrated_ok,
            '; '.join(migrated_detail),
        )
    )

    all_consumers = set(HELPER_CONSUMERS) | set(MIGRATED_CONSUMERS)
    no_adapter = all(
        not imports_from(ROOT / filename, 'kdsl_parser_adapter')
        for filename in all_consumers
    )
    wrappers_clean = all(
        not imports_from(ROOT / filename, 'kdsl_safety_gate')
        and not imports_from(ROOT / filename, 'kdsl_parser_v2_safety_gate_compat')
        for filename in WRAPPERS
    )
    results.append(
        record(
            'consumers have no adapter import and wrappers remain indirect',
            no_adapter and wrappers_clean,
        )
    )

    failed = sum(not result for result in results)
    print('SUMMARY:')
    print('  total: ' + str(len(results)))
    print('  failed: ' + str(failed))
    print(
        'BOUNDARY: contract pass != consumer migration/semantic equivalence/'
        'complete safety proof/U approval/RT:v/authority/adapter retirement/release readiness'
    )
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
