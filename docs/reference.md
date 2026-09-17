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

Installation does not sign you in. Choose whether to use a tool and handle its sign-in separately. Account entitlements can differ; none is a prerequisite for completing either lab.

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
