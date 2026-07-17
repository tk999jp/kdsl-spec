from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any, Iterable, Sequence

FIELD_RE = re.compile(r'^([A-Za-z][A-Za-z0-9_-]*)\s*:\s*(.*)$')
LIST_ITEM_RE = re.compile(r'^-\s*(.*)$')
FENCE_RE = re.compile(r'^\s*```')

KNOWN_ENVELOPES = {
    'P1L',
    'KDSL_RESULT',
    'PACKET_DRAFT',
    'NORMALIZATION_DRAFT',
    'KDSL_PROMPT',
    'KDSL_PROMPT_PREVIEW',
    'SAFETY_GATES',
    'STRUCTURAL_ROUND_TRIP_RESULT',
    'R1C_STRUCTURAL_ROUND_TRIP_RESULT',
}

HEADER_KEYS = {
    'format',
    'profile',
    'mode',
    'safety',
    'lexicon',
    'envelope',
}


@dataclass(frozen=True)
class SourceSpanV2:
    start_line: int
    start_column: int
    end_line: int
    end_column: int

    def format(self) -> str:
        if self.start_line == self.end_line:
            return f'{self.start_line}:{self.start_column}-{self.end_column}'
        return f'{self.start_line}:{self.start_column}-{self.end_line}:{self.end_column}'


@dataclass(frozen=True)
class DiagnosticV2:
    severity: str
    code: str
    message: str
    primary_span: SourceSpanV2 | None = None
    related_spans: tuple[SourceSpanV2, ...] = ()
    node_path: str = ''
    origin: str = 'parser'

    def format(self) -> str:
        location = f' [{self.primary_span.format()}]' if self.primary_span else ''
        path = f' ({self.node_path})' if self.node_path else ''
        return f'{self.code}: {self.message}{location}{path}'


@dataclass(frozen=True)
class LineRef:
    number: int
    text: str


@dataclass(frozen=True)
class ScalarNode:
    value: str
    raw_text: str
    span: SourceSpanV2
    quote: str | None = None
    kind: str = field(default='scalar', init=False)


@dataclass(frozen=True)
class BlockScalarNode:
    style: str
    value: str
    raw_text: str
    span: SourceSpanV2
    kind: str = field(default='block-scalar', init=False)


@dataclass(frozen=True)
class JsonNode:
    value: Any
    raw_text: str
    span: SourceSpanV2
    kind: str = field(default='json', init=False)


@dataclass(frozen=True)
class EmptyNode:
    raw_text: str
    span: SourceSpanV2
    kind: str = field(default='empty', init=False)


@dataclass(frozen=True)
class InvalidNode:
    reason: str
    raw_text: str
    span: SourceSpanV2
    kind: str = field(default='invalid', init=False)


@dataclass(frozen=True)
class MappingEntryNode:
    key: str
    value: 'ValueNode'
    raw_text: str
    span: SourceSpanV2
    key_span: SourceSpanV2
    value_span: SourceSpanV2


@dataclass(frozen=True)
class MappingNode:
    entries: tuple[MappingEntryNode, ...]
    raw_text: str
    span: SourceSpanV2
    kind: str = field(default='mapping', init=False)

    def get_all(self, key: str) -> list[MappingEntryNode]:
        return [entry for entry in self.entries if entry.key == key]


@dataclass(frozen=True)
class SequenceItemNode:
    value: 'ValueNode'
    raw_text: str
    span: SourceSpanV2


@dataclass(frozen=True)
class SequenceNode:
    items: tuple[SequenceItemNode, ...]
    raw_text: str
    span: SourceSpanV2
    kind: str = field(default='sequence', init=False)


@dataclass(frozen=True)
class RecordSequenceNode:
    items: tuple[SequenceItemNode, ...]
    raw_text: str
    span: SourceSpanV2
    kind: str = field(default='record-sequence', init=False)


ValueNode = (
    ScalarNode
    | BlockScalarNode
    | JsonNode
    | EmptyNode
    | InvalidNode
    | MappingNode
    | SequenceNode
    | RecordSequenceNode
)


@dataclass(frozen=True)
class HeaderNode:
    key: str
    raw_value: str
    normalized_value: str
    raw_text: str
    span: SourceSpanV2
    key_span: SourceSpanV2
    value_span: SourceSpanV2
    kind: str = field(default='header', init=False)


