#!/usr/bin/env bash
set -euo pipefail
step='finding the lab folder'
trap 'echo "Setup failed while ${step}. Run Setup lab environment again; if it still fails, show this message to your tutor." >&2' ERR
cd "$(dirname "$0")/.."
root="$PWD"
uv_version=0.12.15
uv="$root/.tools/uv/uv"
step='installing the lab copy of uv'
if [[ ! -x "$uv" ]] || [[ "$("$uv" --version)" != "uv $uv_version"* ]]; then
    installer=$(mktemp)
    curl --fail --show-error --location --retry 2 "https://astral.sh/uv/$uv_version/install.sh" -o "$installer"
    UV_INSTALL_DIR="$root/.tools/uv" UV_NO_MODIFY_PATH=1 sh "$installer"
    rm "$installer"
fi
step='installing Python and the locked lab packages'
export UV_PROJECT_ENVIRONMENT="$root/.venv"
export UV_PYTHON_PREFERENCE=only-managed
"$uv" sync --locked
step='registering the lab notebook kernel'
"$root/.venv/bin/python" -m ipykernel install --prefix "$root/.venv" --name cflabs --display-name 'Corporate Finance Labs (.venv)'
echo 'Setup complete. Open the notebook and select Corporate Finance Labs (.venv), or Python Environments > .venv.'
