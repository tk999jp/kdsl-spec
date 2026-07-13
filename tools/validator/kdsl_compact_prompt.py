import re
import sys
from pathlib import Path

from kdsl_parser_v2_compact_compat import (
    CompactPromptCompatibilityView,
    compare_compact_legacy_v2,
)

STANDARD_REQUIRED = ('Goal', 'Input', 'Output', 'Guard', 'Check')
STANDARD_CONDITIONAL = ('Role', 'Rules', 'Style')
KANJI_REQUIRED = ('目', '材', '出', '守', '確')
KANJI_CONDITIONAL = ('役', '則', '調')
ALL_BLOCK_KEYS = set(STANDARD_REQUIRED + STANDARD_CONDITIONAL + KANJI_REQUIRED + KANJI_CONDITIONAL)

LIFT_PATTERNS = (
    (
        'implementation',
        re.compile(
            r'実装(?!\s*(?:を)?禁止)|改修(?!\s*(?:を)?禁止)|削除(?!\s*(?:を)?禁止)|コード変更|source\s*change',
            re.IGNORECASE,
        ),
    ),
    ('repository operation', re.compile(r'\brepo\b|repository|\bbranch\b|\bcommit\b|\bpush\b|\bpull request\b', re.IGNORECASE)),
    ('file/API/command change', re.compile(r'file変更|API変更|command変更|ファイル変更|コマンド変更', re.IGNORECASE)),
    ('rollback/revert', re.compile(r'\brollback\b|\brevert\b', re.IGNORECASE)),
    ('runtime verification', re.compile(r'RT:v|実機確認|runtime verification', re.IGNORECASE)),
    ('public release operation', re.compile(r'public履歴|公開済tag|Release Assets|stable release|release操作', re.IGNORECASE)),
    ('data migration', re.compile(r'data migration|データ移行', re.IGNORECASE)),
    ('source-of-truth change', re.compile(r'正本変更|正本を変更', re.IGNORECASE)),
    ('AI coding tool', re.compile(r'AI coding tool|Codex', re.IGNORECASE)),
)

RESTRICTED_PATTERNS = (
    ('single-character relation alias', re.compile(r'(?<![一-龥A-Za-z0-9_])(材|出|守|確|禁|不|実|要)\s*(?:→|=>|:=|=)')),
    ('compressed safety phrase', re.compile(r'材外|出順序|守違反|確済|(?<!事)実追加禁止|不→|禁:|要:=')),
)


def load_text(path):
    if path == '-':
        return sys.stdin.read()
    return Path(path).read_text(encoding='utf-8')


def clean_line(line):
    return line.strip().lstrip('>- ').strip()


def header_value(text, key):
    pattern = re.compile(r'^\s*' + re.escape(key) + r'\s*:\s*([^\s#]+)', re.IGNORECASE | re.MULTILINE)
    match = pattern.search(text)
    return match.group(1) if match else None


def detect_profile(text):
    return bool(re.search(r'^\s*profile\s*:\s*compact-prompt\s*$', text, re.IGNORECASE | re.MULTILINE))


def detect_shorthand(text):
    if re.search(r'^\s*KDSL-CP漢\s*:', text, re.MULTILINE):
        return 'kanji'
    if re.search(r'^\s*KDSL-CP\s*:', text, re.MULTILINE):
        return 'standard'
    return None


def extract_scope(text, shorthand):
    if shorthand:
        marker = 'KDSL-CP漢:' if shorthand == 'kanji' else 'KDSL-CP:'
        lines = text.splitlines()
        start = next((index for index, line in enumerate(lines) if line.strip().startswith(marker)), 0)
        scoped = []
        for index in range(start, len(lines)):
            line = lines[index]
            if index > start and line.strip().startswith('```'):
                break
            if index > start and line.startswith('## '):
                break
            scoped.append(line)
        return '\n'.join(scoped)
    return text


def parse_blocks(scope):
    lines = scope.splitlines()
    positions = []
    key_pattern = re.compile(r'^\s*([A-Za-z][A-Za-z0-9_-]*|[役目材出則守調確])\s*:\s*(.*)$')
    for index, line in enumerate(lines):
        match = key_pattern.match(line)
        if match and match.group(1) in ALL_BLOCK_KEYS:
            positions.append((index, match.group(1), match.group(2).strip()))

    blocks = {}
    duplicates = []
    for position_index, (line_index, key, inline) in enumerate(positions):
        next_index = positions[position_index + 1][0] if position_index + 1 < len(positions) else len(lines)
        following = [clean_line(item) for item in lines[line_index + 1:next_index]]
        content = [item for item in ([inline] if inline else []) + following if item and item != '```']
        if key in blocks:
            duplicates.append(key)
        blocks.setdefault(key, []).extend(content)
    return blocks, duplicates


