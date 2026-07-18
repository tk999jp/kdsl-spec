from pathlib import Path


def replace_once(path, old, new):
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{path}: expected one match, found {count}')
    p.write_text(text.replace(old, new, 1), encoding='utf-8')

replace_once('spec/runtime/kdsl-binding-evidence-schema.md', 'status: v2-draft candidate\ncanonical: v2-draft candidate', 'status: v2-draft adopted\ncanonical: v2-draft')
replace_once('spec/lint/kdsl-binding-evidence-lint.md', 'status: v2-draft candidate', 'status: v2-draft adopted')
replace_once('docs/reviews/kdsl-phase9d-binding-evidence-schema.md', 'status: schema-candidate', 'status: schema-adoption-candidate')