@dataclass(frozen=True)
class FieldNodeV2:
    name: str
    value: ValueNode
    raw_text: str
    span: SourceSpanV2
    name_span: SourceSpanV2
    value_span: SourceSpanV2
    kind: str = field(default='field', init=False)


@dataclass(frozen=True)
class EnvelopeNodeV2:
    marker: str
    fields: tuple[FieldNodeV2, ...]
    raw_text: str
    span: SourceSpanV2
    issues: tuple[DiagnosticV2, ...] = ()
    kind: str = field(default='envelope', init=False)

    def get_all(self, name: str) -> list[FieldNodeV2]:
        return [field_node for field_node in self.fields if field_node.name == name]

    def get(self, name: str) -> FieldNodeV2 | None:
        matches = self.get_all(name)
        return matches[0] if matches else None


@dataclass(frozen=True)
class FenceNode:
    raw_text: str
    span: SourceSpanV2
    closed: bool
    kind: str = field(default='fence', init=False)


@dataclass(frozen=True)
class MarkdownNode:
    raw_text: str
    span: SourceSpanV2
    kind: str = field(default='markdown', init=False)


@dataclass(frozen=True)
class TextNode:
    raw_text: str
    span: SourceSpanV2
    kind: str = field(default='text', init=False)


DocumentChildNode = HeaderNode | EnvelopeNodeV2 | FenceNode | MarkdownNode | TextNode


@dataclass
class DocumentNodeV2:
    source_text: str
    normalized_text: str
    lines: tuple[str, ...]
    children: tuple[DocumentChildNode, ...]
    issues: list[DiagnosticV2] = field(default_factory=list)
    context: str = 'active-document'

    @classmethod
    def parse(cls, text: str, *, context: str = 'active-document') -> 'DocumentNodeV2':
        if context not in {'active-document', 'raw-envelope'}:
            raise ValueError(f'unsupported parser context: {context}')
        normalized = text.replace('\r\n', '\n').replace('\r', '\n')
        lines = tuple(normalized.split('\n'))
        parser = _ParserV2(text, normalized, lines, context)
        return parser.parse()

    def envelopes(self, marker: str | None = None) -> list[EnvelopeNodeV2]:
        result = [child for child in self.children if isinstance(child, EnvelopeNodeV2)]
        if marker is not None:
            result = [child for child in result if child.marker == marker]
        return result

    def headers(self, key: str | None = None) -> list[HeaderNode]:
        result = [child for child in self.children if isinstance(child, HeaderNode)]
        if key is not None:
            result = [child for child in result if child.key == key]
        return result

    @property
    def errors(self) -> list[DiagnosticV2]:
        return [issue for issue in self.issues if issue.severity == 'error']

    @property
    def warnings(self) -> list[DiagnosticV2]:
        return [issue for issue in self.issues if issue.severity == 'warning']

    @property
    def exit_code(self) -> int:
        return 2 if self.errors else (1 if self.warnings else 0)


