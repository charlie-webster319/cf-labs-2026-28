"""Save root lab notebooks to Git and retry pending pushes, without extra packages.

Run with the lab's Python. Every invocation waits for the previous invocation;
the operating system releases the lock even if a process crashes. No credentials,
generated files or other work are staged. Git conflicts require manual attention.
"""

import argparse
from contextlib import contextmanager
import os
from pathlib import Path
import re
import subprocess
import sys
import time


NOTEBOOK = re.compile(r"lab[0-9]+-notebook\.ipynb\Z")


class SyncError(Exception):
    pass


def git(repo, *args, check=True):
    step = "push" if "push" in args else args[0]
    env = os.environ.copy()
    env.update(GIT_TERMINAL_PROMPT="0", GCM_INTERACTIVE="never")
    try:
        result = subprocess.run(
            ["git", *args], cwd=repo, env=env, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise SyncError(f"Git {step} could not finish: {exc}") from exc
    if check and result.returncode:
        detail = result.stderr.strip() or result.stdout.strip()
        raise SyncError(f"Git {step} failed: {detail}")
    return result


@contextmanager
def sync_lock(path, timeout=180):
    """Lock one byte on Windows or the file on Unix; never delete the lock file."""
    with path.open("a+b") as handle:
        handle.seek(0, os.SEEK_END)
        if handle.tell() == 0:
            handle.write(b"0")
            handle.flush()
        deadline = time.monotonic() + timeout
        while True:
            try:
                handle.seek(0)
                if os.name == "nt":
                    import msvcrt
                    msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError as exc:
                if time.monotonic() >= deadline:
                    raise SyncError("Another notebook save is still syncing. Save again to retry.") from exc
                time.sleep(0.1)
        try:
            yield
        finally:
            handle.seek(0)
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(handle, fcntl.LOCK_UN)


def names(output):
    return [name for name in output.split("\0") if name]


def assert_ready(repo):
    if git(repo, "ls-files", "--unmerged").stdout:
        raise SyncError("Unresolved Git conflicts. Ask for help; automatic sync has stopped.")
    for state in ("MERGE_HEAD", "CHERRY_PICK_HEAD", "REVERT_HEAD", "rebase-merge", "rebase-apply"):
        path = Path(git(repo, "rev-parse", "--git-path", state).stdout.strip())
        if not path.is_absolute():
            path = repo / path
        if path.exists():
            raise SyncError("A Git merge or rebase is unfinished. Finish it before syncing notebooks.")
    branch = git(repo, "symbolic-ref", "--quiet", "--short", "HEAD", check=False)
    if branch.returncode:
        raise SyncError("No working branch is selected. Select your lab branch before syncing.")
    staged = names(git(repo, "diff", "--cached", "--name-only", "-z").stdout)
    if any(not NOTEBOOK.fullmatch(name) for name in staged):
        raise SyncError("Other files are staged in Source Control. Commit or unstage them, then save the notebook again.")
    return branch.stdout.strip()


def push(repo, branch):
    remote = git(repo, "config", "--get", f"branch.{branch}.remote", check=False).stdout.strip()
    target = git(repo, "config", "--get", f"branch.{branch}.merge", check=False).stdout.strip()
    args = ["-c", "push.followTags=false", "push", "--porcelain", "--no-force"]
    if remote and target:
        if remote == "." or not target.startswith("refs/heads/"):
            raise SyncError("The branch has no online upstream. Set its GitHub upstream before syncing.")
        args += [remote, f"HEAD:{target}"]
    else:
        if "origin" not in git(repo, "remote").stdout.splitlines():
            raise SyncError("No origin remote is configured. Your notebook is saved locally; connect this repository to GitHub to sync.")
        args += ["--set-upstream", "origin", f"HEAD:refs/heads/{branch}"]
    git(repo, *args)
    print("Lab sync: notebook commits synced to the remote branch.", flush=True)


def sync(repo):
    branch = assert_ready(repo)
    # Include tracked deletions as well as new notebooks; exclude symlinks.
    candidates = set(names(git(repo, "ls-files", "-z").stdout))
    candidates.update(path.name for path in repo.iterdir() if path.is_file())
    notebooks = sorted(name for name in candidates if NOTEBOOK.fullmatch(name))
    if any((repo / name).is_symlink() for name in notebooks):
        raise SyncError("A lab notebook is a symbolic link. Automatic sync has stopped.")
    if notebooks:
        git(repo, "var", "GIT_AUTHOR_IDENT")
        git(repo, "add", "--", *notebooks)
        changed = git(repo, "diff", "--cached", "--quiet", "--", *notebooks, check=False)
        if changed.returncode == 1:
            # --only also protects against unrelated staging by another Git client.
            git(repo, "commit", "--only", "-m", "Save lab notebooks", "--", *notebooks)
            print("Lab sync: notebook changes committed locally.", flush=True)
        elif changed.returncode:
            raise SyncError(f"Checking notebook changes failed: {changed.stderr.strip()}")
    # Always push: a previous save may have committed while offline.
    push(repo, branch)


def check_sync(repo):
    """Refresh upstream status, without changing notebook files or commits."""
    branch = assert_ready(repo)
    remote = git(repo, "config", "--get", f"branch.{branch}.remote", check=False).stdout.strip()
    if not remote or remote == ".":
        raise SyncError("No online upstream is configured. Save a notebook to try syncing first.")
    git(repo, "fetch", "--no-tags", remote)
    counts = git(repo, "rev-list", "--left-right", "--count", "HEAD...@{upstream}").stdout.split()
    changed = git(repo, "status", "--porcelain", "--", ":(top)lab[0-9]*-notebook.ipynb").stdout
    ahead, behind = map(int, counts)
    if changed or ahead or behind:
        raise SyncError(f"Not fully synced: {ahead} local commits to push, {behind} remote commits to review"
                        + (", and notebook changes to save." if changed else ".")
                        + " Save again to retry; ask for help if remote commits need review.")
    print("Lab sync: all saved lab notebooks are synced (remote checked now).", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--check", action="store_true", help="Check saved work against the remote without committing or pushing")
    args = parser.parse_args()
    try:
        repo = Path(git(args.repo, "rev-parse", "--show-toplevel").stdout.strip())
        git_dir = Path(git(repo, "rev-parse", "--git-common-dir").stdout.strip())
        if not git_dir.is_absolute():
            git_dir = repo / git_dir
        with sync_lock(git_dir / "lab-notebook-sync.lock"):
            (check_sync if args.check else sync)(repo)
    except (SyncError, OSError) as exc:
        print(f"LAB SYNC FAILED: {exc}\nYour notebook file remains saved on this computer. "
              "Check Source Control or ask for help, then save again to retry.", file=sys.stderr, flush=True)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
