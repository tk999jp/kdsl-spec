from __future__ import annotations

import re
from dataclasses import dataclass

from kdsl_parser_v2 import DocumentNodeV2, SourceSpanV2

STANDARD_REQUIRED = ('Goal', 'Input', 'Output', 'Guard', 'Check')
STANDARD_CONDITIONAL = ('Role', 'Rules', 'Style')
KANJI_REQUIRED = ('目', '材', '出', '守', '確')
KANJI_CONDITIONAL = ('役', '則', '調')
ALL_BLOCK_KEYS = set(STANDARD_REQUIRED + STANDARD_CONDITIONAL + KANJI_REQUIRED + KANJI_CONDITIONAL)
BLOCK_RE = re.compile(r'^\s*([A-Za-z][A-Za-z0-9_-]*|[役目材出則守調確])\s*:\s*(.*)$')


@dataclass(frozen=True)
class CompactBlockNodeV2:
    key: str
    content: tuple[str, ...]
    raw_text: str
    span: SourceSpanV2
    relative_line: int


@dataclass(frozen=True)
class CompactPromptCompatibilityView:
    """Bounded CompactPrompt structural compatibility view.

    The view records AST v2 document/header data and reconstructs the current
    CompactPrompt block contract from raw source. It does not decide CP-Lift,
    restricted free-text aliases, Packet authority, or semantic correctness.
    """

    document: DocumentNodeV2
    is_compact: bool
    shorthand: str | None
    scope: str
    headers: tuple[tuple[str, str | None], ...]
    blocks: tuple[CompactBlockNodeV2, ...]
    duplicates: tuple[str, ...]

    @classmethod
    def from_text(cls, text: str) -> 'CompactPromptCompatibilityView':
        document = DocumentNodeV2.parse(text, context='active-document')
        shorthand = detect_shorthand_compatible(text)
        is_compact = bool(shorthand or detect_profile_compatible(text))
        scope = extract_scope_compatible(text, shorthand)
        blocks, duplicates = parse_blocks_typed(scope)
        headers = tuple(
            (key, header_value_compatible(document, text, key))
            for key in ('profile', 'mode', 'safety', 'lexicon')
        )
        return cls(
            document=document,
            is_compact=is_compact,
            shorthand=shorthand,
            scope=scope,
            headers=headers,
            blocks=tuple(blocks),
            duplicates=tuple(duplicates),
        )

    @property
    def header_values(self) -> dict[str, str | None]:
        return dict(self.headers)

    @property
    def block_values(self) -> dict[str, list[str]]:
        result: dict[str, list[str]] = {}
        for block in self.blocks:
            result.setdefault(block.key, []).extend(block.content)
        return result


def compare_compact_legacy_v2(text: str) -> tuple[list[str], list[str]]:
    """Compare current CompactPrompt extraction with the AST v2 view."""

    from kdsl_compact_prompt import (
        detect_profile,
        detect_shorthand,
        extract_scope,
        header_value,
        parse_blocks,
    )

    errors: list[str] = []
    info: list[str] = []
    view = CompactPromptCompatibilityView.from_text(text)

    legacy_shorthand = detect_shorthand(text)
    legacy_compact = bool(legacy_shorthand or detect_profile(text))
    legacy_scope = extract_scope(text, legacy_shorthand)
    legacy_headers = {
        key: header_value(text, key)
        for key in ('profile', 'mode', 'safety', 'lexicon')
    }
    legacy_blocks, legacy_duplicates = parse_blocks(legacy_scope)

    if legacy_compact != view.is_compact:
        errors.append(
            f'compact detection mismatch: legacy={legacy_compact} v2={view.is_compact}'
        )
    if legacy_shorthand != view.shorthand:
        errors.append(
            f'shorthand mismatch: legacy={legacy_shorthand!r} v2={view.shorthand!r}'
        )
    if legacy_scope != view.scope:
        errors.append('scope mismatch')
    if legacy_headers != view.header_values:
        errors.append(
            f'header mismatch: legacy={legacy_headers!r} v2={view.header_values!r}'
        )
    if legacy_blocks != view.block_values:
        errors.append(
            f'block mismatch: legacy={legacy_blocks!r} v2={view.block_values!r}'
        )
    if tuple(legacy_duplicates) != view.duplicates:
        errors.append(
            'duplicate mismatch: '
            f'legacy={tuple(legacy_duplicates)!r} v2={view.duplicates!r}'
        )

    if not errors:
        info.append('CompactPrompt detection and shorthand match')
        info.append('scope matches')
        info.append('profile/mode/safety/lexicon headers match')
        info.append('block order/content and duplicates match')
        info.append('raw structural compatibility retained')
    return errors, info


