from __future__ import annotations

import hashlib
import os
import stat
import subprocess
import tempfile
from pathlib import Path


def git(repo: Path, *args: str, text: bool = True) -> str | bytes:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=text,
    )
    return result.stdout


def write(repo: Path, path: str, content: str) -> None:
    target = repo / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def split_z(data: bytes) -> list[str]:
    return [part.decode("utf-8", errors="surrogateescape") for part in data.split(b"\0") if part]


def parse_name_status(data: bytes) -> set[str]:
    parts = split_z(data)
    result: set[str] = set()
    i = 0
    while i < len(parts):
        status_code = parts[i]
        i += 1
        if status_code.startswith(("R", "C")):
            if i + 1 >= len(parts):
                raise AssertionError(f"rename/copy entry incomplete: {parts!r}")
            result.add(parts[i])
            result.add(parts[i + 1])
            i += 2
        else:
            if i >= len(parts):
                raise AssertionError(f"name-status entry incomplete: {parts!r}")
            result.add(parts[i])
            i += 1
    return result


def working_candidates(repo: Path, head: str) -> set[str]:
    changed = parse_name_status(
        git(repo, "diff", "--name-status", "-z", "--find-renames", head, text=False)
    )
    staged = parse_name_status(
        git(repo, "diff", "--cached", "--name-status", "-z", "--find-renames", head, text=False)
    )
    untracked = set(
        split_z(git(repo, "ls-files", "--others", "--exclude-standard", "-z", text=False))
    )
    return changed | staged | untracked


def head_paths(repo: Path, old_head: str, new_head: str) -> set[str]:
    if old_head == new_head:
        return set()
    return parse_name_status(
        git(
            repo,
            "diff",
            "--name-status",
            "-z",
            "--find-renames",
            old_head,
            new_head,
            text=False,
        )
    )


def file_state(path: Path) -> str:
    if not path.exists() and not path.is_symlink():
        return "absent"
    info = path.lstat()
    mode = stat.S_IMODE(info.st_mode)
    if path.is_symlink():
        return f"symlink|{mode:o}|{os.readlink(path)}"
    if path.is_file():
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        return f"file|{mode:o}|{digest}"
    return f"other|{mode:o}"


def tree_state(repo: Path, head: str, path: str) -> str:
    probe = subprocess.run(
        ["git", "cat-file", "-e", f"{head}:{path}"],
        cwd=repo,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if probe.returncode != 0:
        return "absent"
    mode_line = git(repo, "ls-tree", head, "--", path).strip()
    mode = mode_line.split(maxsplit=1)[0]
    blob = git(repo, "show", f"{head}:{path}", text=False)
    digest = hashlib.sha256(blob).hexdigest()
    kind = "symlink" if mode == "120000" else "file"
    return f"{kind}|{mode}|{digest}"


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="kdsl-run-changed-") as tmp:
        repo = Path(tmp) / "repo"
        repo.mkdir()
        git(repo, "init", "-q")
        git(repo, "config", "user.email", "kdsl@example.invalid")
        git(repo, "config", "user.name", "KDSL Regression")

        initial_files = {
            "src/Clean.cs": "clean-base\n",
            "src/DirtyChanged.cs": "dirty-base\n",
            "src/DirtyUnchanged.cs": "dirty-unchanged-base\n",
            "src/Delete.cs": "delete-base\n",
            "src/OldName.cs": "rename-base\n",
            "src/Restored.cs": "restored-base\n",
            "src/Committed.cs": "committed-base\n",
            "tests/EditedTests.cs": "edited-test-base\n",
            "tests/ExecutedOnlyTests.cs": "executed-only-base\n",
        }
        for path, content in initial_files.items():
            write(repo, path, content)
        git(repo, "add", ".")
        git(repo, "commit", "-q", "-m", "fixture baseline")

        # Pre-existing state before the run.
        write(repo, "src/DirtyChanged.cs", "dirty-before-run\n")
        write(repo, "src/DirtyUnchanged.cs", "dirty-unchanged-before-run\n")
        write(repo, "src/PreExistingUntracked.cs", "untracked-unchanged\n")
        write(repo, "src/PreExistingUntrackedChanged.cs", "untracked-before-run\n")

        initial_head = git(repo, "rev-parse", "HEAD").strip()
        initial_candidates = working_candidates(repo, initial_head)
        initial_states = {path: file_state(repo / path) for path in initial_candidates}

        # Current run actions.
        write(repo, "src/Clean.cs", "clean-changed-in-run\n")
        write(repo, "src/DirtyChanged.cs", "dirty-changed-again-in-run\n")
        write(repo, "src/PreExistingUntrackedChanged.cs", "untracked-changed-in-run\n")
        write(repo, "src/New.cs", "created-in-run\n")
        (repo / "src/Delete.cs").unlink()
        git(repo, "mv", "src/OldName.cs", "src/NewName.cs")
        write(repo, "src/Restored.cs", "temporary-change\n")
        write(repo, "src/Restored.cs", "restored-base\n")
        write(repo, "tests/EditedTests.cs", "edited-test-in-run\n")
        # ExecutedOnlyTests is deliberately not edited.

        # Exercise InitialHEAD != FinalHEAD and CommittedCandidate.
        write(repo, "src/Committed.cs", "committed-in-run\n")
        git(repo, "add", "src/Committed.cs")
        git(repo, "commit", "-q", "-m", "fixture run commit")
        final_head = git(repo, "rev-parse", "HEAD").strip()

        final_candidates = working_candidates(repo, final_head)
        committed_candidates = head_paths(repo, initial_head, final_head)
        candidates = initial_candidates | final_candidates | committed_candidates

        baseline_states: dict[str, str] = {}
        final_states: dict[str, str] = {}
        for path in sorted(candidates):
            baseline_states[path] = initial_states.get(path, tree_state(repo, initial_head, path))
            final_states[path] = file_state(repo / path)

        run_changed = {
            path for path in candidates if baseline_states[path] != final_states[path]
        }
        expected = {
            "src/Clean.cs",
            "src/DirtyChanged.cs",
            "src/PreExistingUntrackedChanged.cs",
            "src/New.cs",
            "src/Delete.cs",
            "src/OldName.cs",
            "src/NewName.cs",
            "src/Committed.cs",
            "tests/EditedTests.cs",
        }
        excluded = {
            "src/DirtyUnchanged.cs",
            "src/PreExistingUntracked.cs",
            "src/Restored.cs",
            "tests/ExecutedOnlyTests.cs",
        }

        if run_changed != expected:
            raise AssertionError(
                "RunChanged mismatch\n"
                f"expected={sorted(expected)}\n"
                f"actual={sorted(run_changed)}\n"
                f"missing={sorted(expected - run_changed)}\n"
                f"extra={sorted(run_changed - expected)}"
            )
        if run_changed & excluded:
            raise AssertionError(f"excluded paths leaked: {sorted(run_changed & excluded)}")

        print(
            "PASS git_repository=1 "
            f"candidates={len(candidates)} changed={len(run_changed)} excluded={len(excluded)} "
            "clean=1 dirty_changed=1 dirty_unchanged=1 untracked=2 create=1 "
            "delete=1 rename=1 restored=1 test_edited=1 test_executed_only=1 committed=1"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
