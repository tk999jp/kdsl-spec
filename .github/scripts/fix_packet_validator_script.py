from pathlib import Path

path = Path('.github/scripts/apply_packet_validator.py')
text = path.read_text(encoding='utf-8')
old = '''replace_once(
    'README.md',
    """P1:
  Packet validator first slice
  Packet positive/negative sample matrix""",
    """P0:
  PR #13 CI確認 / squash merge / Packet validator closeout

P1:
  Packet normalization round-trip tooling/tests""",
)'''
new = '''replace_once(
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
count = text.count(old)
if count != 1:
    raise SystemExit(f'apply script README phase block match count: {count}')
path.write_text(text.replace(old, new), encoding='utf-8')
Path('.github/scripts/fix_packet_validator_script.py').unlink()
