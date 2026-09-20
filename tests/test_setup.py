"""Safe setup failure/retry checks: no downloads, installs, accounts or credentials.

CI separately exercises the real setup and rerun on all three operating systems.
These tests isolate failure branches using throwaway copies and fake commands.
"""

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
POWERSHELL = shutil.which("powershell") or shutil.which("pwsh")


class SetupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="lab setup with spaces ")
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "student lab"
        shutil.copytree(ROOT / ".utilities", self.repo / ".utilities")
        self.bin = self.repo / "fake commands"
        self.bin.mkdir()
        self.env = os.environ.copy()
        self.env["PATH"] = str(self.bin) + os.pathsep + self.env["PATH"]
        self.log = self.repo / "command log.txt"
        self.env["LAB_TEST_LOG"] = str(self.log)

    def executable(self, path, text):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("#!/bin/sh\n" + text, encoding="utf-8")
        path.chmod(0o755)

    def bash(self, filename, *args):
        return subprocess.run(["bash", str(self.repo / ".utilities" / filename), *args],
                              cwd=self.bin, env=self.env, capture_output=True, text=True, timeout=30)

    def powershell(self, script):
        wrapper = self.repo / "test wrapper.ps1"
        wrapper.write_text(script + "\nexit $LASTEXITCODE\n", encoding="utf-8")
        return subprocess.run([POWERSHELL, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(wrapper)],
                              cwd=self.repo, env=self.env, capture_output=True, text=True, timeout=30)

    @unittest.skipIf(os.name == "nt", "Unix shell implementation; Windows real setup runs in CI")
    def test_setup_rerun_syncs_existing_environment_in_path_with_spaces(self):
        self.executable(self.repo / ".tools/uv/uv", '''
if [ "$1" = --version ]; then echo 'uv 0.12.15'; exit 0; fi
printf 'uv %s\\n' "$*" >> "$LAB_TEST_LOG"
[ "$UV_PROJECT_ENVIRONMENT" = "$PWD/.venv" ] || exit 41
[ "$UV_PYTHON_PREFERENCE" = only-managed ] || exit 42
[ "$*" = 'sync --locked' ] || exit 43
''')
        self.executable(self.repo / ".venv/bin/python", 'printf "python %s\\n" "$*" >> "$LAB_TEST_LOG"\n')
        # Reusing an existing environment must never suppress a locked sync.
        for _ in range(2):
            result = self.bash("setup_lab.sh")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Setup complete", result.stdout)
        lines = self.log.read_text(encoding="utf-8").splitlines()
        self.assertEqual(lines.count("uv sync --locked"), 2)
        self.assertEqual(sum(line.startswith("python -m ipykernel install --prefix ") for line in lines), 2)

    @unittest.skipIf(os.name == "nt", "Unix shell implementation; Windows download failure tested separately")
    def test_setup_reports_the_exact_failed_step(self):
        self.executable(self.bin / "curl", 'echo "simulated download failure" >&2\nexit 23\n')
        result = self.bash("setup_lab.sh")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Setup failed while installing the lab copy of uv", result.stderr)
        self.executable(self.repo / ".tools/uv/uv", '''
if [ "$1" = --version ]; then echo 'uv 0.12.15'; exit 0; fi
exit 24
''')
        result = self.bash("setup_lab.sh")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Setup failed while installing Python and the locked lab packages", result.stderr)
        self.executable(self.repo / ".tools/uv/uv", '''
if [ "$1" = --version ]; then echo 'uv 0.12.15'; fi
exit 0
''')
        self.executable(self.repo / ".venv/bin/python", "exit 25\n")
        result = self.bash("setup_lab.sh")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Setup failed while registering the lab notebook kernel", result.stderr)

    @unittest.skipIf(os.name == "nt", "Windows optional tool failure tested separately")
    def test_optional_failures_continue_and_do_not_modify_lab_environment(self):
        marker = self.repo / ".venv" / "existing lab environment"
        marker.parent.mkdir()
        marker.write_bytes(b"unchanged")
        self.executable(self.bin / "curl", 'printf "curl %s\\n" "$*" >> "$LAB_TEST_LOG"\nexit 23\n')
        self.executable(self.bin / "code", 'printf "code %s\\n" "$*" >> "$LAB_TEST_LOG"\nexit 24\n')
        result = self.bash("install_ai.sh")
        combined = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        for tool in ("copilot", "codex", "claude"):
            # Codex/Claude refresh even if installed; Copilot may already exist.
            self.assertTrue(f"OPTIONAL TOOL FAILED: {tool}" in combined or
                            f"{tool} is already installed." in combined, combined)
        log = self.log.read_text(encoding="utf-8")
        self.assertIn("code --install-extension OpenAI.chatgpt", log)
        self.assertIn("code --install-extension Anthropic.claude-code", log)
        self.assertIn("Optional tools finished", combined)
        self.assertEqual(marker.read_bytes(), b"unchanged")
        self.assertFalse((self.repo / ".tools").exists())

    @unittest.skipIf(os.name == "nt", "Dev container uses Bash")
    def test_container_starts_refresh_existing_ai_tools_using_latest(self):
        self.executable(self.repo / ".tools/uv/uv", 'printf "uv %s\\n" "$*" >> "$LAB_TEST_LOG"\n')
        # Fake old binaries must not suppress either update or be launched for login.
        for name in ("copilot", "codex", "claude"):
            self.executable(self.bin / name, 'echo "unexpected tool launch" >&2; exit 99\n')
        self.executable(self.bin / "curl", '''
while [ "$#" -gt 0 ]; do
    case "$1" in
        https://*) printf 'download %s\\n' "$1" >> "$LAB_TEST_LOG" ;;
        -o) shift; target="$1" ;;
    esac
    shift
done
cat > "$target" <<'INSTALLER'
printf 'installer %s\\n' "$*" >> "$LAB_TEST_LOG"
INSTALLER
''')
        for _ in range(2):
            result = self.bash("post_start.sh")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Optional tools finished (0 failed steps)", result.stdout)
        lines = self.log.read_text().splitlines()
        self.assertEqual(lines.count("installer --release latest"), 2)
        self.assertEqual(lines.count("installer latest"), 2)
        self.assertEqual(lines.count("download https://chatgpt.com/codex/install.sh"), 2)
        self.assertEqual(lines.count("download https://claude.ai/install.sh"), 2)
        self.assertEqual(lines.count("uv sync --locked --inexact --group notebook-mcp"), 2)

    @unittest.skipIf(os.name == "nt", "Dev container uses Bash")
    def test_container_start_survives_failed_updates_and_preserves_old_tools(self):
        marker = self.repo / ".venv" / "lab environment"
        marker.parent.mkdir()
        marker.write_bytes(b"unchanged")
        for name in ("copilot", "codex", "claude"):
            self.executable(self.bin / name, 'echo "old version"\n')
        original = {name: (self.bin / name).read_bytes() for name in ("codex", "claude")}
        self.executable(self.bin / "curl", "exit 23\n")
        result = self.bash("post_start.sh")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for name, content in original.items():
            self.assertIn(f"OPTIONAL TOOL FAILED: {name}", result.stderr)
            self.assertEqual((self.bin / name).read_bytes(), content)
        self.assertIn("The labs still work", result.stderr)
        self.assertEqual(marker.read_bytes(), b"unchanged")

    @unittest.skipUnless(POWERSHELL, "PowerShell is unavailable; Windows CI runs this test")
    def test_powershell_setup_download_failure_identifies_step(self):
        result = self.powershell('''
function Invoke-WebRequest { throw 'simulated download failure' }
& "$PSScriptRoot/.utilities/setup_lab.ps1"
''')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("installing the lab copy of uv", result.stdout + result.stderr)
        self.assertIn("simulated download", result.stdout + result.stderr)
        self.assertFalse((self.repo / ".venv").exists())

    @unittest.skipUnless(POWERSHELL, "PowerShell is unavailable; Windows CI runs this test")
    def test_powershell_optional_failures_are_isolated(self):
        marker = self.repo / ".venv" / "existing lab environment"
        marker.parent.mkdir()
        marker.write_bytes(b"unchanged")
        result = self.powershell('''
function Get-Command { param($Name, $ErrorAction) return $null }
function winget { Write-Host 'MOCK winget failed'; $global:LASTEXITCODE = 23 }
function Invoke-WebRequest { throw 'simulated download failure' }
function code { Write-Host "MOCK extension $args"; $global:LASTEXITCODE = 24 }
& "$PSScriptRoot/.utilities/install_ai.ps1"
''')
        combined = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        for tool in ("Copilot CLI", "codex", "claude", "OpenAI.chatgpt", "Anthropic.claude-code"):
            self.assertIn(f"OPTIONAL TOOL FAILED: {tool}", combined)
        self.assertIn("Optional tools finished (5 failed steps)", combined)
        self.assertEqual(marker.read_bytes(), b"unchanged")
        self.assertFalse((self.repo / ".tools").exists())

    def test_python_setup_task_does_not_depend_on_optional_installers(self):
        tasks = json.loads((ROOT / ".vscode/tasks.json").read_text(encoding="utf-8"))["tasks"]
        setup = next(task for task in tasks if task["label"] == "Setup lab environment")
        self.assertNotIn("dependsOn", setup)
        for suffix in ("sh", "ps1"):
            text = (ROOT / f".utilities/setup_lab.{suffix}").read_text(encoding="utf-8")
            self.assertNotIn("install_ai", text)
        # Process tasks pass paths as arguments, preserving spaces on Windows.
        self.assertEqual(setup["type"], "process")
        self.assertEqual(setup["windows"]["args"][-1], "${workspaceFolder}/.utilities/setup_lab.ps1")


if __name__ == "__main__":
    unittest.main()