class _ParserV2:
    def __init__(self, source_text: str, normalized_text: str, lines: tuple[str, ...], context: str):
        self.source_text = source_text
        self.normalized_text = normalized_text
        self.lines = lines
        self.context = context
        self.issues: list[DiagnosticV2] = []

    def parse(self) -> DocumentNodeV2:
        self._check_tabs()
        children: list[DocumentChildNode] = []
        index = 0
        while index < len(self.lines):
            line = self.lines[index]
            if self.context == 'active-document' and FENCE_RE.match(line):
                node, index = self._parse_fence(index)
                children.append(node)
                continue
            if _is_heading(line):
                children.append(
                    MarkdownNode(
                        raw_text=line,
                        span=_span_for_lines(index + 1, [line]),
                    )
                )
                index += 1
                continue
            envelope_match = _envelope_match(line)
            if envelope_match is not None:
                marker = envelope_match.group(1)
                end_index = self._find_envelope_end(index)
                children.append(self._parse_envelope(index, end_index, marker))
                index = end_index
                continue
            header_match = FIELD_RE.match(line) if _leading_spaces(line) == 0 else None
            if header_match and header_match.group(1).lower() in HEADER_KEYS:
                children.append(self._parse_header(index, header_match))
                index += 1
                continue
            start = index
            index += 1
            while index < len(self.lines) and not self._is_child_boundary(index):
                index += 1
            raw_lines = list(self.lines[start:index])
            children.append(
                TextNode(
                    raw_text='\n'.join(raw_lines),
                    span=_span_for_lines(start + 1, raw_lines),
                )
            )

        seen_envelopes: dict[str, SourceSpanV2] = {}
        for child in children:
            if not isinstance(child, EnvelopeNodeV2):
                continue
            previous = seen_envelopes.get(child.marker)
            if previous is not None:
                self.issues.append(
                    DiagnosticV2(
                        'error',
                        'PARSER_DUPLICATE_ENVELOPE',
                        f'duplicate envelope: {child.marker}',
                        child.span,
                        (previous,),
                        f'envelope[{child.marker}]',
                    )
                )
            else:
                seen_envelopes[child.marker] = child.span

        return DocumentNodeV2(
            source_text=self.source_text,
            normalized_text=self.normalized_text,
            lines=self.lines,
            children=tuple(children),
            issues=self.issues,
            context=self.context,
        )

    def _check_tabs(self) -> None:
        for index, line in enumerate(self.lines, start=1):
            prefix = line[: len(line) - len(line.lstrip(' \t'))]
            if '\t' in prefix:
                self.issues.append(
                    DiagnosticV2(
                        'error',
                        'PARSER_TAB_INDENT',
                        'tab indentation is not supported',
                        SourceSpanV2(index, 1, index, len(prefix) + 1),
                        node_path='document',
                    )
                )

    def _is_child_boundary(self, index: int) -> bool:
        line = self.lines[index]
        if self.context == 'active-document' and FENCE_RE.match(line):
            return True
        if _is_heading(line):
            return True
        if _envelope_match(line) is not None:
            return True
        match = FIELD_RE.match(line) if _leading_spaces(line) == 0 else None
        return bool(match and match.group(1).lower() in HEADER_KEYS)

    def _parse_fence(self, start_index: int) -> tuple[FenceNode, int]:
        end_index = start_index + 1
        while end_index < len(self.lines) and not FENCE_RE.match(self.lines[end_index]):
            end_index += 1
        closed = end_index < len(self.lines)
        if closed:
            end_index += 1
        else:
            self.issues.append(
                DiagnosticV2(
                    'error',
                    'PARSER_UNCLOSED_FENCE',
                    'markdown fence is not closed',
                    _span_for_lines(start_index + 1, [self.lines[start_index]]),
                    node_path='document.fence',
                )
            )
        raw_lines = list(self.lines[start_index:end_index])
        return (
            FenceNode(
                raw_text='\n'.join(raw_lines),
                span=_span_for_lines(start_index + 1, raw_lines),
                closed=closed,
            ),
            end_index,
        )

    def _find_envelope_end(self, start_index: int) -> int:
        index = start_index + 1
        while index < len(self.lines):
            line = self.lines[index]
            if self.context == 'active-document' and FENCE_RE.match(line):
                return index
            if _is_heading(line):
                return index
            if _envelope_match(line) is not None:
                return index
            index += 1
        return len(self.lines)

    def _parse_header(self, index: int, match: re.Match[str]) -> HeaderNode:
        line = self.lines[index]
        key = match.group(1)
        raw_value = match.group(2)
        value_start = line.find(':') + 2
        normalized, quote = _unquote(raw_value.strip())
        del quote
        return HeaderNode(
            key=key,
            raw_value=raw_value,
            normalized_value=normalized,
            raw_text=line,
            span=_span_for_lines(index + 1, [line]),
            key_span=SourceSpanV2(index + 1, 1, index + 1, len(key) + 1),
            value_span=SourceSpanV2(index + 1, value_start, index + 1, len(line) + 1),
        )

    def _parse_envelope(self, start_index: int, end_index: int, marker: str) -> EnvelopeNodeV2:
        scope_lines = list(self.lines[start_index:end_index])
        starts: list[tuple[int, re.Match[str]]] = []
        for relative_index, line in enumerate(scope_lines[1:], start=1):
            if not line.strip() or _leading_spaces(line) != 0:
                continue
            match = FIELD_RE.match(line)
            if match:
                starts.append((relative_index, match))
            else:
                self.issues.append(
                    DiagnosticV2(
                        'error',
                        'PARSER_UNEXPECTED_CONTENT',
                        f'unexpected top-level content inside {marker}',
                        _span_for_lines(start_index + relative_index + 1, [line]),
                        node_path=f'envelope[{marker}]',
                    )
                )

        fields: list[FieldNodeV2] = []
        local_issues: list[DiagnosticV2] = []
        seen_fields: dict[str, SourceSpanV2] = {}
        for position, (relative_index, match) in enumerate(starts):
            next_relative = starts[position + 1][0] if position + 1 < len(starts) else len(scope_lines)
            raw_lines = scope_lines[relative_index:next_relative]
            body_lines = [
                LineRef(start_index + line_offset + 1, scope_lines[line_offset])
                for line_offset in range(relative_index + 1, next_relative)
            ]
            name = match.group(1)
            inline = match.group(2)
            absolute_line = start_index + relative_index + 1
            line = scope_lines[relative_index]
            colon = line.find(':')
            name_span = SourceSpanV2(absolute_line, 1, absolute_line, len(name) + 1)
            value_span = _value_span(absolute_line, line, colon, body_lines)
            value = _parse_value(
                inline,
                body_lines,
                value_span,
                self.issues,
                f'envelope[{marker}].field[{name}]',
            )
            field_span = _span_for_lines(absolute_line, raw_lines)
            field_node = FieldNodeV2(
                name=name,
                value=value,
                raw_text='\n'.join(raw_lines),
                span=field_span,
                name_span=name_span,
                value_span=value_span,
            )
            fields.append(field_node)
            previous = seen_fields.get(name)
            if previous is not None:
                issue = DiagnosticV2(
                    'error',
                    'PARSER_DUPLICATE_FIELD',
                    f'duplicate field: {name}',
                    field_span,
                    (previous,),
                    f'envelope[{marker}].field[{name}]',
                )
                self.issues.append(issue)
                local_issues.append(issue)
            else:
                seen_fields[name] = field_span

        return EnvelopeNodeV2(
            marker=marker,
            fields=tuple(fields),
            raw_text='\n'.join(scope_lines),
            span=_span_for_lines(start_index + 1, scope_lines),
            issues=tuple(local_issues),
        )


