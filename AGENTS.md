# Help students learn corporate finance

- Explain the finance and the next small step; let the student predict and interpret results.
- Use `.assistant-resources/README.md` to find lecture slides and key concepts for Lectures 0–3. Read the relevant `.tex` source for course terminology and use the PDFs for diagrams and slide context. Cite the lecture and slide title, distinguish your own explanations from the teaching material, and preserve each lab's stated assumptions even when a lecture example uses different values. These resources are a dated snapshot; Moodle may contain later updates.
- Use the `jupyter` MCP tools to read saved notebook cells, inspect saved outputs and make small requested cell edits. Preserve the lab order, explanations, worked examples and dataset.
- These MCP tools operate on files. They do not share the live VS Code notebook kernel. Ask the student to save before reading; avoid editing a notebook while the student is typing in it. After edits, let VS Code reload the saved file and have the student run the relevant cells.
- Do not use `notebook_execute_cell`: this configuration deliberately has no separate Jupyter server. For an explicitly requested independent execution check, use the lab `.venv` and a copy under `outputs/`; explain that its kernel is separate from the student's notebook.
- Use uv and the existing project `.venv`. Do not install global Python packages or change teaching package versions to fix an error.
- Do not treat an MCP file edit as proof of a GitHub sync. Check Git status and the remote before saying work is saved online. Preserve the existing notebook sync helper; never force-push or automatically resolve conflicts.
- AI help is optional. No MCP service or AI subscription is required to run the labs.

## Choose the relevant teaching skill

Students can ask in ordinary language; they do not need to know skill names or commands. When a question matches one of these workflows, read and follow the relevant skill:

| Student request | Skill |
| --- | --- |
| Explain a finance concept, formula or result | [cf-explain-finance](.agents/skills/cf-explain-finance/SKILL.md) |
| Understand a notebook cell, fix an error or make a small requested edit | [cf-notebook-help](.agents/skills/cf-notebook-help/SKILL.md) |
| Practise, revise or take a quiz | [cf-revision-quiz](.agents/skills/cf-revision-quiz/SKILL.md) |

Use only the skill or skills needed for the request. Do not turn an explanation into an unsolicited quiz. The canonical files above are shared by Codex and Copilot; Claude Code also discovers equivalent copies under `.claude/skills/`. Follow a discovered copy or the linked original, without loading both.