def detect_profile_compatible(text: str) -> bool:
    return bool(
        re.search(
            r'^\s*profile\s*:\s*compact-prompt\s*$',
            text,
            re.IGNORECASE | re.MULTILINE,
        )
    )


def detect_shorthand_compatible(text: str) -> str | None:
    if re.search(r'^\s*KDSL-CP漢\s*:', text, re.MULTILINE):
        return 'kanji'
    if re.search(r'^\s*KDSL-CP\s*:', text, re.MULTILINE):
        return 'standard'
    return None


def extract_scope_compatible(text: str, shorthand: str | None) -> str:
    if shorthand:
        marker = 'KDSL-CP漢:' if shorthand == 'kanji' else 'KDSL-CP:'
        lines = text.splitlines()
        start = next(
            (index for index, line in enumerate(lines) if line.strip().startswith(marker)),
            0,
        )
        scoped: list[str] = []
        for index in range(start, len(lines)):
            line = lines[index]
            if index > start and line.strip().startswith('```'):
                break
            if index > start and line.startswith('## '):
                break
            scoped.append(line)
        return '\n'.join(scoped)
    return text


def header_value_compatible(
    document: DocumentNodeV2,
    text: str,
    key: str,
) -> str | None:
    headers = document.headers(key)
    if headers:
        raw = headers[0].raw_value.strip()
        return raw.split()[0] if raw else None

    # Phase 6C pilot retains the legacy first-match behavior for headers inside
    # Markdown/fenced fixtures that the active-document AST intentionally does
    # not classify as active header nodes.
    pattern = re.compile(
        r'^\s*' + re.escape(key) + r'\s*:\s*([^\s#]+)',
        re.IGNORECASE | re.MULTILINE,
    )
    match = pattern.search(text)
    return match.group(1) if match else None


def parse_blocks_typed(scope: str) -> tuple[list[CompactBlockNodeV2], list[str]]:
    lines = scope.splitlines()
    positions: list[tuple[int, str, str]] = []
    for index, line in enumerate(lines):
        match = BLOCK_RE.match(line)
        if match and match.group(1) in ALL_BLOCK_KEYS:
            positions.append((index, match.group(1), match.group(2).strip()))

    blocks: list[CompactBlockNodeV2] = []
    duplicates: list[str] = []
    seen: set[str] = set()
    for position_index, (line_index, key, inline) in enumerate(positions):
        next_index = (
            positions[position_index + 1][0]
            if position_index + 1 < len(positions)
            else len(lines)
        )
        raw_lines = lines[line_index:next_index]
        following = [clean_line_compatible(item) for item in lines[line_index + 1:next_index]]
        content = tuple(
            item
            for item in ([inline] if inline else []) + following
            if item and item != '```'
        )
        if key in seen:
            duplicates.append(key)
        seen.add(key)
        blocks.append(
            CompactBlockNodeV2(
                key=key,
                content=content,
                raw_text='\n'.join(raw_lines),
                span=_span_for_scope_lines(line_index + 1, raw_lines),
                relative_line=line_index,
            )
        )
    return blocks, duplicates


def clean_line_compatible(line: str) -> str:
    return line.strip().lstrip('>- ').strip()


def _span_for_scope_lines(start_line: int, lines: list[str]) -> SourceSpanV2:
    if not lines:
        return SourceSpanV2(start_line, 1, start_line, 1)
    end_line = start_line + len(lines) - 1
    return SourceSpanV2(start_line, 1, end_line, len(lines[-1]) + 1)
