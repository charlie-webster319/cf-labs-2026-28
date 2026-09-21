---
name: cf-notebook-help
description: Help students understand, debug or make small requested edits to the corporate finance lab notebooks, including Python errors, unexpected outputs and kernel problems. Use for notebook-specific help rather than general finance explanations or revision quizzes.
---

# Notebook help

Follow the repository's `AGENTS.md`. Paths refer to the repository root. The student may have little programming experience; identify the next small step and explain why it helps.

## Inspect the relevant evidence

Use the cell, error or output already supplied. If reading the notebook from disk, ask the student to save first unless they have already confirmed it is saved. Read the relevant saved cells, their dependencies and outputs through the `jupyter` MCP tools when available. Those tools do not share the live VS Code kernel. If MCP is unavailable, use the assistant's file tools for a bounded notebook inspection or work from the pasted cell and error; do not require another installation.

Distinguish a code problem from an environment problem or cells run out of order. For setup failures, refer to **Terminal → Run Task → Setup lab environment**. For kernel problems, select **Corporate Finance Labs (.venv)** or the Python environment with the `.venv` path. Use uv and the existing `.venv`; preserve the locked teaching packages.

## Explain and make a small correction

Explain the cause in plain language and show the smallest useful correction. Edit a saved cell only when the student requested a change and has paused typing. Preserve cell order, worked examples, dataset and unrelated work. Identify the affected cell by its heading or nearby content and tell the student which cells to rerun.

After an external edit, have VS Code reload the saved file while preserving any unsaved work. Let the student run the relevant cells in the notebook. Do not use `notebook_execute_cell`: no separate Jupyter server is configured. For an explicitly requested independent execution check, use the lab `.venv` and a copy under `outputs/`, explaining that this uses a separate kernel.

Interpret the output financially, using `.assistant-resources/README.md` when lecture context helps. Never claim a correction ran successfully without execution evidence. A saved or edited file is not proof of a GitHub upload; use **Check whether your work has synced** when the student asks about saving online. Preserve the existing sync helper and never force-push or resolve conflicts automatically.
