from __future__ import annotations

import copy
import json
from pathlib import Path

from kdsl_binding_evidence_core import FIELD_ORDER, SCHEMA_ID, compute_digest, match_reference, parse_definition, parse_reference
from kdsl_parser_v2 import DocumentNodeV2

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent
EXAMPLE = REPO / 'examples/runtime/binding-evidence-non-executable.example.md'
HEX = 'sha256:' + 'a' * 64


def scope(text: str) -> str:
    lines = text.replace('\r\n', '\n').replace('\r', '\n').split('\n')
    start = next(index for index, line in enumerate(lines) if line.strip() == 'BINDING_EVIDENCE:')
    end = next(index for index in range(start + 1, len(lines)) if lines[index].strip() == '```')
    return '\n'.join(lines[start:end])


def render(model: dict) -> str:
    lines = ['BINDING_EVIDENCE:']
    for key in FIELD_ORDER:
        lines.append(key + ': ' + json.dumps(model[key], ensure_ascii=False, separators=(',', ':')))
    return '\n'.join(lines)


def canonical_sample() -> tuple[str, dict]:
    text = scope(EXAMPLE.read_text(encoding='utf-8'))
    for token in ('record-digest', 'contract-digest', 'k1-digest', 'pf1-digest', 'evaluator-digest'):
        text = text.replace('sha256:<' + token + '>', HEX)
    text = text.replace('commit:<exact-commit>', 'commit:031f11286526e77034da5d803e6b01bf0d61a60a')
    first = parse_definition(text)
    if first.model is None:
        raise RuntimeError('example template did not parse')
    model = first.model
    model['IDENTITY']['digest'] = compute_digest(model)
    return render(model), model


def check(name: str, passed: bool, detail: str = '') -> int:
    print(('PASS: ' if passed else 'FAIL: ') + name + ((' - ' + detail) if detail else ''))
    return 0 if passed else 1


def main() -> int:
    text, model = canonical_sample()
    total = 0
    failed = 0

    result = parse_definition(text)
    total += 1; failed += check('canonical record', not result.errors, '; '.join(result.errors))

    reference_text = json.dumps({'schema': SCHEMA_ID, 'id': model['IDENTITY']['id'], 'revision': model['IDENTITY']['revision'], 'digest': model['IDENTITY']['digest']}, separators=(',', ':'))
    reference, errors = parse_reference(reference_text)
    total += 1; failed += check('compact reference', reference is not None and not errors)
    total += 1; failed += check('exact reference match', reference is not None and not match_reference(reference, model))

    document = DocumentNodeV2.parse(text, context='raw-envelope')
    total += 1; failed += check('shared AST recognition', len(document.envelopes('BINDING_EVIDENCE')) == 1)

    changed = copy.deepcopy(model); changed['IDENTITY']['digest'] = HEX
    total += 1; failed += check('digest mismatch rejected', bool(parse_definition(render(changed)).errors))

    changed = copy.deepcopy(model); changed['BINDING']['executable'] = True; changed['IDENTITY']['digest'] = compute_digest(changed)
    total += 1; failed += check('executable true rejected', bool(parse_definition(render(changed)).errors))

    changed = copy.deepcopy(model); del changed['AUTHORITY']['rails']['commit']; changed['IDENTITY']['digest'] = compute_digest(changed)
    total += 1; failed += check('missing authority rail rejected', bool(parse_definition(render(changed)).errors))

    wrong = json.dumps({'schema': SCHEMA_ID, 'id': 'wrong', 'revision': model['IDENTITY']['revision'], 'digest': model['IDENTITY']['digest']}, separators=(',', ':'))
    wrong_ref, wrong_errors = parse_reference(wrong)
    total += 1; failed += check('reference mismatch rejected', wrong_ref is not None and bool(match_reference(wrong_ref, model)) and not wrong_errors)

    _, noncompact_errors = parse_reference(reference_text + ' ')
    total += 1; failed += check('noncompact reference rejected', bool(noncompact_errors))

    duplicate = parse_definition(text + '\n' + text)
    total += 1; failed += check('duplicate envelope rejected', bool(duplicate.errors))

    print('total: ' + str(total))
    print('failed: ' + str(failed))
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
