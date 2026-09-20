#!/usr/bin/env bash
# Runs on first creation and every later container start. Never starts a login.
set -euo pipefail
cd "$(dirname "$0")/.."
# Optional downloads must not make the container or the Python lab unavailable.
bash .utilities/install_ai.sh --codespaces || echo 'Some optional AI tools could not be installed or updated. The labs still work; retry Install optional AI tools later.' >&2
# Warm the optional MCP dependencies. Client startup also retries this sync.
.tools/uv/uv sync --locked --inexact --group notebook-mcp || echo 'Optional notebook MCP setup failed. The labs still work; the assistant will retry when its notebook tools start.' >&2
