from __future__ import annotations

import json
import sys
from collections import defaultdict, deque
from pathlib import Path
from typing import Iterable

from kdsl_safety_gate import (
    REGISTRY,
    aggregate_state,
    authority_is_unverified,
    extract_gate_block,
    is_blank,
    parse_registry,
)
from kdsl_safety_semantics import (
    REEVALUATION_RE,
    RESOLUTION_RE,
    SATISFACTION_RE,
    scope_relation,
)


def load_text(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def emit(errors: list[str], warnings: list[str], info: list[str]) -> int:
    status = 'fail' if errors else ('warn' if warnings else 'pass')
    print('SAFETY_GATE_GRAPH_RESULT:')
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
    print('FULL_SAFETY_PROOF: not_proven')
    print('EXECUTION_AUTHORITY: none')
    return 2 if errors else (1 if warnings else 0)


def state_of(entry: dict[str, str]) -> str:
    return str(entry.get('state', '')).strip().lower()


def transition_basis(entry: dict[str, str]) -> str:
    return ' '.join(str(entry.get(field, '')) for field in ('reason', 'evidence', 'authority'))


def read_node(path: Path, node_id: str, errors: list[str]) -> dict[str, dict[str, str]]:
    if not path.exists():
        errors.append(f'{node_id}: file not found: {path}')
        return {}
    text = load_text(path)
    block = extract_gate_block(text)
    if block is None:
        errors.append(f'{node_id}: no SAFETY_GATES block detected')
        return {}
    registry, entries = parse_registry(block)
    if registry != REGISTRY:
        errors.append(f'{node_id}: unknown or missing Safety Gate registry: {registry}')
    mapped: dict[str, dict[str, str]] = {}
    for entry in entries:
        gate_id = entry.get('id', '').strip()
        if not gate_id:
            continue
        if gate_id in mapped:
            errors.append(f'{node_id}: duplicate Safety Gate ID: {gate_id}')
        mapped[gate_id] = entry
    return mapped


def topological_order(nodes: set[str], edges: list[tuple[str, str]], errors: list[str]) -> list[str]:
    children: dict[str, list[str]] = defaultdict(list)
    indegree = {node: 0 for node in nodes}
    for parent, child in edges:
        if parent not in nodes or child not in nodes:
            errors.append(f'edge references unknown node: {parent}->{child}')
            continue
        children[parent].append(child)
        indegree[child] += 1
    queue = deque(sorted(node for node, degree in indegree.items() if degree == 0))
    order: list[str] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for child in sorted(children[node]):
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    if len(order) != len(nodes):
        errors.append('inheritance graph contains a cycle')
    return order


def aggregate_parent_state(entries: Iterable[dict[str, str]]) -> str:
    states = [state_of(entry) for entry in entries]
    applicable = [state for state in states if state != 'na']
    if 'blocked' in applicable:
        return 'blocked'
    if 'hold' in applicable:
        return 'hold'
    if applicable and all(state == 'satisfied' for state in applicable):
        return 'satisfied'
    if states and all(state == 'na' for state in states):
        return 'na'
    return 'unknown'


def check_transition(
    gate_id: str,
    parent_entries: list[tuple[str, dict[str, str]]],
    child_id: str,
    child_entry: dict[str, str] | None,
    errors: list[str],
    warnings: list[str],
    info: list[str],
) -> None:
    inherited = aggregate_parent_state(entry for _, entry in parent_entries)
    if inherited in {'hold', 'blocked'} and child_entry is None:
        sources = ','.join(parent_id for parent_id, _ in parent_entries)
        errors.append(f'{child_id}/{gate_id}: inherited {inherited} gate missing; parents={sources}')
        return
    if child_entry is None:
        return

    child_state = state_of(child_entry)
    basis = transition_basis(child_entry)
    if inherited == 'blocked':
        if child_state == 'na':
            errors.append(f'{child_id}/{gate_id}: inherited blocked gate cannot transition to na')
        elif child_state in {'hold', 'satisfied'} and not RESOLUTION_RE.search(basis):
            errors.append(f'{child_id}/{gate_id}: blocked->{child_state} requires explicit resolution evidence')
        if child_state == 'satisfied':
            if is_blank(child_entry.get('evidence')) or authority_is_unverified(child_entry.get('authority')):
                errors.append(f'{child_id}/{gate_id}: blocked->satisfied requires evidence and verified authority')
            elif not SATISFACTION_RE.search(basis):
                errors.append(f'{child_id}/{gate_id}: blocked->satisfied requires explicit satisfaction basis')
    elif inherited == 'hold':
        if child_state == 'na':
            errors.append(f'{child_id}/{gate_id}: inherited hold gate cannot transition to na')
        elif child_state == 'satisfied':
            if is_blank(child_entry.get('evidence')):
                errors.append(f'{child_id}/{gate_id}: hold->satisfied requires evidence')
            if authority_is_unverified(child_entry.get('authority')):
                errors.append(f'{child_id}/{gate_id}: hold->satisfied requires verified authority or not_required')
            if not SATISFACTION_RE.search(basis):
                errors.append(f'{child_id}/{gate_id}: hold->satisfied requires explicit satisfaction basis')
    elif inherited == 'na' and child_state == 'na':
        parent_reasons = {str(entry.get('reason', '')).strip() for _, entry in parent_entries}
        child_reason = str(child_entry.get('reason', '')).strip()
        if not child_reason or child_reason in parent_reasons:
            warnings.append(f'{child_id}/{gate_id}: inherited na must be independently re-evaluated')

    if inherited == 'satisfied' and child_state == 'satisfied':
        for parent_id, parent_entry in parent_entries:
            if state_of(parent_entry) != 'satisfied':
                continue
            relation = scope_relation(parent_entry.get('scope', ''), child_entry.get('scope', ''))
            if relation in {'widened', 'overlap', 'disjoint'}:
                if not REEVALUATION_RE.search(basis) or is_blank(child_entry.get('evidence')):
                    errors.append(
                        f'{child_id}/{gate_id}: satisfied scope {relation} from {parent_id}; explicit re-evaluation required'
                    )
                else:
                    info.append(f'{child_id}/{gate_id}: satisfied scope {relation} re-evaluated from {parent_id}')
            elif relation == 'unknown':
                warnings.append(f'{child_id}/{gate_id}: scope relation to {parent_id} is unknown; re-evaluate')
            elif relation == 'narrowed':
                info.append(f'{child_id}/{gate_id}: scope narrowed from {parent_id}')


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print('usage: python kdsl_safety_gate_graph.py <graph.json>')
        return 2
    manifest_path = Path(argv[1]).resolve()
    try:
        data = json.loads(manifest_path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError) as exc:
        return emit([f'graph manifest load failed: {exc}'], [], [])

    errors: list[str] = []
    warnings: list[str] = []
    info: list[str] = []
    raw_nodes = data.get('nodes')
    raw_edges = data.get('edges')
    if not isinstance(raw_nodes, list) or not isinstance(raw_edges, list):
        return emit(['graph manifest requires nodes[] and edges[]'], [], [])

    node_files: dict[str, Path] = {}
    for item in raw_nodes:
        if not isinstance(item, dict):
            errors.append('node entry must be an object')
            continue
        node_id = str(item.get('id', '')).strip()
        file_name = str(item.get('file', '')).strip()
        if not node_id or not file_name:
            errors.append('node requires non-empty id and file')
            continue
        if node_id in node_files:
            errors.append('duplicate graph node id: ' + node_id)
            continue
        node_files[node_id] = (manifest_path.parent / file_name).resolve()

    edges: list[tuple[str, str]] = []
    seen_edges: set[tuple[str, str]] = set()
    for item in raw_edges:
        if not isinstance(item, list) or len(item) != 2:
            errors.append('edge must be [parent, child]')
            continue
        edge = (str(item[0]), str(item[1]))
        if edge in seen_edges:
            warnings.append('duplicate graph edge: ' + '->'.join(edge))
            continue
        seen_edges.add(edge)
        edges.append(edge)

    order = topological_order(set(node_files), edges, errors)
    node_entries = {node_id: read_node(path, node_id, errors) for node_id, path in node_files.items()}
    parents: dict[str, list[str]] = defaultdict(list)
    for parent, child in edges:
        if parent in node_files and child in node_files:
            parents[child].append(parent)

    for child_id in order:
        parent_ids = parents.get(child_id, [])
        if not parent_ids:
            continue
        gate_ids = set()
        for parent_id in parent_ids:
            gate_ids.update(node_entries[parent_id])
        gate_ids.update(node_entries[child_id])
        for gate_id in sorted(gate_ids):
            parent_gate_entries = [
                (parent_id, node_entries[parent_id][gate_id])
                for parent_id in parent_ids
                if gate_id in node_entries[parent_id]
            ]
            if not parent_gate_entries:
                continue
            check_transition(
                gate_id,
                parent_gate_entries,
                child_id,
                node_entries[child_id].get(gate_id),
                errors,
                warnings,
                info,
            )

    info.append('graph nodes: ' + str(len(node_files)))
    info.append('graph edges: ' + str(len(edges)))
    info.append('topological order: ' + ('>'.join(order) if order else 'none'))
    for node_id in order:
        info.append(f'{node_id} aggregate state: {aggregate_state(node_entries[node_id].values())}')
    info.append('multi-generation inheritance does not grant execution authority')
    return emit(errors, warnings, info)


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