def _parse_value(
    inline: str,
    body_lines: Sequence[LineRef],
    span: SourceSpanV2,
    issues: list[DiagnosticV2],
    node_path: str,
) -> ValueNode:
    inline_stripped = inline.strip()
    raw_text = _value_raw_text(inline, body_lines)
    dedented = _dedent_refs(body_lines)

    if inline_stripped in {'|', '>'}:
        body_text = '\n'.join(line.text for line in dedented).rstrip()
        value = body_text if inline_stripped == '|' else ' '.join(
            line.text.strip() for line in dedented if line.text.strip()
        )
        return BlockScalarNode(inline_stripped, value, raw_text, span)

    if inline_stripped.startswith(('[', '{')):
        payload_lines = [inline_stripped, *(line.text for line in dedented)]
        payload = '\n'.join(payload_lines).strip()
        try:
            return JsonNode(json.loads(payload), raw_text, span)
        except json.JSONDecodeError as exc:
            issues.append(
                DiagnosticV2(
                    'error',
                    'PARSER_INVALID_JSON',
                    exc.msg,
                    span,
                    node_path=node_path,
                )
            )
            return InvalidNode(exc.msg, raw_text, span)

    if inline_stripped:
        normalized, quote = _unquote(inline_stripped)
        if dedented:
            tail = '\n'.join(line.text for line in dedented).strip()
            if tail:
                normalized = '\n'.join([normalized, tail]).strip()
        return ScalarNode(normalized, raw_text, span, quote)

    nonblank = [line for line in body_lines if line.text.strip()]
    if not nonblank:
        return EmptyNode(raw_text, span)

    base_indent = min(_leading_spaces(line.text) for line in nonblank)
    top = next(line.text[base_indent:] for line in body_lines if line.text.strip())
    if LIST_ITEM_RE.match(top):
        return _parse_sequence(body_lines, base_indent, issues, node_path)
    if FIELD_RE.match(top):
        return _parse_mapping(body_lines, base_indent, issues, node_path)

    normalized = '\n'.join(line.text for line in _dedent_refs(body_lines)).strip()
    return ScalarNode(normalized, raw_text, span)


