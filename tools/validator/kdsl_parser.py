from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Sequence

TOP_LEVEL_ENVELOPES = {
    'KDSL_RESULT',
    'PACKET_DRAFT',
    'NORMALIZATION_DRAFT',
    'KDSL_PROMPT',
    'KDSL_PROMPT_PREVIEW',
    'STRUCTURAL_ROUND_TRIP_RESULT',
    'R1C_STRUCTURAL_ROUND_TRIP_RESULT',
}

_FIELD_RE = re.compile(r'^([A-Za-z][A-Za-z0-9_-]*)\s*:\s*(.*)$')
_LIST_ITEM_RE = re.compile(r'^-\s*(.*)$')


@dataclass(frozen=True)
class SourceSpan:
    start_line: int
    start_column: int
    end_line: int
    end_column: int

    def format(self) -> str:
        if self.start_line == self.end_line:
            return f'{self.start_line}:{self.start_column}-{self.end_column}'
        return f'{self.start_line}:{self.start_column}-{self.end_line}:{self.end_column}'


@dataclass(frozen=True)
class ParseIssue:
    severity: str
    code: str
    message: str
    span: SourceSpan | None = None

    def format(self) -> str:
        location = f' [{self.span.format()}]' if self.span else ''
        return f'{self.code}: {self.message}{location}'


@dataclass
class DiagnosticBag:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    info: list[str] = field(default_factory=list)

    def add_issue(self, issue: ParseIssue) -> None:
        target = {
            'error': self.errors,
            'warning': self.warnings,
            'info': self.info,
        }.get(issue.severity, self.info)
        target.append(issue.format())

    def error(self, code: str, message: str, span: SourceSpan | None = None) -> None:
        self.add_issue(ParseIssue('error', code, message, span))

    def warning(self, code: str, message: str, span: SourceSpan | None = None) -> None:
        self.add_issue(ParseIssue('warning', code, message, span))

    def note(self, code: str, message: str, span: SourceSpan | None = None) -> None:
        self.add_issue(ParseIssue('info', code, message, span))

    @property
    def exit_code(self) -> int:
        return 2 if self.errors else (1 if self.warnings else 0)

    def emit(self) -> int:
        return emit_legacy(self.errors, self.warnings, self.info)


@dataclass(frozen=True)
class FieldNode:
    name: str
    inline_value: str
    body_lines: tuple[str, ...]
    indent: int
    span: SourceSpan
    raw_lines: tuple[str, ...]

    @property
    def raw_text(self) -> str:
        return '\n'.join(self.raw_lines)

    def value_text(self, *, combine_multiline: bool = True) -> str:
        inline = self.inline_value.strip()
        if not combine_multiline or not self.body_lines:
            return inline
        dedented = dedent_lines(self.body_lines)
        if inline == '|':
            return '\n'.join(dedented).rstrip()
        if inline == '>':
            return ' '.join(line.strip() for line in dedented).strip()
        if inline:
            return '\n'.join([inline, *dedented]).strip()
        return '\n'.join(dedented).strip()

    def json_value(self) -> Any:
        return json.loads(self.value_text(combine_multiline=True))


@dataclass
class EnvelopeNode:
    marker: str
    base_indent: int
    start_line: int
    end_line: int
    raw_lines: tuple[str, ...]
    fields: tuple[FieldNode, ...]
    issues: tuple[ParseIssue, ...] = ()

    @property
    def raw_text(self) -> str:
        return '\n'.join(self.raw_lines)

    @property
    def span(self) -> SourceSpan:
        last = self.raw_lines[-1] if self.raw_lines else ''
        return SourceSpan(self.start_line, 1, self.end_line, max(1, len(last) + 1))

    @property
    def field_order(self) -> list[str]:
        return [field.name for field in self.fields]

    @property
    def duplicates(self) -> list[str]:
        seen: set[str] = set()
        duplicates: list[str] = []
        for field in self.fields:
            if field.name in seen:
                duplicates.append(field.name)
            seen.add(field.name)
        return duplicates

    def get_all(self, name: str) -> list[FieldNode]:
        return [field for field in self.fields if field.name == name]

    def get(self, name: str) -> FieldNode | None:
        matches = self.get_all(name)
        return matches[0] if matches else None

    def values(self, *, combine_multiline: bool = True) -> dict[str, str]:
        result: dict[str, str] = {}
        for field_node in self.fields:
            result[field_node.name] = field_node.value_text(combine_multiline=combine_multiline)
        return result


