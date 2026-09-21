# Implementation and verification — 17 September 2026

## Editor recovery and sidebar defaults — 21 September 2026

In the instructor's existing `expert-space-bassoon` Codespace, reloading the browser editor cleared the literal `null` labels from Copilot Chat. The workspace path was `/workspaces/cf-labs-2026-27`; accepting its normal trust prompt removed Restricted Mode. This is a verified recovery, not a diagnosis or upstream fix for the initial loading fault. Browser logs also contained extension compatibility errors, but their relationship to the labels was not established.

Workspace and devcontainer defaults now keep the primary sidebar on the left, the secondary sidebar visible, and `claudeCode.preferredLocation` set to `sidebar`. The installed Codex and Claude extension manifests provide secondary-sidebar views on supported VS Code versions. Existing per-user view placements are not overwritten; the reference documents the one-time Move To action. JSON parsing and whitespace validation passed. No Python, notebook, dependency or trust-policy settings were changed.

## Notebook MCP — 20 September 2026

Added project MCP configuration for Claude Code (`.mcp.json`) and Codex (`.codex/config.toml`), a Claude startup timeout, shared teaching instructions, and optional locked notebook-tool dependencies. The `.gitignore` exceptions allow only the shared settings; credentials and local assistant state remain ignored. All previously locked package versions are unchanged; 92 additional packages are confined to the optional group and its dependency graph. Container startup preloads that group without making an optional failure fail startup.

The pinned `the-notebook-mcp` 0.9.0 CLI failed on long paths and uses obsolete FastMCP constructor/tool-registration APIs. A small compatibility launcher uses its file-tool providers with current FastMCP 2 registration and absolute project paths. `jupyter-kernel-client<1` preserves the import API those providers require. The launcher deliberately omits `notebook_execute_cell`: there is no separate Jupyter server and no attachment to VS Code's live kernel.

