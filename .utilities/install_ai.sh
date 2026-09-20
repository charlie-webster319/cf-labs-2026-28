#!/usr/bin/env bash
# Optional only: never called by Python setup. Installers do not launch assistants.
set -uo pipefail
failures=0
install_cli() {
    local name="$1" url="$2" runner="$3" installer
    shift 3
    # Codex and Claude must refresh even when an older binary already exists.
    if [[ "$name" == copilot ]] && { command -v "$name" >/dev/null 2>&1 || [[ -x "$HOME/.local/bin/$name" ]]; }; then
        echo "$name is already installed."
        return
    fi
    if ! installer=$(mktemp); then
        echo "OPTIONAL TOOL FAILED: $name (could not create a temporary installer). The labs still work." >&2
        failures=$((failures + 1))
        return 1
    fi
    if curl --fail --show-error --location --retry 2 --connect-timeout 15 --max-time 120 "$url" -o "$installer" && "$runner" "$installer" "$@" </dev/null; then
        echo "$name installed or updated."
    else
        echo "OPTIONAL TOOL FAILED: $name. Retry Install optional AI tools later; the labs still work." >&2
        failures=$((failures + 1))
    fi
    rm "$installer"
}
export CODEX_NON_INTERACTIVE=true
install_cli copilot https://gh.io/copilot-install bash
install_cli codex https://chatgpt.com/codex/install.sh sh --release latest
install_cli claude https://claude.ai/install.sh bash latest
# Codespaces installs these through devcontainer customizations.
if [[ "${1:-}" != '--codespaces' ]]; then
    for extension in OpenAI.chatgpt Anthropic.claude-code; do
        if ! code --install-extension "$extension"; then
            echo "OPTIONAL EXTENSION FAILED: $extension. Install it from VS Code Extensions later." >&2
            failures=$((failures + 1))
        fi
    done
fi
echo "Optional tools finished ($failures failed steps). No sign-in was started. Open a new terminal to use installed CLIs."
[[ "$failures" -eq 0 ]]