@dataclass
class DocumentNode:
    text: str
    lines: tuple[str, ...]
    issues: list[ParseIssue] = field(default_factory=list)

    @classmethod
    def parse(cls, text: str) -> 'DocumentNode':
        normalized = text.replace('\r\n', '\n').replace('\r', '\n')
        lines = tuple(normalized.split('\n'))
        document = cls(normalized, lines)
        document._check_tabs()
        return document

    def _check_tabs(self) -> None:
        for index, line in enumerate(self.lines, start=1):
            prefix = line[: len(line) - len(line.lstrip(' \t'))]
            if '\t' in prefix:
                self.issues.append(
                    ParseIssue(
                        'error',
                        'PARSER_TAB_INDENT',
                        'tab indentation is not supported',
                        SourceSpan(index, 1, index, len(prefix) + 1),
                    )
                )

    def find_envelope(self, marker: str) -> EnvelopeNode | None:
        return parse_envelope(self, marker)

    def find_all_envelopes(self, markers: Iterable[str]) -> list[EnvelopeNode]:
        found: list[EnvelopeNode] = []
        for marker in markers:
            envelope = self.find_envelope(marker)
            if envelope is not None:
                found.append(envelope)
        return sorted(found, key=lambda item: item.start_line)


def load_text(path: str) -> str:
    if path == '-':
        return sys.stdin.read()
    return Path(path).read_text(encoding='utf-8')


def emit_legacy(errors: Sequence[str], warnings: Sequence[str], info: Sequence[str]) -> int:
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


def leading_spaces(line: str) -> int:
    return len(line) - len(line.lstrip(' '))


def dedent_lines(lines: Sequence[str]) -> list[str]:
    nonblank = [leading_spaces(line) for line in lines if line.strip()]
    if not nonblank:
        return ['' for _ in lines]
    amount = min(nonblank)
    return [line[amount:] if len(line) >= amount else '' for line in lines]


def _marker_match(line: str, marker: str) -> re.Match[str] | None:
    return re.match(r'^(\s*)' + re.escape(marker) + r'\s*:\s*$', line)


def _is_markdown_boundary(line: str, base_indent: int) -> bool:
    stripped = line.strip()
    if stripped == '```':
        return True
    if leading_spaces(line) <= base_indent and stripped.startswith('#'):
        return True
    return False


def _scope_end(document: DocumentNode, start_index: int, marker: str, base_indent: int) -> int:
    top_level = marker in TOP_LEVEL_ENVELOPES and base_indent == 0
    for index in range(start_index + 1, len(document.lines)):
        line = document.lines[index]
        if _is_markdown_boundary(line, base_indent):
            return index
        if not line.strip():
            continue
        indent = leading_spaces(line)
        if indent < base_indent:
            return index
        if not top_level and indent <= base_indent:
            return index
        if top_level and indent == 0:
            match = _FIELD_RE.match(line)
            if match and match.group(1) in TOP_LEVEL_ENVELOPES and match.group(1) != marker:
                return index
    return len(document.lines)


def _field_indent(scope_lines: Sequence[str], marker: str, base_indent: int) -> int:
    if marker in TOP_LEVEL_ENVELOPES and base_indent == 0:
        return 0
    for line in scope_lines[1:]:
        if not line.strip():
            continue
        indent = leading_spaces(line)
        if indent > base_indent:
            return indent
    return base_indent + 2


