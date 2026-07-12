from pathlib import Path

path = Path('tools/validator/kdsl_packet_property.py')
text = path.read_text(encoding='utf-8')

anchor = '''def gate_line(record: dict[str, str]) -> str:
    return '- ' + ' / '.join(
        [
            'id=' + record.get('id', 'unknown'),
            'state=' + record.get('state', 'unknown'),
            'scope=' + record.get('scope', 'unknown'),
            'reason=' + record.get('reason', 'unknown'),
            'evidence=' + record.get('evidence', 'none'),
            'authority=' + record.get('authority', 'none'),
        ]
    )


'''
replacement = anchor + '''def preview_list_section(preview: str, heading: str) -> list[str]:
    lines = preview.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip() == heading:
            start = index + 1
            break
    if start is None:
        return []
    values: list[str] = []
    for line in lines[start:]:
        stripped = line.strip()
        if not stripped:
            continue
        if not stripped.startswith('- '):
            break
        values.append(stripped[2:])
    return values


'''
if text.count(anchor) != 1:
    raise SystemExit('gate_line anchor count mismatch: ' + str(text.count(anchor)))
text = text.replace(anchor, replacement, 1)

old_verify = '''    if data['verify'] and not ordered_in_text(data['verify'], preview):
        errors.append('VERIFY order changed in preview')
    elif data['verify']:
        checks.append('VERIFY requirement order preserved')
'''
new_verify = '''    verify_section = preview_list_section(preview, '検証要求:')
    if data['verify'] and verify_section[: len(data['verify'])] != data['verify']:
        errors.append('VERIFY order changed in preview')
    elif data['verify']:
        checks.append('VERIFY requirement order preserved in verification section')
'''
if text.count(old_verify) != 1:
    raise SystemExit('VERIFY anchor count mismatch: ' + str(text.count(old_verify)))
text = text.replace(old_verify, new_verify, 1)

old_result = '''    if data['result_schema'] not in preview:
        errors.append('result schema missing from preview')
    else:
        checks.append('result schema request preserved')
'''
new_result = '''    report_section = preview_list_section(preview, '報告形式:')
    if data['result_schema'] not in report_section:
        errors.append('result schema missing from report-format section')
    else:
        checks.append('result schema request preserved in report-format section')
'''
if text.count(old_result) != 1:
    raise SystemExit('result schema anchor count mismatch: ' + str(text.count(old_result)))
text = text.replace(old_result, new_result, 1)

old_dead = '''            if line.strip() not in load_text.__doc__ if False else False:
                pass
'''
if text.count(old_dead) != 1:
    raise SystemExit('dead conditional anchor count mismatch: ' + str(text.count(old_dead)))
text = text.replace(old_dead, '', 1)

path.write_text(text, encoding='utf-8')