def _parse_mapping(
    lines: Sequence[LineRef],
    base_indent: int,
    issues: list[DiagnosticV2],
    node_path: str,
) -> MappingNode:
    starts: list[tuple[int, re.Match[str]]] = []
    for index, line_ref in enumerate(lines):
        if not line_ref.text.strip() or _leading_spaces(line_ref.text) != base_indent:
            continue
        match = FIELD_RE.match(line_ref.text[base_indent:])
        if match:
            starts.append((index, match))
        else:
            issues.append(
                DiagnosticV2(
                    'error',
                    'PARSER_UNEXPECTED_CONTENT',
                    'unexpected content in mapping',
                    _span_for_refs([line_ref]),
                    node_path=node_path,
                )
            )

    entries: list[MappingEntryNode] = []
    seen: dict[str, SourceSpanV2] = {}
    for position, (index, match) in enumerate(starts):
        next_index = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        raw_refs = list(lines[index:next_index])
        first = raw_refs[0]
        body = raw_refs[1:]
        key = match.group(1)
        inline = match.group(2)
        colon = first.text.find(':', base_indent)
        key_span = SourceSpanV2(first.number, base_indent + 1, first.number, base_indent + len(key) + 1)
        value_span = _value_span(first.number, first.text, colon, body)
        value = _parse_value(inline, body, value_span, issues, f'{node_path}.mapping[{key}]')
        entry_span = _span_for_refs(raw_refs)
        entry = MappingEntryNode(
            key=key,
            value=value,
            raw_text='\n'.join(item.text for item in raw_refs),
            span=entry_span,
            key_span=key_span,
            value_span=value_span,
        )
        entries.append(entry)
        previous = seen.get(key)
        if previous is not None:
            issues.append(
                DiagnosticV2(
                    'error',
                    'PARSER_DUPLICATE_MAPPING_KEY',
                    f'duplicate mapping key: {key}',
                    entry_span,
                    (previous,),
                    f'{node_path}.mapping[{key}]',
                )
            )
        else:
            seen[key] = entry_span

    return MappingNode(
        entries=tuple(entries),
        raw_text='\n'.join(line.text for line in lines),
        span=_span_for_refs(lines),
    )


def _parse_sequence(
    lines: Sequence[LineRef],
    base_indent: int,
    issues: list[DiagnosticV2],
    node_path: str,
) -> ValueNode:
    starts: list[tuple[int, str]] = []
    for index, line_ref in enumerate(lines):
        if not line_ref.text.strip() or _leading_spaces(line_ref.text) != base_indent:
            continue
        match = LIST_ITEM_RE.match(line_ref.text[base_indent:])
        if match:
            starts.append((index, match.group(1)))
        else:
            issues.append(
                DiagnosticV2(
                    'error',
                    'PARSER_UNEXPECTED_CONTENT',
                    'unexpected content in sequence',
                    _span_for_refs([line_ref]),
                    node_path=node_path,
                )
            )

    items: list[SequenceItemNode] = []
    all_records = True
    for position, (index, payload) in enumerate(starts):
        next_index = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        raw_refs = list(lines[index:next_index])
        first = raw_refs[0]
        continuation = raw_refs[1:]
        payload_match = FIELD_RE.match(payload)
        if payload_match:
            synthetic_first = LineRef(first.number, ' ' * (base_indent + 2) + payload)
            value = _parse_mapping(
                [synthetic_first, *continuation],
                base_indent + 2,
                issues,
                f'{node_path}.item[{position}]',
            )
        elif payload.strip():
            normalized, quote = _unquote(payload.strip())
            if continuation:
                tail = '\n'.join(line.text for line in _dedent_refs(continuation)).strip()
                if tail:
                    normalized = '\n'.join([normalized, tail]).strip()
            value = ScalarNode(normalized, '\n'.join(item.text for item in raw_refs), _span_for_refs(raw_refs), quote)
            all_records = False
        elif continuation:
            child_nonblank = [line for line in continuation if line.text.strip()]
            if child_nonblank:
                child_indent = min(_leading_spaces(line.text) for line in child_nonblank)
                first_child = next(line.text[child_indent:] for line in continuation if line.text.strip())
                if FIELD_RE.match(first_child):
                    value = _parse_mapping(
                        continuation,
                        child_indent,
                        issues,
                        f'{node_path}.item[{position}]',
                    )
                elif LIST_ITEM_RE.match(first_child):
                    value = _parse_sequence(
                        continuation,
                        child_indent,
                        issues,
                        f'{node_path}.item[{position}]',
                    )
                    all_records = False
                else:
                    normalized = '\n'.join(line.text for line in _dedent_refs(continuation)).strip()
                    value = ScalarNode(normalized, '\n'.join(item.text for item in raw_refs), _span_for_refs(raw_refs))
                    all_records = False
            else:
                value = EmptyNode('', _span_for_refs(raw_refs))
                all_records = False
        else:
            value = EmptyNode('', _span_for_refs(raw_refs))
            all_records = False

        items.append(
            SequenceItemNode(
                value=value,
                raw_text='\n'.join(item.text for item in raw_refs),
                span=_span_for_refs(raw_refs),
            )
        )

    cls = RecordSequenceNode if items and all_records else SequenceNode
    return cls(
        items=tuple(items),
        raw_text='\n'.join(line.text for line in lines),
        span=_span_for_refs(lines),
    )


