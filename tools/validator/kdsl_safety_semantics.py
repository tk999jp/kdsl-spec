from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from kdsl_parser_v2_safety_gate_compat import SafetyGateCompatibilityView

MODEL_ID = 'kdsl-safety-language@0.1-draft'


@dataclass(frozen=True)
class SemanticAtom:
    operator: str
    text: str
    condition: str | None = None
    exception: str | None = None
    weakened: bool = False


@dataclass(frozen=True)
class SemanticRequirement:
    concept: str
    strong_groups: tuple[tuple[re.Pattern[str], ...], ...]
    weak_patterns: tuple[re.Pattern[str], ...] = ()


def _rx(*patterns: str) -> tuple[re.Pattern[str], ...]:
    return tuple(re.compile(pattern, re.IGNORECASE) for pattern in patterns)


REQUIREMENTS: dict[str, tuple[SemanticRequirement, ...]] = {
    'SG-DESIGN': (
        SemanticRequirement(
            'design-approval-boundary',
            (
                _rx(
                    r'未承認.*(?:設計|方針|要件|実装).*(?:禁止|不可)',
                    r'(?:設計|方針|要件).*変更.*(?:承認|approval).*(?:必須|required)',
                    r'design change.*(?:requires|required).*approval',
                    r'承認済.*場合のみ.*(?:変更|実装).*(?:可|可能)',
                ),
            ),
            _rx(
                r'承認.*(?:不要|なくても)',
                r'未承認.*(?:実装|変更).*(?:可|可能)',
                r'design change.*without approval',
                r'(?:禁止|prohibited).*(?:しない|not)',
            ),
        ),
    ),
    'SG-SCOPE': (
        SemanticRequirement(
            'scope-boundary',
            (
                _rx(
                    r'原因未確.*広域修正.*(?:禁止|不可)',
                    r'TGT外変更.*(?:禁止|不可)',
                    r'exact target.*non-target',
                    r'対象/非対象.*(?:明示|固定|確認)',
                ),
            ),
            _rx(
                r'原因未確.*広域修正.*(?:可|可能)',
                r'TGT外変更.*(?:可|可能)',
                r'scope.*(?:unlimited|unbounded)',
                r'対象.*(?:不明|未確認).*(?:変更|実装).*(?:可|可能)',
            ),
        ),
    ),
    'SG-EVIDENCE': (
        SemanticRequirement(
            'evidence-separation',
            (
                _rx(
                    r'未確認.*確認済扱.*(?:禁止|不可)',
                    r'未実行.*実行済扱.*(?:禁止|不可)',
                    r'観測/推論',
                    r'observed.*inferred.*unverified',
                    r'executed evidence separated from inference',
                ),
            ),
            _rx(
                r'未確認.*確認済扱(?!.*(?:禁止|不可))',
                r'未実行.*実行済扱(?!.*(?:禁止|不可))',
                r'推測.*観測扱(?!.*(?:禁止|不可))',
                r'unverified.*(?:verified|confirmed).*(?:allowed|may)',
            ),
        ),
    ),
    'SG-RUNTIME': (
        SemanticRequirement(
            'runtime-claim-marker',
            (_rx(r'RT:v', r'runtime verification', r'対象環境runtime確認', r'実機確認'),),
        ),
        SemanticRequirement(
            'runtime-non-substitution',
            (
                _rx(
                    r'build/diff/lint/test/CI pass != RT:v',
                    r'(?:build|diff|lint|test|CI).*(?:だけ|のみ).*(?:RT:v|実機確認).*(?:扱禁止|ではない)',
                    r'Runtime未確認.*(?:RT:p|RT:u)',
                    r'build.*does not prove.*runtime',
                ),
            ),
            _rx(
                r'(?:build|diff|lint|test|CI).*(?:pass|成功).*(?:(?<![!<>])=|なら|なので).*RT:v',
                r'RT:v.*(?:runtime|実機).*(?:不要|未確認で可)',
            ),
        ),
    ),
    'SG-AUTHORITY': (
        SemanticRequirement(
            'operation-authority-boundary',
            (
                _rx(
                    r'NEXT.*実行許可扱.*(?:禁止|不可)',
                    r'COMMIT.*自動commit許可扱.*(?:禁止|不可)',
                    r'commit/push/release authority',
                    r'propose_only',
                    r'operation-specific authority',
                ),
            ),
            _rx(
                r'NEXT.*実行許可(?!.*(?:禁止|不可))',
                r'COMMIT.*自動commit(?!.*(?:禁止|不可))',
                r'proposal.*(?:grants|is).*permission',
                r'propose_only.*(?:allow|authority)',
            ),
        ),
    ),
    'SG-ROLLBACK': (
        SemanticRequirement(
            'rollback-preflight',
            (
                _rx(
                    r'rollback前.*(?:status|diff|退避)',
                    r'(?:git status|diff).*(?:backup|patch|退避)',
                    r'rollback.*(?:scope|verify|backup)',
                    r'revert.*(?:preflight|backup|verification)',
                ),
            ),
            _rx(
                r'rollback.*(?:確認不要|backup不要|即時実行)',
                r'全体破棄.*(?:可|推奨)',
                r'git clean -fdx.*(?:可|実行)',
            ),
        ),
    ),
    'SG-PUBLIC': (
        SemanticRequirement(
            'public-history-protection',
            (
                _rx(
                    r'public履歴.*(?:改竄|上書|書換).*(?:禁止|不可)',
                    r'公開済tag.*(?:移動|上書).*(?:禁止|不可)',
                    r'Release Assets.*(?:上書|削除).*(?:禁止|不可)',
                    r'public history.*(?:non-rewrite|must not rewrite)',
                ),
            ),
            _rx(
                r'public履歴.*(?:改竄|上書|書換).*(?:可|可能)',
                r'公開済tag.*(?:移動|上書).*(?:可|可能)',
                r'Release Assets.*(?:上書|削除).*(?:可|可能)',
                r'force push.*(?:allowed|permitted)',
            ),
        ),
    ),
    'SG-DATA': (
        SemanticRequirement(
            'data-recovery-boundary',
            (
                _rx(
                    r'data保護',
                    r'(?:backup|バックアップ).*(?:rollback|復旧|restore)',
                    r'data migration.*(?:backup|rollback|recovery)',
                    r'不可逆.*(?:退避|復旧|rollback)',
                ),
            ),
            _rx(
                r'(?:backup|バックアップ).*(?:不要|省略可)',
                r'(?:rollback|復旧).*(?:不要|省略可)',
                r'不可逆.*(?:確認不要|そのまま実行)',
            ),
        ),
    ),
    'SG-KDSL-DP': (
        SemanticRequirement(
            'kdsl-dp-direct-execution-prohibition',
            (_rx(r'KDSL-DP直接実行禁止', r'KDSL-DP.*直接.*(?:禁止|不可)'),),
            _rx(r'KDSL-DP.*直接実行.*(?:可|可能)', r'KDSL-DP.*(?:そのまま|directly).*(?:execute|実行可)'),
        ),
        SemanticRequirement(
            'p1-normalization-required',
            (_rx(r'P1/P1L正規化必須', r'P1/P1L.*正規化.*(?:必須|required)'),),
            _rx(r'P1/P1L.*(?:不要|省略可)', r'normalization.*(?:optional|not required)'),
        ),
    ),
    'SG-STOP': (
        SemanticRequirement(
            'stop-condition-boundary',
            (
                _rx(
                    r'停止条件',
                    r'stop condition',
                    r'(?:mismatch|不一致).*(?:停止|blocked|stop)',
                ),
            ),
            _rx(
                r'停止条件.*(?:無視|解除不要)',
                r'(?:mismatch|不一致).*(?:継続可|continue)',
            ),
        ),
    ),
}