def parse_envelope(document: DocumentNode, marker: str) -> EnvelopeNode | None:
    start_index: int | None = None
    base_indent = 0
    for index, line in enumerate(document.lines):
        match = _marker_match(line, marker)
        if match:
            start_index = index
            base_indent = len(match.group(1))
            break
    if start_index is None:
        return None

    end_index = _scope_end(document, start_index, marker, base_indent)
    scope_lines = document.lines[start_index:end_index]
    field_indent = _field_indent(scope_lines, marker, base_indent)
    fields: list[FieldNode] = []
    issues: list[ParseIssue] = []

    starts: list[tuple[int, str, str]] = []
    for relative_index, line in enumerate(scope_lines[1:], start=1):
        if not line.strip() or leading_spaces(line) != field_indent:
            continue
        match = _FIELD_RE.match(line[field_indent:])
        if not match:
            continue
        starts.append((relative_index, match.group(1), match.group(2)))

    for position, (relative_index, name, inline_value) in enumerate(starts):
        next_relative = starts[position + 1][0] if position + 1 < len(starts) else len(scope_lines)
        raw_lines = scope_lines[relative_index:next_relative]
        body_lines = tuple(raw_lines[1:])
        absolute_start = start_index + relative_index + 1
        absolute_end = start_index + next_relative
        last_line = raw_lines[-1] if raw_lines else ''
        span = SourceSpan(
            absolute_start,
            field_indent + 1,
            max(absolute_start, absolute_end),
            max(1, len(last_line) + 1),
        )
        node = FieldNode(
            name=name,
            inline_value=inline_value.strip(),
            body_lines=body_lines,
            indent=field_indent,
            span=span,
            raw_lines=tuple(raw_lines),
        )
        fields.append(node)
        if node.inline_value.startswith(('[', '{')):
            try:
                json.loads(node.value_text(combine_multiline=True))
            except json.JSONDecodeError as exc:
                issues.append(
                    ParseIssue(
                        'error',
                        'PARSER_INVALID_JSON',
                        f'{name}: {exc.msg}',
                        span,
                    )
                )

    seen: dict[str, SourceSpan] = {}
    for field_node in fields:
        if field_node.name in seen:
            issues.append(
                ParseIssue(
                    'error',
                    'PARSER_DUPLICATE_FIELD',
                    f'duplicate field: {field_node.name}',
                    field_node.span,
                )
            )
        else:
            seen[field_node.name] = field_node.span

    return EnvelopeNode(
        marker=marker,
        base_indent=base_indent,
        start_line=start_index + 1,
        end_line=max(start_index + 1, end_index),
        raw_lines=tuple(scope_lines),
        fields=tuple(fields),
        issues=tuple(issues),
    )


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_mapping(field_node: FieldNode) -> tuple[dict[str, str], list[str]]:
    values: dict[str, str] = {}
    duplicates: list[str] = []
    lines = list(field_node.body_lines)
    nonblank = [line for line in lines if line.strip()]
    if not nonblank:
        return values, duplicates
    child_indent = min(leading_spaces(line) for line in nonblank)
    for line in lines:
        if not line.strip() or leading_spaces(line) != child_indent:
            continue
        match = _FIELD_RE.match(line[child_indent:])
        if not match:
            continue
        key = match.group(1).lower()
        value = unquote(match.group(2))
        if key in values:
            duplicates.append(key)
        values[key] = value
    return values, duplicates


def parse_sequence(field_node: FieldNode) -> list[str]:
    inline = field_node.inline_value.strip()
    if inline == '[]':
        return []
    items: list[str] = []
    for line in dedent_lines(field_node.body_lines):
        match = _LIST_ITEM_RE.match(line)
        if not match:
            continue
        payload = match.group(1).strip()
        if not payload or _FIELD_RE.match(payload):
            continue
        items.append(unquote(payload))
    if inline and inline not in {'[]', '|', '>'}:
        items.insert(0, unquote(inline))
    return items


def parse_list_field(field_node: FieldNode, key: str) -> list[str]:
    values: list[str] = []
    pattern = re.compile(r'^\s*-\s*' + re.escape(key) + r'\s*:\s*(.*?)\s*$', re.IGNORECASE)
    for line in dedent_lines(field_node.body_lines):
        match = pattern.match(line)
        if match:
            values.append(unquote(match.group(1)))
    return values


def parse_records(field_node: FieldNode) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for line in dedent_lines(field_node.body_lines):
        item_match = re.match(r'^\s*-\s+([A-Za-z][A-Za-z0-9_-]*)\s*:\s*(.*?)\s*$', line)
        if item_match:
            if current is not None:
                records.append(current)
            current = {item_match.group(1).lower(): unquote(item_match.group(2))}
            continue
        field_match = re.match(r'^\s+([A-Za-z][A-Za-z0-9_-]*)\s*:\s*(.*?)\s*$', line)
        if field_match and current is not None:
            current[field_match.group(1).lower()] = unquote(field_match.group(2))
    if current is not None:
        records.append(current)
    return records


def parse_nested_lists(field_node: FieldNode) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    current: str | None = None
    for line in dedent_lines(field_node.body_lines):
        key_match = re.match(r'^([A-Za-z][A-Za-z0-9_-]*)\s*:\s*(.*?)\s*$', line)
        if key_match:
            current = key_match.group(1).lower()
            result.setdefault(current, [])
            inline = key_match.group(2).strip()
            if inline and inline != '[]':
                result[current].append(unquote(inline))
            continue
        item_match = re.match(r'^\s*-\s*(.*?)\s*$', line)
        if item_match and current is not None:
            result[current].append(unquote(item_match.group(1)))
    return result