def node_to_data(node: Any) -> Any:
    if isinstance(node, SourceSpanV2):
        return {
            'start_line': node.start_line,
            'start_column': node.start_column,
            'end_line': node.end_line,
            'end_column': node.end_column,
            'formatted': node.format(),
        }
    if isinstance(node, DiagnosticV2):
        return {
            'severity': node.severity,
            'code': node.code,
            'message': node.message,
            'primary_span': node_to_data(node.primary_span) if node.primary_span else None,
            'related_spans': [node_to_data(span) for span in node.related_spans],
            'node_path': node.node_path,
            'origin': node.origin,
        }
    if isinstance(node, DocumentNodeV2):
        return {
            'kind': 'document',
            'context': node.context,
            'source_text': node.source_text,
            'normalized_text': node.normalized_text,
            'children': [node_to_data(child) for child in node.children],
            'issues': [node_to_data(issue) for issue in node.issues],
        }
    if isinstance(node, HeaderNode):
        return {
            'kind': node.kind,
            'key': node.key,
            'raw_value': node.raw_value,
            'normalized_value': node.normalized_value,
            'raw_text': node.raw_text,
            'span': node_to_data(node.span),
            'key_span': node_to_data(node.key_span),
            'value_span': node_to_data(node.value_span),
        }
    if isinstance(node, FieldNodeV2):
        return {
            'kind': node.kind,
            'name': node.name,
            'value': node_to_data(node.value),
            'raw_text': node.raw_text,
            'span': node_to_data(node.span),
            'name_span': node_to_data(node.name_span),
            'value_span': node_to_data(node.value_span),
        }
    if isinstance(node, EnvelopeNodeV2):
        return {
            'kind': node.kind,
            'marker': node.marker,
            'fields': [node_to_data(field_node) for field_node in node.fields],
            'raw_text': node.raw_text,
            'span': node_to_data(node.span),
            'issues': [node_to_data(issue) for issue in node.issues],
        }
    if isinstance(node, MappingNode):
        return {
            'kind': node.kind,
            'entries': [node_to_data(entry) for entry in node.entries],
            'raw_text': node.raw_text,
            'span': node_to_data(node.span),
        }
    if isinstance(node, MappingEntryNode):
        return {
            'kind': 'mapping-entry',
            'key': node.key,
            'value': node_to_data(node.value),
            'raw_text': node.raw_text,
            'span': node_to_data(node.span),
            'key_span': node_to_data(node.key_span),
            'value_span': node_to_data(node.value_span),
        }
    if isinstance(node, (SequenceNode, RecordSequenceNode)):
        return {
            'kind': node.kind,
            'items': [node_to_data(item) for item in node.items],
            'raw_text': node.raw_text,
            'span': node_to_data(node.span),
        }
    if isinstance(node, SequenceItemNode):
        return {
            'kind': 'sequence-item',
            'value': node_to_data(node.value),
            'raw_text': node.raw_text,
            'span': node_to_data(node.span),
        }
    if isinstance(node, ScalarNode):
        return {
            'kind': node.kind,
            'value': node.value,
            'quote': node.quote,
            'raw_text': node.raw_text,
            'span': node_to_data(node.span),
        }
    if isinstance(node, BlockScalarNode):
        return {
            'kind': node.kind,
            'style': node.style,
            'value': node.value,
            'raw_text': node.raw_text,
            'span': node_to_data(node.span),
        }
    if isinstance(node, JsonNode):
        return {
            'kind': node.kind,
            'value': node.value,
            'raw_text': node.raw_text,
            'span': node_to_data(node.span),
        }
    if isinstance(node, EmptyNode):
        return {
            'kind': node.kind,
            'raw_text': node.raw_text,
            'span': node_to_data(node.span),
        }
    if isinstance(node, InvalidNode):
        return {
            'kind': node.kind,
            'reason': node.reason,
            'raw_text': node.raw_text,
            'span': node_to_data(node.span),
        }
    if isinstance(node, FenceNode):
        return {
            'kind': node.kind,
            'raw_text': node.raw_text,
            'span': node_to_data(node.span),
            'closed': node.closed,
        }
    if isinstance(node, (MarkdownNode, TextNode)):
        return {
            'kind': node.kind,
            'raw_text': node.raw_text,
            'span': node_to_data(node.span),
        }
    return node


