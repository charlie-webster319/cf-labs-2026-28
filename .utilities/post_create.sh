#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
bash .utilities/setup_lab.sh
# Optional downloads can fail without failing Codespace creation or Python setup.
bash .utilities/install_ai.sh --codespaces || echo 'Some optional AI tools were unavailable. Your lab environment is ready.'
