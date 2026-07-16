import re
import sys
from pathlib import Path

from kdsl_parser_v2_safety_gate_compat import SafetyGateCompatibilityView
from kdsl_safety_gate import (
    REGISTRY,
    aggregate_state,
    authority_is_unverified,
    is_blank,
)
from kdsl_safety_semantics import REEVALUATION_RE, scope_relation

RESOLUTION_WORDING = re.compile(
    r'resolved|resolution|解消|解除|原因除去|再確認|再評価|充足確認|verified',
    re.IGNORECASE,
)
SATISFACTION_WORDING = re.compile(
    r'confirmed|verified|確認済|充足|resolved|解消|根拠|再評価',
    re.IGNORECASE,
)


def load_text(path):
    return Path(path).read_text(encoding='utf-8')


def emit(errors, warnings, info):
    status = 'fail' if errors else ('warn' if warnings else 'pass')
    print('VALIDATION_RESULT:')
    print('STATUS: ' + status)
    print('ERRORS:')
    for item in errors or ['none']:
        print('  - ' + item)
    print('WARNINGS:')
    for item in warnings or ['none']:
        print('  - ' + item)
    print('INFO:')
    for item in info or ['none']:
        print('  - ' + item)
    return 2 if errors else (1 if warnings else 0)


def entry_map(text, label, errors):
    view = SafetyGateCompatibilityView.from_text(text)
    if not view.present:
        errors.append(label + ': no SAFETY_GATES block detected')
        return {}
    if view.registry != REGISTRY:
        errors.append(label + ': unknown or missing Safety Gate registry: ' + str(view.registry))
    mapped = {}
    for entry in view.entry_dicts:
        gate_id = entry.get('id', '').strip()
        if gate_id:
            mapped[gate_id] = entry
    return mapped


def transition_basis(entry):
    return ' '.join(str(entry.get(field, '')) for field in ('reason', 'evidence', 'authority'))


def state_of(entry):
    return str(entry.get('state', '')).strip().lower()


def main(argv):
    if len(argv) != 3:
        print('usage: python kdsl_safety_gate_inheritance.py <parent> <child>')
        return 2

    parent_text = load_text(argv[1])
    child_text = load_text(argv[2])
    errors = []
    warnings = []
    info = []

    parent = entry_map(parent_text, 'parent', errors)
    child = entry_map(child_text, 'child', errors)

    for gate_id, parent_entry in sorted(parent.items()):
        parent_state = state_of(parent_entry)
        child_entry = child.get(gate_id)

        if parent_state in {'hold', 'blocked'} and child_entry is None:
            errors.append(f'{gate_id}: parent {parent_state} gate missing from child')
            continue

        if child_entry is None:
            continue

        child_state = state_of(child_entry)
        basis = transition_basis(child_entry)

        if parent_state == 'blocked':
            if child_state == 'na':
                errors.append(f'{gate_id}: inherited blocked gate cannot transition to na')
            elif child_state in {'hold', 'satisfied'} and not RESOLUTION_WORDING.search(basis):
                errors.append(f'{gate_id}: blocked->{child_state} requires explicit resolution evidence')

        elif parent_state == 'hold':
            if child_state == 'na':
                errors.append(f'{gate_id}: inherited hold gate cannot transition to na')
            elif child_state == 'satisfied':
                if is_blank(child_entry.get('evidence')):
                    errors.append(f'{gate_id}: hold->satisfied requires evidence')
                if authority_is_unverified(child_entry.get('authority')):
                    errors.append(f'{gate_id}: hold->satisfied requires verified authority or not_required')
                if not SATISFACTION_WORDING.search(basis):
                    errors.append(f'{gate_id}: hold->satisfied requires explicit satisfaction basis')

        elif parent_state == 'na' and child_state == 'na':
            parent_reason = str(parent_entry.get('reason', '')).strip()
            child_reason = str(child_entry.get('reason', '')).strip()
            if not child_reason or child_reason == parent_reason:
                warnings.append(f'{gate_id}: parent na must be re-evaluated in child; copied reason detected')

        elif parent_state == 'satisfied' and child_state == 'satisfied':
            relation = scope_relation(parent_entry.get('scope', ''), child_entry.get('scope', ''))
            if relation in {'widened', 'overlap', 'disjoint'}:
                if REEVALUATION_RE.search(basis) and not is_blank(child_entry.get('evidence')):
                    info.append(f'{gate_id}: satisfied scope {relation} re-evaluated')
                else:
                    warnings.append(f'{gate_id}: satisfied scope changed; re-evaluate evidence and authority')
            elif relation == 'unknown':
                warnings.append(f'{gate_id}: satisfied scope relation unknown; re-evaluate evidence and authority')
            elif relation == 'narrowed':
                info.append(f'{gate_id}: satisfied scope narrowed')
            else:
                info.append(f'{gate_id}: satisfied scope preserved')

    info.append('parent aggregate state: ' + aggregate_state(parent.values()))
    info.append('child aggregate state: ' + aggregate_state(child.values()))
    info.append('parent gates checked: ' + str(len(parent)))
    info.append('child gates checked: ' + str(len(child)))
    info.append('inheritance does not grant execution authority')
    return emit(errors, warnings, info)


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
