from pathlib import Path

path = Path('tools/validator/kdsl_packet.py')
text = path.read_text(encoding='utf-8')

replacements = [
    (
        """        elif 'PKT:v1' in text:
            errors.append('PKT:v1 is prohibited')""",
        """        elif re.search(r'^\\s*PKT\\s*:\\s*v1\\s*$', text, re.IGNORECASE | re.MULTILINE):
            errors.append('PKT:v1 is prohibited')""",
    ),
    (
        """        return emit(errors, warnings, info)

    entries, duplicates = parse_top_level(scope)""",
        """        return emit(errors, warnings, info)

    packet_text = '\\n'.join(scope)
    entries, duplicates = parse_top_level(scope)""",
    ),
    (
        """    if 'PKT:v1' in text:
        errors.append('PKT:v1 is prohibited')""",
        """    if re.search(r'^\\s*PKT\\s*:\\s*v1\\s*$', packet_text, re.IGNORECASE | re.MULTILINE):
        errors.append('PKT:v1 is prohibited')""",
    ),
    (
        "gate_ids = validate_sg(blocks.get('SG', {}), task_id, text, errors)",
        "gate_ids = validate_sg(blocks.get('SG', {}), task_id, packet_text, errors)",
    ),
]

for old, new in replacements:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'Packet scope patch match count {count}: {old!r}')
    text = text.replace(old, new)

path.write_text(text, encoding='utf-8')
Path('.github/scripts/fix_packet_scope.py').unlink()
