# Optional lab reference

You do not need this page to start the labs. Follow the [README](../README.md) first.

## The lab environment

Both Codespaces and local VS Code use the same project environment, **`.venv`**, managed by **uv**. It keeps the lab's Python packages separate from other projects on your computer.

- `.python-version` specifies Python **3.12.14**.
- `pyproject.toml` lists the nine teaching packages: NumPy, pandas, openpyxl, plotnine, mizani, adjustText, PyPortfolioOpt, CVXPY and ipykernel. PyPortfolioOpt is pinned to **1.5.6**.
- `uv.lock` fixes the resolved package versions, including the packages they depend on.
- Notebook validation tools are in a separate development group; they are not needed to do the exercises.

**Setup lab environment** installs a pinned copy of uv in `.tools/uv` if needed, obtains the required Python version and runs `uv sync --locked`, including on reruns. It then registers **Corporate Finance Labs (.venv)** as the notebook kernel. Rerunning setup repairs or updates the environment to match the lockfile; it does not replace your notebooks. If setup fails, read the named step in its terminal output and retry after correcting that issue.

You do not need to activate the environment in a terminal to run a notebook. Select its kernel in the notebook instead. Avoid installing packages into another Python environment to fix a missing-package error: rerun the setup task first.

## What saving and syncing mean

Your working files live inside your Codespace or local project folder. GitHub holds the uploaded copy. These are separate places:

1. **Save** writes your current edits to the working files.
2. **Commit** records a version in the working copy's Git history.
3. **Push** uploads commits to GitHub.

The repository's Run On Save helper attempts the last two steps whenever a root-level `lab*-notebook.ipynb` is saved. It only commits these lab notebooks, not every file in the folder. Other files you create need a deliberate, separate commit if you want them on GitHub. Credentials, local tool state and generated files are excluded.

Overlapping saves are handled one at a time. If a push fails, the committed work remains in your working copy and the next notebook save retries the pending push. The helper does not force-push or resolve conflicting work automatically.

Run **Terminal → Run Task → Check whether your work has synced** before switching computers or stopping a Codespace. This checks the current working copy and its connection to GitHub. A failed connection cannot confirm that work is safely uploaded. Read the task output and check **View → Output → Run On Save** for save-triggered errors.

For a connection failure, reconnect and save again. For an authentication, missing Git identity or write-permission error, follow the reported recovery step. For a conflict or remote changes you do not understand, keep your working copy and ask your lecturer for help before continuing on another machine.

Work in one copy at a time. Reopen your existing Codespace when returning to the labs. If you deliberately switch to another copy, first check that your previous work has synced, then bring the new copy up to date using Git before editing.

## Optional notebook check on GitHub

After syncing, open your private repository on GitHub and choose **Actions → Check my notebooks (optional) → Run workflow**. This runs both notebooks from the beginning on Linux and saves the executed notebooks and figures as a downloadable result. It does not change your working notebooks.

The check only tests whether the notebooks run: it does not mark your answers or confirm that your financial reasoning is correct. A failure identifies the step or cell that needs attention. This is optional; you can complete the labs by running the cells in Codespaces. It does not run automatically on notebook saves, and running it is not a formal submission.

## Optional AI installations

AI installation is separate from Python setup. Codespaces attempts to install all three assistants' extensions and command-line tools. Local setup recommends Copilot alongside the essential notebook extensions; **Install optional AI tools** adds Codex and Claude extensions and all three command-line tools using their official installers. It can be rerun if an optional download fails.

Each container start (including first creation) installs or updates the Codex and Claude Code CLIs from their official `latest` release channels. An unavailable download produces a warning and leaves the labs usable; the next start retries. The container enables automatic extension checks and updates with no extra release delay. An extension update can still require **Restart Extensions** before it takes effect. Existing Codespaces need the updated repository files and a container rebuild to pick up these settings; changing the starter template does not update student repositories automatically.

Installation does not sign you in. Choose whether to use a tool and handle its sign-in separately. Account entitlements can differ; none is a prerequisite for completing either lab.

## Chat panels and editor recovery

The course settings keep the file explorer on the left and the secondary sidebar visible on the right. Current Codex and Copilot versions use the secondary sidebar by default; Claude Code is configured to open there too. Your saved VS Code layout can override a view's initial location. If an assistant is on the left, right-click its icon and choose **Move To → Secondary Side Bar** once. VS Code remembers that placement.

If interface labels display `null`, save your work, then use **F1 → Developer: Reload Window**. A browser reload is another recovery step if the editor is unresponsive. This does not require reinstalling Python. When asked to trust the workspace, check that it is your course repository; do not disable Workspace Trust globally. The assistant's own sign-in remains separate from workspace trust.

## Optional notebook tools for Codex and Claude Code

