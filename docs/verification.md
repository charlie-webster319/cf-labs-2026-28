# Implementation and verification — 17 September 2026

Changes are local for review. Nothing was committed, pushed or published by this implementation.

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

## Checks still requiring a published test branch or live account

The Actions workflow in `.github/workflows/labs.yml` is configured for clean setup, setup reruns, regression tests, full notebook execution and financial validation on Linux, macOS and Windows. It deliberately checks out into `lab workspace` to exercise spaces. It has **not run remotely** for these unpushed changes. Native Windows and Linux installation/execution remain unverified; macOS PowerShell tests do not establish native Windows compatibility.

A fresh Codespace has **not** been created. Docker is installed locally but its daemon was unavailable, so no local container check was claimed. Before student release:

1. Create a Codespace from the reviewed test branch. Confirm automatic setup finishes and the first code cell runs with `.venv` / **Corporate Finance Labs (.venv)**.
2. Check installed extensions: Python, Jupyter, Run On Save, Copilot, Codex and Claude. In a new terminal, run `copilot --version`, `codex --version` and `claude --version`; these checks do not require signing in. Actual optional installers were not run on Christian's Mac.
3. In a writable student test copy, edit/save a notebook and run **Check whether your work has synced**. Verify the changed notebook on GitHub. The helper passed isolated Git tests, but real VS Code save events, extension loading, authentication and GitHub write permissions have not been exercised.
4. Check account-dependent Copilot availability separately. Neither assistant login nor a subscription is required for notebook execution. On native Windows, Copilot CLI requires PowerShell 6 or later.

Official installer and PyPortfolioOpt references are linked in [the optional reference](reference.md).
