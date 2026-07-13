from __future__ import annotations

import re
from dataclasses import dataclass

from kdsl_parser_v2 import DocumentNodeV2, EnvelopeNodeV2, FieldNodeV2, SourceSpanV2

_MARKER = 'NORMALIZATION_DRAFT'
_MARKER_RE = re.compile(r'^(\s*)NORMALIZATION_DRAFT\s*:\s*$')
_FIELD_RE = re.compile(r'^([A-Za-z][A-Za-z0-9_-]*)\s*:\s*(.*)$')
_TOP_LEVEL_ENVELOPES = {
    'KDSL_RESULT',
    'PACKET_DRAFT',
    'NORMALIZATION_DRAFT',
    'KDSL_PROMPT',
    'KDSL_PROMPT_PREVIEW',
    'STRUCTURAL_ROUND_TRIP_RESULT',
    'R1C_STRUCTURAL_ROUND_TRIP_RESULT',
}
_NESTED_SCALAR_BLOCKS = ('SOURCE', 'TARGET', 'ROUND_TRIP', 'AUTHORITY', 'OUTPUT')
_RECORD_BLOCKS = ('MAP', 'UNRESOLVED', 'LOSS')
_NESTED_LIST_BLOCKS = ('PRESERVE',)


@dataclass(frozen=True)
class NormalizationBlockNodeV2:
    name: str
    inline_value: str
    body_lines: tuple[str, ...]
    raw_text: str
    span: SourceSpanV2
    relative_line: int

    @property
    def legacy_block(self) -> dict[str, object]:
        return {'value': self.inline_value, 'lines': list(self.body_lines)}

    def nested_scalars(self) -> tuple[dict[str, str], list[str]]:
        values: dict[str, str] = {}
        duplicates: list[str] = []
        nonblank = [line for line in self.body_lines if line.strip()]
        if not nonblank:
            return values, duplicates
        child_indent = min(_leading_spaces(line) for line in nonblank)
        for line in self.body_lines:
            if not line.strip() or _leading_spaces(line) != child_indent:
                continue
            match = _FIELD_RE.match(line[child_indent:])
            if not match:
                continue
            key = match.group(1).lower()
            value = _unquote(match.group(2))
            if key in values:
                duplicates.append(key)
            values[key] = value
        return values, duplicates

    def list_records(self) -> list[dict[str, str]]:
        records: list[dict[str, str]] = []
        current: dict[str, str] | None = None
        for line in _dedent_lines(self.body_lines):
            item_match = re.match(
                r'^\s*-\s+([A-Za-z][A-Za-z0-9_-]*)\s*:\s*(.*?)\s*$',
                line,
            )
            if item_match:
                if current is not None:
                    records.append(current)
                current = {item_match.group(1).lower(): _unquote(item_match.group(2))}
                continue
            field_match = re.match(
                r'^\s+([A-Za-z][A-Za-z0-9_-]*)\s*:\s*(.*?)\s*$',
                line,
            )
            if field_match and current is not None:
                current[field_match.group(1).lower()] = _unquote(field_match.group(2))
        if current is not None:
            records.append(current)
        return records

    def nested_lists(self) -> dict[str, list[str]]:
        result: dict[str, list[str]] = {}
        current: str | None = None
        for line in _dedent_lines(self.body_lines):
            key_match = re.match(r'^([A-Za-z][A-Za-z0-9_-]*)\s*:\s*(.*?)\s*$', line)
            if key_match:
                current = key_match.group(1).lower()
                result.setdefault(current, [])
                inline = key_match.group(2).strip()
                if inline and inline != '[]':
                    result[current].append(_unquote(inline))
                continue
            item_match = re.match(r'^\s*-\s*(.*?)\s*$', line)
            if item_match and current is not None:
                result[current].append(_unquote(item_match.group(1)))
        return result

    def multiline(self, key: str) -> str:
        lines = list(self.body_lines)
        if not lines:
            return ''
        base = min((_leading_spaces(line) for line in lines if line.strip()), default=0)
        start: int | None = None
        for index, line in enumerate(lines):
            if _leading_spaces(line) != base:
                continue
            match = _FIELD_RE.match(line[base:])
            if match and match.group(1).lower() == key.lower() and match.group(2).strip() == '|':
                start = index + 1
                break
        if start is None:
            return ''
        collected: list[str] = []
        for line in lines[start:]:
            if not line.strip():
                collected.append('')
                continue
            if _leading_spaces(line) <= base:
                break
            collected.append(line)
        return '\n'.join(_dedent_lines(tuple(collected))).rstrip()


