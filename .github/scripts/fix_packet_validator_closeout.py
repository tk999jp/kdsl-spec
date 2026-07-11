from pathlib import Path

path = Path('.github/scripts/apply_packet_validator_closeout.py')
text = path.read_text(encoding='utf-8')

old_arch = '''replace_once(
    'docs/project-status.md',
    'Packet validator first slice:=integration pending',
    'Packet validator first slice:=main統合済み / 69 expectations verified',
)'''
new_arch = '''replace_once(
    'docs/project-status.md',
    """Packet ownership:=v2-draft adopted authoring schema/registries/lint
Packet validator first slice:=integration pending
KDSL-Packet:=non-executable / normalization required""",
    """Packet ownership:=v2-draft adopted authoring schema/registries/lint
Packet validator first slice:=main統合済み / 69 expectations verified
KDSL-Packet:=non-executable / normalization required""",
)'''
count = text.count(old_arch)
if count != 1:
    raise SystemExit(f'architecture replacement block count: {count}')
text = text.replace(old_arch, new_arch)

old_gap = '''replace_once(
    'docs/project-status.md',
    'Packet validator first slice:=integration pending\\n',
    '',
)'''
new_gap = '''replace_once(
    'docs/project-status.md',
    """R1C round-trip semantic proofなし
Packet validator first slice:=integration pending
Packet full YAML/semantic parserなし""",
    """R1C round-trip semantic proofなし
Packet full YAML/semantic parserなし""",
)'''
count = text.count(old_gap)
if count != 1:
    raise SystemExit(f'known-gap replacement block count: {count}')
text = text.replace(old_gap, new_gap)

path.write_text(text, encoding='utf-8')
Path('.github/scripts/fix_packet_validator_closeout.py').unlink()
