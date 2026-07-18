from pathlib import Path

path = Path(__file__).resolve().parents[2] / 'tools/validator/run_all_samples.py'
text = path.read_text(encoding='utf-8')
old = "    ('binding-evidence', 'run_binding_evidence_samples.py'),\n"
new = old + "    ('binding-evaluator', 'run_binding_evaluator_samples.py'),\n"
if text.count(old) != 1:
    raise RuntimeError('binding-evidence runner anchor mismatch')
path.write_text(text.replace(old, new), encoding='utf-8')

# trigger: 1