A clean temporary uv project on macOS, with spaces and a long path, passed all 18 MCP/setup/sync tests. Real MCP clients launched both configurations, discovered tools, read a saved notebook and output, edited a disposable cell while preserving the explanation, and rejected an edit outside the project. No teaching notebook was modified by these checks. Lock validation, configuration parsing and whitespace checks passed. The [three-platform validation run](https://github.com/ustandrews-ec3318-mn3101/cf-labs-2026-27/actions/runs/35508720000) passed on Linux, macOS and Windows for commit `379bd72`, including clean setup/reruns, all regression tests, full execution of both notebooks and independent financial checks. The update was tested on a separate branch before promotion to the private starter template's `main`.

## AI update change — 20 September 2026

The container now invokes optional AI setup on every start, including first creation. Codex and Claude Code use their official installers with explicit `latest` targets even when binaries already exist. Python setup remains in `postCreateCommand`; optional update failures are reported without failing container startup. Extension auto-checking and auto-updating are explicitly enabled with zero additional release delay.

All eight setup regression checks passed locally, including repeated starts with existing binaries, paths containing spaces, and failed downloads preserving existing tools and the Python environment. Bash syntax, container JSON/hook validation and whitespace checks passed. Installer downloads were mocked for these regression tests. A fresh instructor-account Codespace also installed Python 3.12.14, Codex CLI 0.155.1 and Claude Code 2.1.278 through the real installers; rerunning the startup hook completed with zero failed optional steps and preserved the environment. Existing student repositories need these changes separately, followed by a rebuild.

### Fresh Codespace check — 20 September 2026

The editor automatically selected `.venv/bin/python` (`cflabs`, Python 3.12.14). The first Lab 1 code cell completed successfully in a disposable notebook under ignored `outputs/qa/`. No Python-installation or extension-recommendation prompt appeared. Python, Jupyter, Run On Save, Codex and Claude Code extensions were installed. The instructor account also loaded personal extensions; Claude extension versions changed during that process, and its update/restart UI was exercised. This verifies installation and update support, not an assurance that every account immediately activates the newest extension build.

The startup hook preloaded Notebook MCP 0.9.0. Real MCP protocol tests launched both checked-in client configurations in the Codespace and passed saved-cell/output reads, disposable edits and outside-project rejection. Claude CLI detected the project server and correctly reported pending approval. Codex CLI did not list it before Codex project trust; the signed-in assistant trust/connection flow and paid model calls were not exercised. No authentication or approval bypass was added. These remain account-dependent checks.

Following approval to set up the course, the starter was published as the private template [cf-labs-2026-27](https://github.com/ustandrews-ec3318-mn3101/cf-labs-2026-27). The original `christian-engels/cflabs` remote was not changed. A separate private `cf-labs-2026-27-pilot` repository tests the student workflow without student data.

## Implemented

- Codespaces is the main student route; local setup, optional AI tools and technical reference are separate.
- Python 3.12.14 and PyPortfolioOpt 1.5.6; nine direct teaching packages. The final lock contains 65 core packages across platform markers (64 installed on this Mac), rather than the earlier plan's estimated 69. Development validation adds eight packages. All versions are locked.
- Project-local uv 0.12.15 bootstraps the single `.venv`. Setup always runs `uv sync --locked` and registers its kernel inside that environment. Existing system uv/Python installations are unchanged.
- Plotnine 0.14.5 fails with Matplotlib 3.11.2 (`_get_textbox` was removed). The verified lock constrains Matplotlib to 3.8.4 and preserves SciPy 1.15.2 and statsmodels 0.14.4 for the teaching stack.
- Codespaces declares all three assistants' extensions and installs their CLIs with official installers. Optional installer failures are reported separately from Python setup. No authentication command is run by setup.
- One portable notebook sync helper serializes saves, restricts automatic commits to root numbered lab notebooks, retries pending pushes, and refuses conflicts or unrelated staging. A status task fetches the upstream state before reporting success.
- Compounding, VaR, sample alignment, arithmetic annualisation, risk-free rate, constraints, chart labels, frontiers and whole-share allocation explanations are corrected. The dataset and sequence of worked examples are preserved.

## Verified locally on macOS / Apple Silicon

- Real clean installation and rerun in a temporary folder containing spaces; all nine packages import; kernel executable points to that folder's `.venv`.
- Both complete notebooks execute under their `cflabs` kernel with no cell errors or notebook-execution warnings. Source cell IDs are unique. Outputs are saved separately under `outputs/validation/`.
- All seven notebook plots were inspected, including a second review after correcting the two eight-stock chart titles and separating frontier annotations.
- Fifteen regression tests pass: setup reruns, exact failed-step messages, optional-tool failures, spaced paths, overlapping saves, failed-push retry without new edits, excluded files, preservation of unrelated staging, missing identity/remote, unfinished merge, and divergence without force-pushing. PowerShell failure branches were tested using `pwsh` on macOS with mocked commands.
- Independent NumPy calculations from the original Excel file reproduce the 120 monthly observations, annual means/covariance and 95% Amazon monthly historical VaR (10.87583%). Independent SciPy SLSQP solutions agree with all seven portfolio examples and all 100 frontier points within numerical tolerances. Weight sums, bounds and return targets pass.
- Whole-share allocation: MSFT 10, WMT 35, AMZN 10, TSLA 3, AAPL 2. Historical adjusted-price units cost $9,997.12; remaining cash is $2.88. Together they equal the $10,000 budget.
- Excel dataset is byte-for-byte unchanged. SHA-256: `58ac2dd56c42ac59917fc3819a6be97083f7bcab2c46e01b94985bd23ee8746a`.
- `git diff --check` passes. The separate direct-code financial validator emits two harmless warnings that an Agg figure cannot be shown; rich notebook rendering is checked by the notebook executor.

## Verified on GitHub Actions

The [three-platform validation run](https://github.com/ustandrews-ec3318-mn3101/cf-labs-2026-27/actions/runs/35264233511) passed on Linux, macOS and Windows: clean setup, setup reruns, regression tests, full execution of both notebooks, independent financial validation and export of plots. The checkout path `lab workspace` exercises spaces.

The instructor workflow is restricted to the exact template repository. It was skipped in the pilot copy as intended. The pilot's separately dispatched [Check my notebooks (optional)](https://github.com/ustandrews-ec3318-mn3101/cf-labs-2026-27-pilot/actions/runs/35210745703) passed. This student workflow runs only on request and does not grade financial answers.

All 21 exported plots (seven per platform) were visually inspected. No missing plots, clipped axes, titles or legends were found. Frontier labels remain crowded at small display sizes; font placement varies slightly across platforms.

## Live-account checks

A fresh two-core Codespace was created from the private pilot. Automatic setup installed Python 3.12.14 and the project environment. Selecting **Python Environments → cflabs (3.12.14), .venv/bin/python** ran all 22 Lab 1 code cells without errors. The editor automatically committed and pushed the executed notebook; GitHub commit `d9abc3b7eac161588b617e955e7fe998900b1e87` was independently checked.

The live sync-status check fetched GitHub and reported all saved lab notebooks synced, with exit status 0. The pilot Codespace was stopped after verification.

Python, Jupyter, Run On Save, Codex and Claude extensions were confirmed installed; this VS Code release includes **GitHub Copilot Chat 0.66.0** as a built-in extension. The CLIs reported Copilot 1.0.85, Codex 0.154.0 and Claude 2.1.274. No assistant login was needed or initiated. Copilot's first version check spent about 115 seconds unpacking its package.

A second fresh Codespace verified the startup correction: the project `.venv` and local uv are on PATH, and the supported `python.useEnvironmentsExtension: false` setting lets the main Python extension discover the lab environment without the newer environment manager's false ‘No Python found’ prompt. Required extensions are installed through the container configuration; the obsolete standalone Copilot recommendation was removed and recommendation prompts are disabled in Codespaces. The notebook automatically selected `.venv/bin/python` (`cflabs`, Python 3.12.14), ran all 22 cells without errors, and synced commit `789d890c2a73c05d2176f69ffe4ba8559dfc341b`. No Python-installation or extension-recommendation prompt appeared. Christian's editor preferences installed additional personal extensions, so this remains an instructor-account test. The same configuration correction was pushed to the student test repository; its existing Codespace needs to pull and rebuild.

Remaining account-dependent checks:

- Classroom 50 organisation setup and the service-token step were completed by Christian. The 2026–27 classroom and `python-labs` assignment were created and their publication workflow passed. No current cohort students have been supplied or invited.
- The test student `christian-engels-25` enrolled and accepted the assignment. Their generated repository was verified private, their repository role is Write, and feedback pull request #1 is open. Christian opened its Codespace in the student account. Execution and sync in that student account after rebuilding with the startup fix remain to be checked; individual students’ Codespaces allowance is account-dependent. Classroom teams have read-only access to the private starter template.
- Assistant account access and subscriptions were not tested. They are optional. Native Windows Copilot CLI requires PowerShell 6 or later; the actual optional installers were tested in Codespaces, not on native Windows or macOS.

Official installer and PyPortfolioOpt references are linked in [the optional reference](reference.md).
