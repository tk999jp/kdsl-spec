from __future__ import annotations

import re
from dataclasses import dataclass

from kdsl_parser_v2 import (
    DocumentNodeV2,
    EnvelopeNodeV2,
    FieldNodeV2,
    MappingNode,
    RecordSequenceNode,
    ScalarNode,
    SourceSpanV2,
)

_MARKER_RE = re.compile(r'^(\s*)SAFETY_GATES\s*:\s*$')
_FIELD_RE = re.compile(r'^([A-Za-z][A-Za-z0-9_-]*)\s*:\s*(.*?)\s*$')


@dataclass(frozen=True)
class SafetyGateEntryNodeV2:
    values: tuple[tuple[str, str], ...]
    raw_text: str
    span: SourceSpanV2
    relative_line: int

    @property
    def field_order(self) -> tuple[str, ...]:
        return tuple(key for key, _ in self.values)

    @property
    def as_dict(self) -> dict[str, str]:
        result: dict[str, str] = {}
        for key, value in self.values:
            result[key] = value
        return result


@dataclass(frozen=True)
class SafetyGateCompatibilityView:
    """Bounded Safety Gate structural compatibility view.

    The view preserves the exact Phase 1 selected scope while parsing a local,
    dedented copy through AST v2. It does not decide registry validity, known IDs,
    states, inheritance, protected wording, composition, authority, or safety.
    """

    document: DocumentNodeV2
    scope_document: DocumentNodeV2 | None
    envelope: EnvelopeNodeV2 | None
    scope_lines: tuple[str, ...]
    registry: str | None
    entries: tuple[SafetyGateEntryNodeV2, ...]

    @classmethod
    def from_text(cls, text: str) -> 'SafetyGateCompatibilityView':
        document = DocumentNodeV2.parse(text, context='active-document')
        scope_lines = _extract_legacy_compatible_scope(text)
        if scope_lines is None:
            return cls(document, None, None, (), None, ())

        parse_text = _dedent_scope_for_ast(scope_lines)
        scope_document = DocumentNodeV2.parse(parse_text, context='raw-envelope')
        envelopes = scope_document.envelopes('SAFETY_GATES')
        if not envelopes:
            return cls(document, scope_document, None, scope_lines, None, ())

        envelope = envelopes[0]
        registry = _registry_from_envelope(envelope)
        entries = tuple(_entries_from_envelope(envelope))
        return cls(document, scope_document, envelope, scope_lines, registry, entries)

    @property
    def present(self) -> bool:
        return bool(self.scope_lines)

    @property
    def block_text(self) -> str | None:
        return '\n'.join(self.scope_lines) if self.scope_lines else None

    @property
    def entry_dicts(self) -> list[dict[str, str]]:
        return [entry.as_dict for entry in self.entries]

    @property
    def entry_field_orders(self) -> tuple[tuple[str, ...], ...]:
        return tuple(entry.field_order for entry in self.entries)


def compare_safety_gate_legacy_v2(text: str) -> tuple[list[str], list[str]]:
    """Compare Phase 1 Safety Gate extraction with the AST v2 view."""

    from kdsl_parser import extract_gate_block_legacy, parse_registry_legacy

    errors: list[str] = []
    info: list[str] = []
    legacy_block = extract_gate_block_legacy(text)
    view = SafetyGateCompatibilityView.from_text(text)

    legacy_present = legacy_block is not None
    if legacy_present != view.present:
        errors.append(
            f'block presence mismatch: legacy={legacy_present} v2={view.present}'
        )
        return errors, info

    if legacy_block is None:
        info.append('SAFETY_GATES absent in both parsers')
        return errors, info

    if legacy_block != view.block_text:
        errors.append('scope block mismatch')

    legacy_registry, legacy_entries = parse_registry_legacy(legacy_block)
    if legacy_registry != view.registry:
        errors.append(
            f'registry mismatch: legacy={legacy_registry!r} v2={view.registry!r}'
        )

    legacy_entry_items = tuple(tuple(entry.items()) for entry in legacy_entries)
    view_entry_items = tuple(tuple(entry.as_dict.items()) for entry in view.entries)
    if legacy_entry_items != view_entry_items:
        errors.append(
            f'entry mismatch: legacy={legacy_entry_items!r} v2={view_entry_items!r}'
        )

    legacy_orders = tuple(tuple(entry.keys()) for entry in legacy_entries)
    if legacy_orders != view.entry_field_orders:
        errors.append(
            f'entry field-order mismatch: legacy={legacy_orders!r} '
            f'v2={view.entry_field_orders!r}'
        )

    if not errors:
        info.append('SAFETY_GATES presence and exact scope match')
        info.append('registry matches')
        info.append('entry order/field order/value match')
        info.append('raw structural compatibility retained')
    return errors, info