def extract_block_scalar(field_node: FieldNode, key: str) -> str:
    lines = list(field_node.body_lines)
    if not lines:
        return ''
    base = min((leading_spaces(line) for line in lines if line.strip()), default=0)
    start: int | None = None
    for index, line in enumerate(lines):
        if leading_spaces(line) != base:
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
        if leading_spaces(line) <= base:
            break
        collected.append(line)
    return '\n'.join(dedent_lines(collected)).rstrip()


def parse_registry_entries(field_node: FieldNode) -> tuple[str | None, list[dict[str, str]]]:
    mapping, _ = parse_mapping(field_node)
    return mapping.get('registry'), parse_records(field_node)


def extract_scope_lines(text: str, marker: str) -> list[str] | None:
    envelope = DocumentNode.parse(text).find_envelope(marker)
    return list(envelope.raw_lines) if envelope else None


def parse_top_level_legacy(
    scope: Sequence[str],
    marker: str,
    *,
    combine_multiline_json: bool = False,
) -> tuple[list[tuple[str, str, int]], list[str]]:
    envelope = DocumentNode.parse('\n'.join(scope)).find_envelope(marker)
    if envelope is None:
        return [], []
    entries: list[tuple[str, str, int]] = []
    for field_node in envelope.fields:
        value = field_node.value_text(combine_multiline=combine_multiline_json)
        entries.append((field_node.name, value, field_node.span.start_line - envelope.start_line))
    return entries, envelope.duplicates


def blocks_from_entries_legacy(
    scope: Sequence[str],
    entries: Sequence[tuple[str, str, int]],
) -> dict[str, dict[str, Any]]:
    blocks: dict[str, dict[str, Any]] = {}
    for position, (key, value, line_index) in enumerate(entries):
        next_index = entries[position + 1][2] if position + 1 < len(entries) else len(scope)
        blocks[key] = {'value': value, 'lines': list(scope[line_index + 1:next_index])}
    return blocks


def field_from_legacy_block(name: str, block: dict[str, Any]) -> FieldNode:
    value = str(block.get('value', ''))
    lines = tuple(str(line) for line in block.get('lines', []))
    raw = (f'{name}: {value}'.rstrip(), *lines)
    return FieldNode(
        name=name,
        inline_value=value,
        body_lines=lines,
        indent=0,
        span=SourceSpan(1, 1, max(1, len(raw)), max(1, len(raw[-1]) + 1)),
        raw_lines=raw,
    )


def parse_nested_scalars_legacy(block: dict[str, Any]) -> tuple[dict[str, str], list[str]]:
    return parse_mapping(field_from_legacy_block('BLOCK', block))


def parse_list_field_legacy(block: dict[str, Any], key: str) -> list[str]:
    return parse_list_field(field_from_legacy_block('BLOCK', block), key)


def parse_sequence_items_legacy(block: dict[str, Any]) -> list[str]:
    return parse_sequence(field_from_legacy_block('BLOCK', block))


def parse_list_records_legacy(block: dict[str, Any]) -> list[dict[str, str]]:
    return parse_records(field_from_legacy_block('BLOCK', block))


def parse_nested_lists_legacy(block: dict[str, Any]) -> dict[str, list[str]]:
    return parse_nested_lists(field_from_legacy_block('BLOCK', block))


def extract_multiline_legacy(block: dict[str, Any], key: str) -> str:
    return extract_block_scalar(field_from_legacy_block('BLOCK', block), key)


def extract_gate_block_legacy(text: str) -> str | None:
    envelope = DocumentNode.parse(text).find_envelope('SAFETY_GATES')
    return envelope.raw_text if envelope else None


def parse_registry_legacy(block_text: str) -> tuple[str | None, list[dict[str, str]]]:
    envelope = DocumentNode.parse(block_text).find_envelope('SAFETY_GATES')
    if envelope is None:
        return None, []
    synthetic = FieldNode(
        name='SAFETY_GATES',
        inline_value='',
        body_lines=tuple(envelope.raw_lines[1:]),
        indent=envelope.base_indent,
        span=envelope.span,
        raw_lines=envelope.raw_lines,
    )
    return parse_registry_entries(synthetic)
