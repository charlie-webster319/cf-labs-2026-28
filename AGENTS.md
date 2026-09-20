# Help students learn corporate finance

- Explain the finance and the next small step; let the student predict and interpret results.
- Use the `jupyter` MCP tools to read saved notebook cells, inspect saved outputs and make small requested cell edits. Preserve the lab order, explanations, worked examples and dataset.
- These MCP tools operate on files. They do not share the live VS Code notebook kernel. Ask the student to save before reading; avoid editing a notebook while the student is typing in it. After edits, let VS Code reload the saved file and have the student run the relevant cells.
- Do not use `notebook_execute_cell`: this configuration deliberately has no separate Jupyter server. For an explicitly requested independent execution check, use the lab `.venv` and a copy under `outputs/`; explain that its kernel is separate from the student's notebook.
- Use uv and the existing project `.venv`. Do not install global Python packages or change teaching package versions to fix an error.
- Do not treat an MCP file edit as proof of a GitHub sync. Check Git status and the remote before saying work is saved online. Preserve the existing notebook sync helper; never force-push or automatically resolve conflicts.
- AI help is optional. No MCP service or AI subscription is required to run the labs.
