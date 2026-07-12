from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence


@dataclass(frozen=True)
class SuiteCase:
    name: str
    command: tuple[str, ...]
    expected: int
    stdout_contains: tuple[str, ...] = ()
    stdout_not_contains: tuple[str, ...] = ()


@dataclass
class SuiteResult:
    name: str
    total: int = 0
    failed: int = 0
    failures: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.failed == 0


class SuiteRunner:
    def __init__(self, root: Path, repo_root: Path, name: str):
        self.root = root
        self.repo_root = repo_root
        self.name = name

    def resolve_command(self, command: Sequence[str]) -> list[str]:
        script = self.root / command[0]
        args: list[str] = []
        for item in command[1:]:
            if item.startswith('samples/'):
                args.append(str(self.root / item))
            elif item.startswith('examples/'):
                args.append(str(self.repo_root / item))
            else:
                args.append(item)
        return [sys.executable, str(script), *args]

    def run_case(self, case: SuiteCase) -> tuple[bool, subprocess.CompletedProcess[str]]:
        proc = subprocess.run(
            self.resolve_command(case.command),
            cwd=str(self.repo_root),
            text=True,
            capture_output=True,
        )
        ok = (
            proc.returncode == case.expected
            and all(value in proc.stdout for value in case.stdout_contains)
            and all(value not in proc.stdout for value in case.stdout_not_contains)
        )
        return ok, proc

    def run(self, cases: Sequence[SuiteCase]) -> SuiteResult:
        result = SuiteResult(self.name, total=len(cases))
        for case in cases:
            ok, proc = self.run_case(case)
            status = 'PASS' if ok else 'FAIL'
            print(f'{status}: {case.name}')
            if not ok:
                result.failed += 1
                result.failures.append(case.name)
                print('  command: ' + ' '.join(case.command))
                print(f'  expected: {case.expected}')
                print(f'  actual: {proc.returncode}')
                missing = [value for value in case.stdout_contains if value not in proc.stdout]
                prohibited = [value for value in case.stdout_not_contains if value in proc.stdout]
                if missing:
                    print('  missing stdout: ' + repr(missing))
                if prohibited:
                    print('  prohibited stdout: ' + repr(prohibited))
                if proc.stdout:
                    print('  stdout:')
                    for line in proc.stdout.rstrip().splitlines():
                        print('    ' + line)
                if proc.stderr:
                    print('  stderr:')
                    for line in proc.stderr.rstrip().splitlines():
                        print('    ' + line)
        print('SUITE_SUMMARY:')
        print('  name: ' + result.name)
        print('  total: ' + str(result.total))
        print('  failed: ' + str(result.failed))
        return result
