"""Integration tests use only temporary repositories; no network or real credentials."""

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


HELPER = Path(__file__).resolve().parents[1] / ".utilities" / "sync_notebooks.py"


class NotebookSyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="lab sync spaces ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "student work"
        self.remote = self.root / "remote repo.git"
        self.repo.mkdir()
        # Isolate tests from personal git configuration and credential helpers.
        self.env = os.environ.copy()
        self.env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
        self.git("init", "--bare", str(self.remote))
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Student Test")
        self.git("config", "user.email", "student@example.invalid")
        self.notebook = self.repo / "lab1-notebook.ipynb"
        self.notebook.write_text("initial notebook\n", encoding="utf-8")
        self.git("add", self.notebook.name)
        self.git("commit", "-m", "Initial notebook")
        self.git("remote", "add", "origin", str(self.remote))
        self.git("push", "-u", "origin", "main")

    def git(self, *args, check=True):
        return subprocess.run(["git", *args], cwd=self.repo, env=self.env,
                              capture_output=True, text=True, check=check)

    def run_sync(self, *args, success=True):
        result = subprocess.run([sys.executable, str(HELPER), "--repo", str(self.repo), *args],
                                cwd=self.root, env=self.env, capture_output=True, text=True, timeout=90)
        if success:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("LAB SYNC FAILED", result.stderr)
        return result

    def test_only_root_lab_notebooks_are_committed_and_rerun_is_safe(self):
        self.notebook.write_text("edited notebook\n", encoding="utf-8")
        for filename in (".env", "token.json", "generated.png", "notes.ipynb"):
            (self.repo / filename).write_text("private or generated\n", encoding="utf-8")
        (self.repo / "outputs").mkdir()
        (self.repo / "outputs" / self.notebook.name).write_text("generated", encoding="utf-8")
        self.run_sync()
        self.assertEqual(self.git("diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD").stdout.strip(),
                         self.notebook.name)
        head = self.git("rev-parse", "HEAD").stdout
        self.run_sync()
        self.assertEqual(head, self.git("rev-parse", "HEAD").stdout)
        self.run_sync("--check")

    def test_unrelated_staged_work_is_preserved(self):
        (self.repo / "private.txt").write_text("do not commit", encoding="utf-8")
        self.git("add", "private.txt")
        self.notebook.write_text("new changes", encoding="utf-8")
        previous = self.git("rev-parse", "HEAD").stdout
        result = self.run_sync(success=False)
        self.assertIn("Other files are staged", result.stderr)
        self.assertEqual(previous, self.git("rev-parse", "HEAD").stdout)
        self.assertEqual("private.txt", self.git("diff", "--cached", "--name-only").stdout.strip())

    def test_failed_push_is_retried_without_further_changes(self):
        self.notebook.write_text("saved while offline", encoding="utf-8")
        self.git("remote", "set-url", "--push", "origin", str(self.root / "missing.git"))
        self.run_sync(success=False)
        committed = self.git("rev-parse", "HEAD").stdout
        self.assertEqual("", self.git("status", "--porcelain").stdout)
        self.git("remote", "set-url", "--push", "origin", str(self.remote))
        self.run_sync()
        self.assertEqual(committed, self.git("rev-parse", "origin/main").stdout)
        self.assertEqual(committed, self.git("rev-parse", "HEAD").stdout)

    def test_rapid_overlapping_saves_are_serialized(self):
        self.notebook.write_text("rapid save", encoding="utf-8")
        processes = [subprocess.Popen(
            [sys.executable, str(HELPER), "--repo", str(self.repo)], cwd=self.root,
            env=self.env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        ) for _ in range(8)]
        for process in processes:
            stdout, stderr = process.communicate(timeout=90)
            self.assertEqual(process.returncode, 0, stdout + stderr)
        self.assertEqual("2", self.git("rev-list", "--count", "HEAD").stdout.strip())
        self.run_sync("--check")

    def test_missing_remote_still_commits_locally(self):
        self.git("remote", "remove", "origin")
        self.notebook.write_text("local work", encoding="utf-8")
        result = self.run_sync(success=False)
        self.assertIn("No origin remote", result.stderr)
        self.assertEqual("local work", self.git("show", "HEAD:lab1-notebook.ipynb").stdout)

    def test_missing_identity_is_clear(self):
        self.git("config", "--unset", "user.name")
        self.git("config", "--unset", "user.email")
        self.git("config", "user.useConfigOnly", "true")
        self.notebook.write_text("local work", encoding="utf-8")
        result = self.run_sync(success=False)
        self.assertIn("Git var failed", result.stderr)

    def test_unfinished_merge_is_not_changed(self):
        gitdir = self.repo / ".git"
        (gitdir / "MERGE_HEAD").write_text(self.git("rev-parse", "HEAD").stdout, encoding="utf-8")
        self.notebook.write_text("local work", encoding="utf-8")
        result = self.run_sync(success=False)
        self.assertIn("unfinished", result.stderr)
        self.assertTrue((gitdir / "MERGE_HEAD").exists())

    def test_new_notebook_and_deleted_notebook_are_saved(self):
        new = self.repo / "lab2-notebook.ipynb"
        new.write_text("new lab", encoding="utf-8")
        self.run_sync()
        self.assertEqual("new lab", self.git("show", "HEAD:lab2-notebook.ipynb").stdout)
        new.unlink()
        self.run_sync()
        self.assertNotIn(new.name, self.git("ls-files").stdout)

    def test_diverged_remote_is_not_overwritten(self):
        clone = self.root / "other computer"
        self.git("clone", str(self.remote), str(clone))
        # Explicit branch checkout also works when bare remote HEAD defaults to master.
        self.git("-C", str(clone), "checkout", "main")
        self.git("-C", str(clone), "config", "user.name", "Other Student")
        self.git("-C", str(clone), "config", "user.email", "other@example.invalid")
        (clone / "lab1-notebook.ipynb").write_text("remote work", encoding="utf-8")
        self.git("-C", str(clone), "commit", "-am", "Remote changes")
        self.git("-C", str(clone), "push")
        remote_head = self.git("--git-dir", str(self.remote), "rev-parse", "main").stdout
        self.notebook.write_text("different local work", encoding="utf-8")
        self.run_sync(success=False)
        self.assertEqual(remote_head, self.git("--git-dir", str(self.remote), "rev-parse", "main").stdout)
        self.assertEqual("different local work", self.notebook.read_text(encoding="utf-8"))
        result = self.run_sync("--check", success=False)
        self.assertIn("1 local commits to push, 1 remote commits to review", result.stderr)


if __name__ == "__main__":
    unittest.main()