def _extract_legacy_compatible_scope(text: str) -> tuple[str, ...] | None:
    normalized = text.replace('\r\n', '\n').replace('\r', '\n')
    lines = tuple(normalized.split('\n'))
    start_index: int | None = None
    base_indent = 0
    for index, line in enumerate(lines):
        match = _MARKER_RE.match(line)
        if match:
            start_index = index
            base_indent = len(match.group(1))
            break
    if start_index is None:
        return None

    end_index = len(lines)
    for index in range(start_index + 1, len(lines)):
        line = lines[index]
        stripped = line.strip()
        if stripped == '```':
            end_index = index
            break
        if _leading_spaces(line) <= base_indent and stripped.startswith('#'):
            end_index = index
            break
        if not stripped:
            continue
        if _leading_spaces(line) <= base_indent:
            end_index = index
            break
    return tuple(lines[start_index:end_index])


def _dedent_scope_for_ast(scope_lines: tuple[str, ...]) -> str:
    if not scope_lines:
        return ''
    marker = scope_lines[0]
    marker_indent = _leading_spaces(marker)
    normalized_marker = marker[marker_indent:]
    body = list(scope_lines[1:])
    nonblank = [_leading_spaces(line) for line in body if line.strip()]
    body_indent = min(nonblank) if nonblank else marker_indent + 2

    normalized_body: list[str] = []
    for line in body:
        if not line.strip():
            normalized_body.append('')
        elif len(line) >= body_indent:
            normalized_body.append(line[body_indent:])
        else:
            normalized_body.append(line.lstrip(' '))
    return '\n'.join([normalized_marker, *normalized_body])


def _registry_from_envelope(envelope: EnvelopeNodeV2) -> str | None:
    fields = envelope.get_all('registry')
    if not fields:
        return None
    return _legacy_inline_value(fields[-1])


def _entries_from_envelope(envelope: EnvelopeNodeV2) -> list[SafetyGateEntryNodeV2]:
    result: list[SafetyGateEntryNodeV2] = []
    for field_node in envelope.get_all('entries'):
        value = field_node.value
        if not isinstance(value, RecordSequenceNode):
            continue
        for item in value.items:
            if not isinstance(item.value, MappingNode):
                continue
            values: list[tuple[str, str]] = []
            for mapping_entry in item.value.entries:
                key = mapping_entry.key.lower()
                values.append((key, _legacy_mapping_value(mapping_entry.raw_text)))
            result.append(
                SafetyGateEntryNodeV2(
                    values=tuple(values),
                    raw_text=item.raw_text,
                    span=item.span,
                    relative_line=item.span.start_line - envelope.span.start_line,
                )
            )
    return result


def _legacy_inline_value(field_node: FieldNodeV2) -> str:
    first = field_node.raw_text.splitlines()[0] if field_node.raw_text else ''
    match = _FIELD_RE.match(first.strip())
    return _unquote(match.group(2)) if match else ''


def _legacy_mapping_value(raw_text: str) -> str:
    first = raw_text.splitlines()[0] if raw_text else ''
    match = _FIELD_RE.match(first.strip())
    return _unquote(match.group(2)) if match else ''


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def _leading_spaces(line: str) -> int:
    return len(line) - len(line.lstrip(' '))
