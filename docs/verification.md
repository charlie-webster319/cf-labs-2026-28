# Implementation and verification — 17 September 2026

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
