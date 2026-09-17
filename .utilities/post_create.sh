#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
bash .utilities/setup_lab.sh
# VS Code also probes for a base interpreter, excluding virtual environments.
# Expose the SAME uv-managed runtime already installed by sync, using local links.
if ! UV_PYTHON_BIN_DIR="$PWD/.tools/python" .tools/uv/uv python install --offline --default --preview-features python-install-default "$(cat .python-version)"; then
    echo 'Codespaces setup failed while exposing the managed Python runtime to VS Code. Rebuild the container to retry.' >&2
    exit 1
fi
# Optional downloads can fail without failing Codespace creation or Python setup.
bash .utilities/install_ai.sh --codespaces || echo 'Some optional AI tools were unavailable. Your lab environment is ready.'