@dataclass(frozen=True)
class NormalizationCompatibilityView:
    """Structural compatibility view for NORMALIZATION_DRAFT.

    This view does not validate normalization semantics, target resolution,
    source digest, authority, output markers, executability, or equivalence.
    """

    document: DocumentNodeV2
    scope_document: DocumentNodeV2 | None
    envelope: EnvelopeNodeV2 | None
    scope_lines: tuple[str, ...]
    entries: tuple[tuple[str, str, int], ...]
    duplicates: tuple[str, ...]
    blocks: tuple[NormalizationBlockNodeV2, ...]

    @classmethod
    def from_text(cls, text: str) -> 'NormalizationCompatibilityView':
        document = DocumentNodeV2.parse(text, context='active-document')
        scope_lines = _extract_legacy_compatible_scope(text)
        if scope_lines is None:
            return cls(document, None, None, (), (), (), ())

        scope_document = DocumentNodeV2.parse('\n'.join(scope_lines), context='raw-envelope')
        envelopes = scope_document.envelopes(_MARKER)
        if not envelopes:
            return cls(document, scope_document, None, scope_lines, (), (), ())

        envelope = envelopes[0]
        blocks = tuple(_block_from_field(envelope, field_node) for field_node in envelope.fields)
        entries = tuple((block.name, block.inline_value, block.relative_line) for block in blocks)
        duplicates = tuple(_duplicate_names(envelope.fields))
        return cls(document, scope_document, envelope, scope_lines, entries, duplicates, blocks)

    @property
    def present(self) -> bool:
        return bool(self.scope_lines)

    @property
    def values(self) -> dict[str, str]:
        return {key: value for key, value, _ in self.entries}

    @property
    def block_map(self) -> dict[str, NormalizationBlockNodeV2]:
        result: dict[str, NormalizationBlockNodeV2] = {}
        for block in self.blocks:
            result[block.name] = block
        return result

    @property
    def legacy_blocks(self) -> dict[str, dict[str, object]]:
        return {key: block.legacy_block for key, block in self.block_map.items()}

    def nested_scalars(self, key: str) -> tuple[dict[str, str], list[str]]:
        block = self.block_map.get(key)
        return block.nested_scalars() if block else ({}, [])

    def list_records(self, key: str) -> list[dict[str, str]]:
        block = self.block_map.get(key)
        return block.list_records() if block else []

    def nested_lists(self, key: str) -> dict[str, list[str]]:
        block = self.block_map.get(key)
        return block.nested_lists() if block else {}

    def multiline(self, key: str, field: str) -> str:
        block = self.block_map.get(key)
        return block.multiline(field) if block else ''


