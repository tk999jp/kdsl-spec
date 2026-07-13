from __future__ import annotations

import re
from dataclasses import dataclass

from kdsl_parser_v2 import DocumentNodeV2, EnvelopeNodeV2, FieldNodeV2

_FIELD_RE = re.compile(r'^([A-Za-z][A-Za-z0-9_-]*)\s*:\s*(.*)$')
_MARKER_RE = re.compile(r'^(\s*)KDSL_RESULT\s*:\s*$')
_TOP_LEVEL_ENVELOPES = {
    'KDSL_RESULT',
    'PACKET_DRAFT',
    'NORMALIZATION_DRAFT',
    'KDSL_PROMPT',
    'KDSL_PROMPT_PREVIEW',
    'STRUCTURAL_ROUND_TRIP_RESULT',
    'R1C_STRUCTURAL_ROUND_TRIP_RESULT',
}


@dataclass(frozen=True)
class R1CCompatibilityView:
    """Phase 6C view matching the Phase 1 R1C extraction contract.

    This view is structural only. It does not validate R1C semantics, authority,
    RT evidence, NEXT, COMMIT, or Safety Gate meaning.
    """

    document: DocumentNodeV2
    envelope: EnvelopeNodeV2
    scope_lines: tuple[str, ...]
    entries: tuple[tuple[str, str, int], ...]
    duplicates: tuple[str, ...]

    @classmethod
    def from_text(cls, text: str) -> 'R1CCompatibilityView | None':
        scope_lines = _extract_legacy_compatible_scope(text)
        if scope_lines is None:
            return None

        # Parse the selected scope as raw envelope input. This intentionally
        # preserves Phase 1 behavior for repository examples whose active R1C
        # envelope is placed inside a Markdown fence, while leaving the AST v2
        # active-document fence policy unchanged.
        document = DocumentNodeV2.parse('\n'.join(scope_lines), context='raw-envelope')
        envelopes = document.envelopes('KDSL_RESULT')
        if not envelopes:
            return None
        envelope = envelopes[0]
        entries = tuple(
            (
                field_node.name,
                _legacy_compatible_value(field_node),
                field_node.span.start_line - envelope.span.start_line,
            )
            for field_node in envelope.fields
        )
        return cls(
            document=document,
            envelope=envelope,
            scope_lines=scope_lines,
            entries=entries,
            duplicates=tuple(_duplicate_field_names(envelope.fields)),
        )

    @property
    def values(self) -> dict[str, str]:
        return {key: value for key, value, _ in self.entries}

    @property
    def field_order(self) -> tuple[str, ...]:
        return tuple(key for key, _, _ in self.entries)


def compare_r1c_legacy_v2(text: str) -> tuple[list[str], list[str]]:
    """Compare Phase 1 extraction and AST v2 compatibility extraction.

    Local imports keep the additive AST v2 module independent from the Phase 1
    implementation while allowing the migration guard to dual-run both paths.
    """

    from kdsl_parser import DocumentNode, parse_top_level_legacy

    errors: list[str] = []
    info: list[str] = []
    legacy_document = DocumentNode.parse(text)
    legacy_envelope = legacy_document.find_envelope('KDSL_RESULT')
    view = R1CCompatibilityView.from_text(text)

    legacy_present = legacy_envelope is not None
    v2_present = view is not None
    if legacy_present != v2_present:
        errors.append(
            f'envelope presence mismatch: legacy={legacy_present} v2={v2_present}'
        )
        return errors, info

    if legacy_envelope is None or view is None:
        info.append('KDSL_RESULT absent in both parsers')
        return errors, info

    legacy_scope = tuple(legacy_envelope.raw_lines)
    legacy_entries, legacy_duplicates = parse_top_level_legacy(
        legacy_scope,
        'KDSL_RESULT',
        combine_multiline_json=True,
    )
    legacy_entries_tuple = tuple(legacy_entries)
    legacy_duplicates_tuple = tuple(legacy_duplicates)

    if legacy_scope != view.scope_lines:
        errors.append('scope line mismatch')
    if legacy_entries_tuple != view.entries:
        errors.append(
            'entry mismatch: '
            f'legacy={legacy_entries_tuple!r} v2={view.entries!r}'
        )
    if legacy_duplicates_tuple != view.duplicates:
        errors.append(
            'duplicate-field mismatch: '
            f'legacy={legacy_duplicates_tuple!r} v2={view.duplicates!r}'
        )

    if not errors:
        info.append('scope lines match')
        info.append('field order/value/relative-line entries match')
        info.append('duplicate field list matches')
        info.append('raw-source compatibility retained')
    return errors, info


def _extract_legacy_compatible_scope(text: str) -> tuple[str, ...] | None:
    normalized = text.replace('\r\n', '\n').replace('\r', '\n')
    lines = tuple(normalized.split('\n'))
    start_index = None
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
            if (
                match
                and match.group(1) in _TOP_LEVEL_ENVELOPES
                and match.group(1) != 'KDSL_RESULT'
            ):
                end_index = index
                break
    return tuple(lines[start_index:end_index])


def _legacy_compatible_value(field_node: FieldNodeV2) -> str:
    """Reproduce Phase 1 FieldNode.value_text(combine_multiline=True).

    The value is derived from AST v2 raw source, not from normalized nodes, so
    quoting, protected wording, JSON text, and block-scalar style remain visible.
    """

    raw_lines = field_node.raw_text.split('\n')
    first = raw_lines[0] if raw_lines else ''
    match = _FIELD_RE.match(first)
    inline = match.group(2).strip() if match else ''
    body_lines = raw_lines[1:]
    dedented = _dedent_lines(body_lines)

    if not body_lines:
        return inline
    if inline == '|':
        return '\n'.join(dedented).rstrip()
    if inline == '>':
        return ' '.join(line.strip() for line in dedented).strip()
    if inline:
        return '\n'.join([inline, *dedented]).strip()
    return '\n'.join(dedented).strip()


def _duplicate_field_names(fields: tuple[FieldNodeV2, ...]) -> list[str]:
    seen: set[str] = set()
    duplicates: list[str] = []
    for field_node in fields:
        if field_node.name in seen:
            duplicates.append(field_node.name)
        seen.add(field_node.name)
    return duplicates


def _dedent_lines(lines: list[str]) -> list[str]:
    nonblank = [_leading_spaces(line) for line in lines if line.strip()]
    if not nonblank:
        return ['' for _ in lines]
    amount = min(nonblank)
    return [line[amount:] if len(line) >= amount else '' for line in lines]


def _leading_spaces(line: str) -> int:
    return len(line) - len(line.lstrip(' '))
