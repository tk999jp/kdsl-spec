from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def replace(path: str, old: str, new: str) -> None:
    target = ROOT / path
    text = target.read_text(encoding='utf-8')
    if text.count(old) != 1:
        raise RuntimeError(f'{path}: expected one replacement for {old!r}')
    target.write_text(text.replace(old, new), encoding='utf-8')


def main() -> None:
    replace(
        'tools/validator/kdsl_parser_v2.py',
        "    'PF1',\n",
        "    'PF1',\n    'BINDING_EVIDENCE',\n",
    )
    replace(
        'tools/validator/kdsl_validate.py',
        "    'runtime-control': ['kdsl_runtime_control_compatibility.py'],\n",
        "    'runtime-control': ['kdsl_runtime_control_compatibility.py'],\n    'binding-evidence': ['kdsl_binding_evidence.py'],\n",
    )
    replace(
        'tools/validator/kdsl_validate.py',
        "    'runtime-control': (),\n",
        "    'runtime-control': (),\n    'binding-evidence': (),\n",
    )
    replace(
        'tools/validator/kdsl_validate.py',
        "p1l, p1, p1-contract, k1, pf1, runtime-control, packet, packet-semantic, ",
        "p1l, p1, p1-contract, k1, pf1, runtime-control, binding-evidence, packet, packet-semantic, ",
    )
    replace(
        'tools/validator/kdsl_validate.py',
        "p1-contract|k1|pf1|runtime-control|packet|packet-semantic|packet-p1-normalization",
        "p1-contract|k1|pf1|runtime-control|binding-evidence|packet|packet-semantic|packet-p1-normalization",
    )
    replace(
        'tools/validator/run_all_samples.py',
        "    ('runtime-control', 'run_runtime_control_samples.py'),\n",
        "    ('runtime-control', 'run_runtime_control_samples.py'),\n    ('binding-evidence', 'run_binding_evidence_samples.py'),\n",
    )
    replace(
        'tools/validator/kdsl_runtime_control.py',
        "'evidence_schema': 'deferred_phase9d'",
        "'evidence_schema': 'kdsl-binding-evidence@0.1-draft'",
    )
    replace(
        'examples/runtime/k1-canonical.example.md',
        'evidence_schema: "deferred_phase9d"',
        'evidence_schema: "kdsl-binding-evidence@0.1-draft"',
    )

    sys.path.insert(0, str(ROOT / 'tools/validator'))
    from kdsl_runtime_control import compute_digest, parse_definition

    sample_path = ROOT / 'examples/runtime/k1-canonical.example.md'
    sample = sample_path.read_text(encoding='utf-8')
    parsed = parse_definition(sample, 'K1')
    if parsed.model is None:
        raise RuntimeError('canonical K1 sample did not parse')
    old_digest = parsed.model['IDENTITY']['digest']
    new_digest = compute_digest('K1', parsed.model)
    sample_path.write_text(sample.replace(old_digest, new_digest, 1), encoding='utf-8')


if __name__ == '__main__':
    main()