def compare_normalization_legacy_v2(text: str) -> tuple[list[str], list[str]]:
    """Compare every Phase 1 helper output consumed by normalization checker."""

    from kdsl_parser import (
        blocks_from_entries_legacy,
        extract_multiline_legacy,
        extract_scope_lines,
        parse_list_records_legacy,
        parse_nested_lists_legacy,
        parse_nested_scalars_legacy,
        parse_top_level_legacy,
    )

    errors: list[str] = []
    info: list[str] = []
    legacy_scope = extract_scope_lines(text, _MARKER)
    view = NormalizationCompatibilityView.from_text(text)

    legacy_present = legacy_scope is not None
    if legacy_present != view.present:
        errors.append(f'envelope presence mismatch: legacy={legacy_present} v2={view.present}')
        return errors, info

    if legacy_scope is None:
        info.append('NORMALIZATION_DRAFT absent in both parsers')
        return errors, info

    legacy_scope_tuple = tuple(legacy_scope)
    if legacy_scope_tuple != view.scope_lines:
        errors.append('scope line mismatch')

    legacy_entries, legacy_duplicates = parse_top_level_legacy(legacy_scope, _MARKER)
    if tuple(legacy_entries) != view.entries:
        errors.append(f'top-level entry mismatch: legacy={tuple(legacy_entries)!r} v2={view.entries!r}')
    if tuple(legacy_duplicates) != view.duplicates:
        errors.append(
            f'duplicate-field mismatch: legacy={tuple(legacy_duplicates)!r} v2={view.duplicates!r}'
        )

    legacy_blocks = blocks_from_entries_legacy(legacy_scope, legacy_entries)
    if legacy_blocks != view.legacy_blocks:
        errors.append('raw block boundary mismatch')

    for key in _NESTED_SCALAR_BLOCKS:
        legacy_value = parse_nested_scalars_legacy(legacy_blocks.get(key, {}))
        view_value = view.nested_scalars(key)
        if legacy_value != view_value:
            errors.append(f'{key} nested-scalar mismatch: legacy={legacy_value!r} v2={view_value!r}')

    for key in _RECORD_BLOCKS:
        legacy_value = parse_list_records_legacy(legacy_blocks.get(key, {}))
        view_value = view.list_records(key)
        if legacy_value != view_value:
            errors.append(f'{key} record mismatch: legacy={legacy_value!r} v2={view_value!r}')

    for key in _NESTED_LIST_BLOCKS:
        legacy_value = parse_nested_lists_legacy(legacy_blocks.get(key, {}))
        view_value = view.nested_lists(key)
        if legacy_value != view_value:
            errors.append(f'{key} nested-list mismatch: legacy={legacy_value!r} v2={view_value!r}')

    legacy_preview = extract_multiline_legacy(legacy_blocks.get('OUTPUT', {}), 'preview')
    view_preview = view.multiline('OUTPUT', 'preview')
    if legacy_preview != view_preview:
        errors.append(f'OUTPUT.preview multiline mismatch: legacy={legacy_preview!r} v2={view_preview!r}')

    if not errors:
        info.append('NORMALIZATION_DRAFT presence and exact scope match')
        info.append('top-level field order/value/relative-line and duplicates match')
        info.append('raw block boundaries match')
        info.append('nested scalar/record/list/block-scalar helper outputs match')
        info.append('Packet Normalization structural compatibility retained')
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

    top_level = base_indent == 0
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
        indent = _leading_spaces(line)
        if indent < base_indent:
            end_index = index
            break
        if not top_level and indent <= base_indent:
            end_index = index
            break
        if top_level and indent == 0:
            match = _FIELD_RE.match(line)
            if match and match.group(1) in _TOP_LEVEL_ENVELOPES and match.group(1) != _MARKER:
                end_index = index
                break
    return tuple(lines[start_index:end_index])


def _block_from_field(
    envelope: EnvelopeNodeV2,
    field_node: FieldNodeV2,
) -> NormalizationBlockNodeV2:
    raw_lines = tuple(field_node.raw_text.split('\n'))
    first = raw_lines[0] if raw_lines else ''
    match = _FIELD_RE.match(first.lstrip(' '))
    inline = match.group(2).strip() if match else ''
    return NormalizationBlockNodeV2(
        name=field_node.name,
        inline_value=inline,
        body_lines=raw_lines[1:],
        raw_text=field_node.raw_text,
        span=field_node.span,
        relative_line=field_node.span.start_line - envelope.span.start_line,
    )


def _duplicate_names(fields: tuple[FieldNodeV2, ...]) -> list[str]:
    seen: set[str] = set()
    duplicates: list[str] = []
    for field_node in fields:
        if field_node.name in seen:
            duplicates.append(field_node.name)
        seen.add(field_node.name)
    return duplicates


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def _dedent_lines(lines: tuple[str, ...]) -> list[str]:
    nonblank = [_leading_spaces(line) for line in lines if line.strip()]
    if not nonblank:
        return ['' for _ in lines]
    amount = min(nonblank)
    return [line[amount:] if len(line) >= amount else '' for line in lines]


def _leading_spaces(line: str) -> int:
    return len(line) - len(line.lstrip(' '))