WEAKENING_MARKERS = _rx(
    r'禁止しない',
    r'必須ではない',
    r'不要',
    r'省略可',
    r'なくても(?:よい|可|可能)',
    r'not prohibited',
    r'not required',
    r'without approval',
    r'may proceed without',
)

OPERATOR_PATTERNS = (
    ('prohibit', re.compile(r'禁止|不可|must not|prohibited|forbid', re.IGNORECASE)),
    ('require', re.compile(r'必須|必要|required|must|only if|場合のみ', re.IGNORECASE)),
    ('allow', re.compile(r'許可|可能|可\b|allowed|permitted|may|can', re.IGNORECASE)),
    ('claim', re.compile(r'確認済|実行済|成功|verified|executed|success', re.IGNORECASE)),
)
CONDITION_RE = re.compile(r'(.+?)(?:場合|時|なら|if|when)', re.IGNORECASE)
EXCEPTION_RE = re.compile(r'(?:除く|例外|unless|except|only if|場合のみ)', re.IGNORECASE)

WILDCARDS = {'*', 'all', 'global', 'repository-wide', 'repo-wide', '全体', '全域', '全ファイル'}
SCOPE_SPLIT_RE = re.compile(r'\s*(?:,|\||\+|\band\b|および|ならびに|\sと\s)\s*', re.IGNORECASE)
SCOPE_PREFIX_RE = re.compile(r'^(?:exact|target|scope|file|path|対象|範囲)\s*[:=]?\s*', re.IGNORECASE)
REEVALUATION_RE = re.compile(r're-?evaluat|再評価|再確認|scope.*verified|範囲.*確認', re.IGNORECASE)
RESOLUTION_RE = re.compile(r'resolved|resolution|解消|解除|原因除去|再確認|再評価|充足確認|verified', re.IGNORECASE)
SATISFACTION_RE = re.compile(r'confirmed|verified|確認済|充足|resolved|解消|根拠|再評価', re.IGNORECASE)


def load_text(path: str) -> str:
    if path == '-':
        return sys.stdin.read()
    return Path(path).read_text(encoding='utf-8')


