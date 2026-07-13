from __future__ import annotations

import re
from dataclasses import dataclass

from kdsl_parser_v2 import DocumentNodeV2, SourceSpanV2

_REQUIRED_FIELDS = (
    'KDSL_RESULT',
    'STATUS',
    'PHASE',
    'S',
    'FILES',
    'WHY',
    'CMD',
    'VERIFY',
    'RT',
    'RISK',
    'NEXT',
    'COMMIT',
)
_BASIS_FIELDS = ('RT', 'VERIFY', 'S')
_AUTHORITY_FIELDS = ('NEXT', 'COMMIT')
_FIELD_HEADER = re.compile(r'^[A-Z_]+:')


@dataclass(frozen=True)
class FullR1FieldNodeV2:
    name: str
    simple_value: str
    continued_value: str
    raw_line: str
    span: SourceSpanV2


@dataclass(frozen=True)
class FullR1CompatibilityView:
    """Source-spanned view matching the current Full R1 checker scans.

    Current Full R1 checkers scan the whole document rather than an envelope
    scope. This view intentionally preserves that behavior. It does not infer
    schemas, defaults, runtime evidence, NEXT authority, or COMMIT authority.
    """

    document: DocumentNodeV2
    fields: tuple[FullR1FieldNodeV2, ...]

    @classmethod
    def from_text(cls, text: str) -> 'FullR1CompatibilityView':
        document = DocumentNodeV2.parse(text, context='active-document')
        fields: list[FullR1FieldNodeV2] = []
        for name in _REQUIRED_FIELDS:
            node = _first_field(document.lines, name)
            if node is not None:
                fields.append(node)
        return cls(document=document, fields=tuple(fields))

    @property
    def has_result_envelope(self) -> bool:
        return self.present('KDSL_RESULT')

    def present(self, name: str) -> bool:
        marker = name + ':'
        return any(line.strip().startswith(marker) for line in self.document.lines)

    def simple_value(self, name: str) -> str:
        node = self.get(name)
        return node.simple_value if node is not None else ''

    def continued_value(self, name: str) -> str:
        node = self.get(name)
        return node.continued_value if node is not None else ''

    def get(self, name: str) -> FullR1FieldNodeV2 | None:
        for field in self.fields:
            if field.name == name:
                return field
        return None

    @property
    def required_presence(self) -> tuple[tuple[str, bool], ...]:
        return tuple((name, self.present(name)) for name in _REQUIRED_FIELDS)

    @property
    def basis_scope_text(self) -> str:
        values: list[str] = []
        for name in _BASIS_FIELDS:
            value = self.simple_value(name)
            if value:
                values.append(name + ': ' + value)
        return '\n'.join(values)

    @property
    def authority_values(self) -> tuple[tuple[str, str], ...]:
        return tuple((name, self.continued_value(name)) for name in _AUTHORITY_FIELDS)


def compare_full_r1_legacy_v2(text: str) -> tuple[list[str], list[str]]:
    """Compare structural inputs consumed by the three current Full R1 checkers."""

    import r1_authority_guard as authority
    import r1_required_blocks as required
    import r1_rt_basis as rt_basis

    view = FullR1CompatibilityView.from_text(text)
    errors: list[str] = []
    info: list[str] = []

    legacy_required = tuple((name, required.present(text, name)) for name in _REQUIRED_FIELDS)
    if legacy_required != view.required_presence:
        errors.append(
            f'required-presence mismatch: legacy={legacy_required!r} v2={view.required_presence!r}'
        )

    legacy_rt_present = rt_basis.has_result_envelope(text)
    legacy_authority_present = authority.has_result_envelope(text)
    if legacy_rt_present != view.has_result_envelope:
        errors.append(
            f'RT envelope-presence mismatch: legacy={legacy_rt_present} v2={view.has_result_envelope}'
        )
    if legacy_authority_present != view.has_result_envelope:
        errors.append(
            'authority envelope-presence mismatch: '
            f'legacy={legacy_authority_present} v2={view.has_result_envelope}'
        )

    for name in _BASIS_FIELDS:
        legacy_value = rt_basis.find_field(text, name)
        view_value = view.simple_value(name)
        if legacy_value != view_value:
            errors.append(
                f'{name} simple-field mismatch: legacy={legacy_value!r} v2={view_value!r}'
            )

    legacy_basis_scope = rt_basis.field_scope_text(text)
    if legacy_basis_scope != view.basis_scope_text:
        errors.append(
            'RT basis-scope mismatch: '
            f'legacy={legacy_basis_scope!r} v2={view.basis_scope_text!r}'
        )

    for name in _AUTHORITY_FIELDS:
        legacy_value = authority.find_field(text, name)
        view_value = view.continued_value(name)
        if legacy_value != view_value:
            errors.append(
                f'{name} continued-field mismatch: legacy={legacy_value!r} v2={view_value!r}'
            )

    if not errors:
        info.append('KDSL_RESULT and required-field presence match')
        info.append('RT/VERIFY/S first-field values and basis scope match')
        info.append('NEXT/COMMIT continuation values match')
        info.append('whole-document legacy scan compatibility retained')
        info.append('Full R1 structural compatibility retained')
    return errors, info


def _first_field(lines: tuple[str, ...], name: str) -> FullR1FieldNodeV2 | None:
    marker = name + ':'
    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith(marker):
            continue
        simple_value = stripped[len(marker):].strip()
        block_lines: list[str] = []
        for following in lines[index + 1:]:
            if not following.strip():
                if block_lines:
                    break
                continue
            if _FIELD_HEADER.match(following.strip()) and not following.startswith((' ', '\t')):
                break
            if following.startswith((' ', '\t', '-', '*')):
                block_lines.append(following.strip())
                continue
            break
        continued = simple_value
        if block_lines:
            continued = (simple_value + '\n' + '\n'.join(block_lines)).strip()
        column = line.find(name) + 1
        return FullR1FieldNodeV2(
            name=name,
            simple_value=simple_value,
            continued_value=continued,
            raw_line=line,
            span=SourceSpanV2(index + 1, max(1, column), index + 1, len(line) + 1),
        )
    return None
