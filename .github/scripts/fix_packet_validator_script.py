from pathlib import Path

path = Path('.github/scripts/apply_packet_validator.py')
text = path.read_text(encoding='utf-8')

old_phase = '''replace_once(
    'README.md',
    """P1:
  Packet validator first slice
  Packet positive/negative sample matrix""",
    """P0:
  PR #13 CI確認 / squash merge / Packet validator closeout

P1:
  Packet normalization round-trip tooling/tests""",
)'''
new_phase = '''replace_once(
    'README.md',
    """P0:
  local mainをorigin/mainへ同期
  49 sample runner再確認

P1:
  Packet validator first slice
  Packet positive/negative sample matrix""",
    """P0:
  PR #13 CI確認 / squash merge / Packet validator closeout

P1:
  Packet normalization round-trip tooling/tests""",
)'''
count = text.count(old_phase)
if count != 1:
    raise SystemExit(f'apply script README phase block match count: {count}')
text = text.replace(old_phase, new_phase)

old_example = '''replace_once(
    'README.md',
    'examples/r1c/r1c-needs-user.example.md\\n```',
    'examples/r1c/r1c-needs-user.example.md\\nexamples/packet/packet-design.example.md\\n```',
)'''
new_example = '''replace_once(
    'README.md',
    'examples/r1c/r1c-blocked.example.md\\nexamples/r1c/r1c-needs-user.example.md\\n```',
    'examples/r1c/r1c-blocked.example.md\\nexamples/r1c/r1c-needs-user.example.md\\nexamples/packet/packet-design.example.md\\n```',
)'''
count = text.count(old_example)
if count != 1:
    raise SystemExit(f'apply script README example block match count: {count}')
text = text.replace(old_example, new_example)

path.write_text(text, encoding='utf-8')
Path('.github/scripts/fix_packet_validator_script.py').unlink()