def split_statements(text: str) -> list[str]:
    statements: list[str] = []
    for line in text.splitlines():
        line = re.sub(r'^\s*[-*]\s*', '', line).strip()
        if not line:
            continue
        for part in re.split(r'[。；;]+', line):
            part = part.strip()
            if part:
                statements.append(part)
    return statements


def analyze_atoms(text: str) -> list[SemanticAtom]:
    atoms: list[SemanticAtom] = []
    for statement in split_statements(text):
        operator = 'other'
        for candidate, pattern in OPERATOR_PATTERNS:
            if pattern.search(statement):
                operator = candidate
                break
        condition_match = CONDITION_RE.search(statement)
        condition = condition_match.group(1).strip() if condition_match else None
        exception = statement if EXCEPTION_RE.search(statement) else None
        weakened = any(pattern.search(statement) for pattern in WEAKENING_MARKERS)
        atoms.append(SemanticAtom(operator, statement, condition, exception, weakened))
    return atoms


def gate_ids_from_text(text: str) -> list[str]:
    view = SafetyGateCompatibilityView.from_text(text)
    return [entry.get('id', '').strip() for entry in view.entry_dicts if entry.get('id')]


def check_semantics(text: str, gate_ids: Iterable[str]) -> tuple[list[str], list[str], list[str], list[SemanticAtom]]:
    errors: list[str] = []
    warnings: list[str] = []
    info: list[str] = []
    atoms = analyze_atoms(text)
    for gate_id in sorted(set(gate_ids)):
        requirements = REQUIREMENTS.get(gate_id, ())
        for requirement in requirements:
            weak_hits = [pattern.pattern for pattern in requirement.weak_patterns if pattern.search(text)]
            if weak_hits:
                errors.append(f'{gate_id}: protected concept weakened: {requirement.concept}')
                continue
            missing_groups = [
                index
                for index, group in enumerate(requirement.strong_groups, start=1)
                if not any(pattern.search(text) for pattern in group)
            ]
            if missing_groups:
                errors.append(
                    f'{gate_id}: bounded semantic concept missing: {requirement.concept} groups={missing_groups}'
                )
            else:
                info.append(f'{gate_id}: semantic concept preserved: {requirement.concept}')
    weakened_atoms = [atom.text for atom in atoms if atom.weakened]
    if weakened_atoms:
        warnings.append('bounded weakening markers observed: ' + ' | '.join(weakened_atoms[:3]))
    info.append('semantic model: ' + MODEL_ID)
    info.append('semantic atoms: ' + str(len(atoms)))
    info.append('semantic analysis is bounded and does not prove full equivalence')
    return errors, warnings, info, atoms


def normalize_scope(scope: str) -> tuple[bool, frozenset[str]]:
    raw = str(scope or '').strip().lower()
    if not raw:
        return False, frozenset()
    if raw in WILDCARDS or any(token in raw for token in ('repository-wide', 'repo-wide', '全ファイル', '全体', '全域')):
        return True, frozenset()
    parts = [part.strip() for part in SCOPE_SPLIT_RE.split(raw) if part.strip()]
    normalized: set[str] = set()
    for part in parts:
        part = SCOPE_PREFIX_RE.sub('', part).strip().strip('"\'`')
        part = re.sub(r'\s+', ' ', part)
        if part:
            normalized.add(part)
    return False, frozenset(normalized)


def scope_relation(parent_scope: str, child_scope: str) -> str:
    parent_all, parent = normalize_scope(parent_scope)
    child_all, child = normalize_scope(child_scope)
    if parent_all and child_all:
        return 'equal'
    if parent_all and child:
        return 'narrowed'
    if child_all and parent:
        return 'widened'
    if not parent or not child:
        return 'unknown'
    if parent == child:
        return 'equal'
    if child < parent:
        return 'narrowed'
    if parent < child:
        return 'widened'
    if parent.isdisjoint(child):
        return 'disjoint'
    return 'overlap'


def emit(errors: list[str], warnings: list[str], info: list[str]) -> int:
    status = 'fail' if errors else ('warn' if warnings else 'pass')
    print('SAFETY_SEMANTICS_RESULT:')
    print('STATUS: ' + status)
    print('MODEL: ' + MODEL_ID)
    print('ERRORS:')
    for item in errors or ['none']:
        print('  - ' + item)
    print('WARNINGS:')
    for item in warnings or ['none']:
        print('  - ' + item)
    print('INFO:')
    for item in info or ['none']:
        print('  - ' + item)
    print('FULL_SEMANTIC_EQUIVALENCE: not_proven')
    print('EXECUTION_AUTHORITY: none')
    return 2 if errors else (1 if warnings else 0)


def main(argv: list[str]) -> int:
    path = argv[1] if len(argv) > 1 else '-'
    text = load_text(path)
    gate_ids = gate_ids_from_text(text)
    if not gate_ids:
        return emit([], [], ['no SAFETY_GATES entries detected'])
    errors, warnings, info, _ = check_semantics(text, gate_ids)
    return emit(errors, warnings, info)


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
