from __future__ import annotations

from pathlib import Path
from typing import Callable

from kdsl_packet_roundtrip import parse_normalization

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent
VALID = ROOT / 'samples' / 'sample_normalization_valid.md'
FULL_EXAMPLE = REPO_ROOT / 'examples' / 'packet' / 'normalization-full-kdsl.example.md'
BLOCKED_EXAMPLE = REPO_ROOT / 'examples' / 'packet' / 'normalization-p1-blocked.example.md'


def read(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def check_valid_scalars() -> None:
    parsed = parse_normalization(read(VALID))
    assert parsed['values']['SCHEMA'] == 'kdsl-packet-normalization@0.1-draft'
    assert parsed['values']['STATUS'] == 'non-executable'
    assert parsed['source']['normalize_state'] == 'not_normalized'
    assert parsed['target'] == {
        'kind': 'full-kdsl-dev-prompt',
        'schema': 'format:KDSL/profile:dev-prompt',
        'resolution': 'resolved',
        'executable': 'false',
    }
    assert parsed['round_trip']['semantic_equivalence'] == 'not_proven'
    assert parsed['authority']['execution_authority'] == 'none'
    assert parsed['output']['executable'] == 'false'


def check_map_order() -> None:
    parsed = parse_normalization(read(VALID))
    sources = [record.get('source') for record in parsed['map_records']]
    assert len(sources) == 17
    assert sources == [
        'SCHEMA',
        'STATUS',
        'BASE',
        'TASK',
        'SRC',
        'READ',
        'TGT',
        'OBS',
        'GOAL',
        'NON',
        'SG',
        'STOP',
        'FLOW',
        'VERIFY',
        'OUT',
        'AUTHORITY',
        'NORMALIZE',
    ]


def check_preserve_and_preview() -> None:
    parsed = parse_normalization(read(VALID))
    assert parsed['preserve']['exact_strings'] == ['src/Example.cs']
    assert parsed['preserve']['protected_wording'] == [
        'KDSL_PROMPT_PREVIEW != KDSL_PROMPT'
    ]
    assert parsed['preserve']['ordered_fields'] == [
        'FLOW-READ>FLOW-GATE>FLOW-REPORT'
    ]
    assert parsed['preview'] == (
        'KDSL_PROMPT_PREVIEW:\n'
        'format: KDSL\n'
        'profile: dev-prompt\n'
        'execution: prohibited'
    )


def check_fenced_repository_example() -> None:
    parsed = parse_normalization(read(FULL_EXAMPLE))
    assert parsed['values']['STATUS'] == 'non-executable'
    assert parsed['target']['kind'] == 'full-kdsl-dev-prompt'
    assert parsed['target']['resolution'] == 'resolved'
    assert parsed['output']['marker'] == 'KDSL_PROMPT_PREVIEW'
    assert parsed['preview'].startswith('KDSL_PROMPT_PREVIEW:')


def check_blocked_p1_example() -> None:
    parsed = parse_normalization(read(BLOCKED_EXAMPLE))
    assert parsed['target'] == {
        'kind': 'P1',
        'schema': 'unresolved',
        'resolution': 'blocked',
        'executable': 'false',
    }
    assert parsed['output']['marker'] == 'none'
    assert parsed['output']['executable'] == 'false'
    assert parsed['preview'] == ''
    assert parsed['loss'] == []
    assert parsed['unresolved'][0]['impact'] == 'blocked'


def check_missing_envelope() -> None:
    try:
        parse_normalization('SCHEMA: kdsl-packet-normalization@0.1-draft\n')
    except ValueError as exc:
        assert str(exc) == 'NORMALIZATION_DRAFT block not found'
        return
    raise AssertionError('missing NORMALIZATION_DRAFT did not raise ValueError')


def check_duplicate_nested_scalar_last_wins() -> None:
    text = read(VALID).replace(
        '  normalize_state: not_normalized\n',
        '  normalize_state: not_normalized\n  normalize_state: mutated\n',
        1,
    )
    parsed = parse_normalization(text)
    assert parsed['source']['normalize_state'] == 'mutated'


def check_nested_list_order_mutation() -> None:
    text = read(VALID).replace(
        '    - "src/Example.cs"\n',
        '    - "first"\n    - "src/Example.cs"\n    - "last"\n',
        1,
    )
    parsed = parse_normalization(text)
    assert parsed['preserve']['exact_strings'] == ['first', 'src/Example.cs', 'last']


def check_preview_block_mutation() -> None:
    text = read(VALID).replace(
        '    execution: prohibited\n',
        '    execution: prohibited\n    guard: unchanged\n',
        1,
    )
    parsed = parse_normalization(text)
    assert parsed['preview'].endswith('execution: prohibited\nguard: unchanged')


def check_boundary_mutations_are_not_coerced() -> None:
    text = read(VALID)
    text = text.replace(
        'TARGET:\n  kind: full-kdsl-dev-prompt\n'
        '  schema: "format:KDSL/profile:dev-prompt"\n'
        '  resolution: resolved\n'
        '  executable: false\n',
        'TARGET:\n  kind: full-kdsl-dev-prompt\n'
        '  schema: "format:KDSL/profile:dev-prompt"\n'
        '  resolution: resolved\n'
        '  executable: true\n',
        1,
    )
    text = text.replace(
        '  semantic_equivalence: not_proven\n',
        '  semantic_equivalence: claimed\n',
        1,
    )
    text = text.replace(
        '  execution_authority: none\n',
        '  execution_authority: allow\n',
        1,
    )
    text = text.replace(
        'OUTPUT:\n  marker: KDSL_PROMPT_PREVIEW\n  executable: false\n',
        'OUTPUT:\n  marker: KDSL_PROMPT_PREVIEW\n  executable: true\n',
        1,
    )
    parsed = parse_normalization(text)
    assert parsed['target']['executable'] == 'true'
    assert parsed['round_trip']['semantic_equivalence'] == 'claimed'
    assert parsed['authority']['execution_authority'] == 'allow'
    assert parsed['output']['executable'] == 'true'


CASES: tuple[tuple[str, Callable[[], None]], ...] = (
    ('valid nested scalar contract', check_valid_scalars),
    ('MAP record order contract', check_map_order),
    ('PRESERVE and preview contract', check_preserve_and_preview),
    ('fenced repository example contract', check_fenced_repository_example),
    ('blocked P1 artifact contract', check_blocked_p1_example),
    ('missing envelope error contract', check_missing_envelope),
    ('duplicate nested scalar last-wins contract', check_duplicate_nested_scalar_last_wins),
    ('nested list order mutation contract', check_nested_list_order_mutation),
    ('preview block mutation contract', check_preview_block_mutation),
    ('boundary mutation extraction fidelity', check_boundary_mutations_are_not_coerced),
)


def main() -> int:
    failed = 0
    for name, case in CASES:
        try:
            case()
        except Exception as exc:  # noqa: BLE001 - corpus reports exact assertion/runtime failure
            failed += 1
            print('FAIL: ' + name)
            print('  ' + type(exc).__name__ + ': ' + str(exc))
        else:
            print('PASS: ' + name)

    print('SUMMARY:')
    print('  total: ' + str(len(CASES)))
    print('  failed: ' + str(failed))
    print(
        'BOUNDARY: consumer contract pass != migration/semantic equivalence/'
        'safety proof/adapter retirement proof/RT:v/authority/release readiness'
    )
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