def collect_value_kinds(document: DocumentNodeV2) -> list[str]:
    kinds: list[str] = []

    def visit(value: ValueNode) -> None:
        kinds.append(value.kind)
        if isinstance(value, MappingNode):
            for entry in value.entries:
                visit(entry.value)
        elif isinstance(value, (SequenceNode, RecordSequenceNode)):
            for item in value.items:
                visit(item.value)

    for envelope in document.envelopes():
        for field_node in envelope.fields:
            visit(field_node.value)
    return kinds


def _is_heading(line: str) -> bool:
    return _leading_spaces(line) == 0 and line.startswith('#')


def _envelope_match(line: str) -> re.Match[str] | None:
    if _leading_spaces(line) != 0:
        return None
    match = FIELD_RE.match(line)
    if match and not match.group(2).strip() and match.group(1) in KNOWN_ENVELOPES:
        return match
    return None


def _leading_spaces(text: str) -> int:
    return len(text) - len(text.lstrip(' '))


def _span_for_lines(start_line: int, lines: Sequence[str]) -> SourceSpanV2:
    if not lines:
        return SourceSpanV2(start_line, 1, start_line, 1)
    end_line = start_line + len(lines) - 1
    return SourceSpanV2(start_line, 1, end_line, len(lines[-1]) + 1)


def _span_for_refs(lines: Sequence[LineRef]) -> SourceSpanV2:
    if not lines:
        return SourceSpanV2(1, 1, 1, 1)
    return SourceSpanV2(lines[0].number, 1, lines[-1].number, len(lines[-1].text) + 1)


def _value_span(line_number: int, line: str, colon: int, body: Sequence[LineRef]) -> SourceSpanV2:
    start_column = max(1, colon + 2)
    nonblank = [line_ref for line_ref in body if line_ref.text.strip()]
    if nonblank:
        last = nonblank[-1]
        return SourceSpanV2(line_number, start_column, last.number, len(last.text) + 1)
    return SourceSpanV2(line_number, start_column, line_number, len(line) + 1)


def _dedent_refs(lines: Sequence[LineRef]) -> list[LineRef]:
    nonblank = [_leading_spaces(line.text) for line in lines if line.text.strip()]
    if not nonblank:
        return [LineRef(line.number, '') for line in lines]
    amount = min(nonblank)
    return [LineRef(line.number, line.text[amount:] if len(line.text) >= amount else '') for line in lines]


def _value_raw_text(inline: str, body: Sequence[LineRef]) -> str:
    parts = [inline]
    parts.extend(line.text for line in body)
    return '\n'.join(parts).rstrip()


def _unquote(value: str) -> tuple[str, str | None]:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1], value[0]
    return value, None