def find_restricted_aliases(scope):
    findings = []
    for raw_line in scope.splitlines():
        key_match = re.match(r'^\s*([役目材出則守調確])\s*:\s*(.*)$', raw_line)
        content = key_match.group(2) if key_match else raw_line
        for label, pattern in RESTRICTED_PATTERNS:
            match = pattern.search(content)
            if match:
                findings.append(f'{label}: {match.group(0)}')
    return sorted(set(findings))


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


def main(argv):
    path = argv[1] if len(argv) > 1 else '-'
    text = load_text(path)

    errors = []
    warnings = []
    info = []

    view = CompactPromptCompatibilityView.from_text(text)
    parity_errors, _ = compare_compact_legacy_v2(text)
    if parity_errors:
        for item in parity_errors:
            errors.append('CompactPrompt parser parity guard: ' + item)
        return emit(errors, warnings, info)
    info.append('CompactPrompt parser parity guard: pass')

    if not view.is_compact:
        info.append('no CompactPrompt profile or shorthand detected')
        return emit(errors, warnings, info)

    shorthand = view.shorthand
    scope = view.scope
    headers = view.header_values
    mode = headers.get('mode')
    lexicon = headers.get('lexicon')
    safety = headers.get('safety')

    if mode and mode.lower() == 'dense-ja':
        errors.append('mode:dense-ja is not valid; use mode:dense with lexicon:kanji-v1')
    if mode and mode.lower() not in {'readable', 'min', 'dense', 'lock'}:
        errors.append('unknown CompactPrompt mode: ' + mode)
    if safety and safety.lower() not in {'normal', 'lock-critical', 'lock-all'}:
        errors.append('unknown CompactPrompt safety: ' + safety)
    if lexicon and lexicon.lower() not in {'standard', 'kanji-v1'}:
        errors.append('unknown CompactPrompt lexicon: ' + lexicon)

    expected_kanji = shorthand == 'kanji' or (lexicon and lexicon.lower() == 'kanji-v1')
    if shorthand == 'kanji':
        if mode and mode.lower() != 'dense':
            errors.append('KDSL-CP漢 conflicts with explicit mode; expected mode:dense')
        if lexicon and lexicon.lower() != 'kanji-v1':
            errors.append('KDSL-CP漢 conflicts with explicit lexicon; expected lexicon:kanji-v1')

    blocks = view.block_values
    duplicates = list(view.duplicates)
    required = KANJI_REQUIRED if expected_kanji else STANDARD_REQUIRED
    other_keys = STANDARD_REQUIRED + STANDARD_CONDITIONAL if expected_kanji else KANJI_REQUIRED + KANJI_CONDITIONAL

    for key in required:
        if key not in blocks:
            errors.append('required CompactPrompt block missing: ' + key)
        elif not blocks[key]:
            errors.append('required CompactPrompt block is empty: ' + key)

    mixed = sorted(key for key in other_keys if key in blocks)
    if mixed:
        warnings.append('mixed standard/kanji structural keys: ' + ', '.join(mixed))
    if duplicates:
        warnings.append('duplicate CompactPrompt blocks: ' + ', '.join(sorted(set(duplicates))))

    for item in find_restricted_aliases(scope):
        errors.append('restricted free-text alias detected: ' + item)

    lift_hits = []
    for label, pattern in LIFT_PATTERNS:
        if pattern.search(scope):
            lift_hits.append(label)
    if lift_hits:
        errors.append('CP-Lift required: ' + ', '.join(sorted(set(lift_hits))))

    if re.search(r'PKT\s*:\s*v1', scope, re.IGNORECASE):
        errors.append('PKT:v1 is prohibited')

    if 'PACKET_DRAFT:' in scope:
        required_packet_markers = (
            'SCHEMA: kdsl-packet@0.1-draft',
            'STATUS: non-executable',
            'required: true',
            'state: not_normalized',
        )
        missing = [marker for marker in required_packet_markers if marker not in scope]
        if missing:
            errors.append('PACKET_DRAFT non-executable markers missing: ' + ', '.join(missing))
        else:
            info.append('adopted non-executable Packet marker detected')

    info.append('CompactPrompt structural extraction: AST v2 compatibility view')
    info.append('CompactPrompt form: ' + ('kanji-v1' if expected_kanji else 'standard'))
    info.append('required blocks checked: ' + ', '.join(required))
    return emit(errors, warnings, info)


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