The repository includes `.codex/config.toml` for Codex and `.mcp.json` for Claude Code, both defining the same local `jupyter` MCP server ([The Notebook MCP](https://github.com/svallory/the-notebook-mcp)). It can read and edit saved cells and inspect saved outputs. Dependencies are pinned in the optional `notebook-mcp` group and the lockfile, using the same `.venv`; the nine core teaching packages are unchanged. No extra account, token or public server is needed.

Open the assistant in the repository root. Accept its normal project-trust/MCP prompt, then use `/mcp` to check that `jupyter` is connected. In Codespaces, uv is already on PATH and optional dependencies are prepared at container startup. Locally, uv must be on PATH; the configuration installs its locked optional dependencies on first use. A slow first connection may need a retry. The configuration never approves tools on the student's behalf.

**This works with saved notebook files, not the live VS Code kernel.** Save before asking for help and pause typing while the assistant edits. Reload the notebook from disk after an external edit if VS Code has not refreshed it; preserve any unsaved work before doing so. Run cells in the usual notebook interface. The server's separate-Jupyter execution tool is not configured for these labs. An MCP edit also does not itself guarantee a commit/push: use **Check whether your work has synced**.

Keep the initial MCP list to this one server. [Context7](https://github.com/upstash/context7) is an optional later addition for library documentation, especially when matching examples to package versions; its anonymous service has rate limits. Filesystem and Git servers add little to these coding assistants' existing tools. GitHub, browser and live market-data servers are unnecessary for the supplied labs and add authentication or extra moving parts.

## Optional teaching skills

All three assistants have the same three repository skills:

| Skill | Use it for |
| --- | --- |
| `cf-explain-finance` | An explanation grounded in the lecture slides, with an example when useful |
| `cf-notebook-help` | Understanding a cell, debugging an error or making a small requested correction |
| `cf-revision-quiz` | Practice questions and feedback, normally one question at a time |

Ask naturally, such as “Explain why bond prices fall when yields rise” or “Quiz me on discounting”. The assistant can select a relevant skill automatically. To choose explicitly, use `/cf-explain-finance`, `/cf-notebook-help` or `/cf-revision-quiz` in Copilot or Claude Code; in Codex use `$cf-explain-finance`, `$cf-notebook-help` or `$cf-revision-quiz`. Skills guide the assistant; they do not provide an account or replace checking its answers. No AI tool is required for the labs.

Maintainers: edit the originals under `.agents/skills/`, which Codex and Copilot discover. Run `uv run --no-sync python .utilities/sync_skills.py` to update the committed copies under `.claude/skills/` for Claude Code. Commit both sets. The instructor CI checks that the copies match, so students need no skill installation or symlink setup. The helper touches only these three `SKILL.md` files; resources stay in `.assistant-resources/`. There is no need for another copy in `.github/skills/`.

If newly added skills are not listed, start a new assistant session; in VS Code, reload the window if needed. Existing student repositories must receive these files before the skills are available there.

## Further reading

- [Creating a Codespace — GitHub](https://docs.github.com/en/codespaces/developing-in-a-codespace/creating-a-codespace-for-a-repository)
- [Using Git in VS Code](https://code.visualstudio.com/docs/sourcecontrol/quickstart)
- [GitHub Copilot documentation](https://docs.github.com/en/copilot)
- [Tidy Finance](https://www.tidy-finance.org/)
- [Software Carpentry: Programming with Python](https://swcarpentry.github.io/python-novice-inflammation/)

Maintainers can add the locked validation group with `.tools/uv/uv sync --locked --group dev`, then run `.tools/uv/uv run --no-sync python tests/execute_notebooks.py` and `.tools/uv/uv run --no-sync python tests/validate_finance.py`. **Instructor template validation** repeats setup and notebook checks on Linux, macOS and Windows, including regression tests and independent checks of the supplied worked examples. Its jobs run only in `ustandrews-ec3318-mn3101/cf-labs-2026-27`; inherited copies skip them. These financial checks are template maintenance checks, not an assessment rubric. Student copies have the separate, manually started execution check above. Executed notebooks and plots go to the ignored `outputs/validation/` folder.

Official installation and calculation references:

- [uv installation](https://docs.astral.sh/uv/getting-started/installation/)
- [Copilot CLI installation](https://docs.github.com/en/copilot/how-tos/set-up/install-copilot-cli)
- [Codex CLI installation](https://learn.chatgpt.com/docs/codex/cli)
- [Claude Code installation](https://code.claude.com/docs/en/setup)
- [PyPortfolioOpt expected returns](https://pyportfolioopt.readthedocs.io/en/stable/ExpectedReturns.html)
- [PyPortfolioOpt mean–variance optimisation](https://pyportfolioopt.readthedocs.io/en/stable/MeanVariance.html)
- [PyPortfolioOpt discrete allocation](https://pyportfolioopt.readthedocs.io/en/stable/Postprocessing.html)
