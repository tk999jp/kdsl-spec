from __future__ import annotations

import re
from dataclasses import dataclass

from kdsl_parser_v2 import DocumentNodeV2, EnvelopeNodeV2, FieldNodeV2

_FIELD_RE = re.compile(r'^([A-Za-z][A-Za-z0-9_-]*)\s*:\s*(.*)$')


@dataclass(frozen=True)
class R1CCompatibilityView:
    """Phase 6C pilot view matching the Phase 1 R1C extraction contract.

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
        document = DocumentNodeV2.parse(text, context='active-document')
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
            scope_lines=tuple(envelope.raw_text.split('\n')),
            entries=entries,
            duplicates=tuple(_duplicate_field_names(envelope.fields)),
        )

    @property
    def values(self) -> dict[str, str]:
        return {key: value for key, value, _ in self.entries}

    @property
    def field_order(self) -> tuple[str, ...]:
        return tuple(key for key, _, _ in self.entries)


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
