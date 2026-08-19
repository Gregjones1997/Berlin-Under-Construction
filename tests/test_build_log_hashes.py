from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


CHECKER = Path(__file__).parents[1] / "scripts" / "check_build_log_hashes.py"


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def initialize_repo(tmp_path: Path) -> tuple[Path, str]:
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-b", "main")
    git(repo, "config", "user.name", "Build Log Test")
    git(repo, "config", "user.email", "build-log-test@example.invalid")
    (repo / "tracked.txt").write_text("reachable\n", encoding="utf-8")
    git(repo, "add", "tracked.txt")
    git(repo, "commit", "-m", "reachable commit")
    return repo, git(repo, "rev-parse", "--short=7", "HEAD")


def run_checker(repo: Path, log: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECKER), str(log)],
        cwd=repo,
        capture_output=True,
        text=True,
    )


class BuildLogHashCliTests(unittest.TestCase):
    def test_cli_accepts_a_reachable_build_log_hash(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo, reachable_hash = initialize_repo(Path(directory))
            log = repo / "build-log.md"
            log.write_text(f"Verified work. `{reachable_hash}`\n", encoding="utf-8")

            result = run_checker(repo, log)

            self.assertEqual(result.returncode, 0)
            self.assertIn("1 reachable build-log hash", result.stdout)

    def test_cli_ignores_prefixed_content_hashes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo, reachable_hash = initialize_repo(Path(directory))
            content_hash = "a" * 64
            log = repo / "build-log.md"
            log.write_text(
                f"Commit `{reachable_hash}`; content `sha256:{content_hash}`\n",
                encoding="utf-8",
            )

            result = run_checker(repo, log)

            self.assertEqual(result.returncode, 0)
            self.assertIn("1 reachable build-log hash", result.stdout)

    def test_cli_rejects_an_orphaned_build_log_hash(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo, _ = initialize_repo(Path(directory))
            log = repo / "build-log.md"
            log.write_text("Recorded before amend. `deadbee`\n", encoding="utf-8")

            result = run_checker(repo, log)

            self.assertEqual(result.returncode, 1)
            self.assertIn("deadbee", result.stderr)
            self.assertIn("not reachable from git log --all", result.stderr)


class RealOrphanTests(unittest.TestCase):
    def test_cli_rejects_a_pre_amend_hash_that_cat_file_still_resolves(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo, orphaned = initialize_repo(Path(directory))
            (repo / "tracked.txt").write_text("amended\n", encoding="utf-8")
            git(repo, "add", "tracked.txt")
            git(repo, "commit", "--amend", "-m", "reachable commit")

            still_resolves = subprocess.run(
                ["git", "cat-file", "-e", f"{orphaned}^{{commit}}"],
                cwd=repo,
                capture_output=True,
            )
            self.assertEqual(
                still_resolves.returncode,
                0,
                "precondition: the pre-amend object must survive locally",
            )

            log = repo / "build-log.md"
            log.write_text(f"Recorded before amend. `{orphaned}`\n", encoding="utf-8")
            result = run_checker(repo, log)

            self.assertEqual(result.returncode, 1)
            self.assertIn(orphaned, result.stderr)
