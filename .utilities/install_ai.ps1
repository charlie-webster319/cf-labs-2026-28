# Optional only: never called by Python setup. Installers do not launch assistants.
$ErrorActionPreference = 'Stop'
$failures = 0
function Install-Optional($name, $action) {
    try { & $action; Write-Host "$name installed or already available." }
    catch { Write-Warning "OPTIONAL TOOL FAILED: ${name}: $_. Retry Install optional AI tools later; the labs still work."; $script:failures++ }
}
Install-Optional 'Copilot CLI' {
    if (!(Get-Command copilot -ErrorAction SilentlyContinue)) {
        & winget install --id GitHub.Copilot --exact --silent --accept-package-agreements --accept-source-agreements
        if ($LASTEXITCODE -ne 0) { throw 'WinGet failed. See https://docs.github.com/en/copilot/how-tos/set-up/install-copilot-cli' }
    }
}
$env:CODEX_NON_INTERACTIVE = 'true'
foreach ($tool in @(@('codex','https://chatgpt.com/codex/install.ps1'), @('claude','https://claude.ai/install.ps1'))) {
    Install-Optional $tool[0] {
        if (!(Get-Command $tool[0] -ErrorAction SilentlyContinue)) {
            $installer = Join-Path ([IO.Path]::GetTempPath()) ([IO.Path]::GetRandomFileName() + '.ps1')
            Invoke-WebRequest $tool[1] -OutFile $installer -UseBasicParsing
            & powershell -NoProfile -ExecutionPolicy Bypass -File $installer
            if ($LASTEXITCODE -ne 0) { throw 'Installer failed' }
            Remove-Item -LiteralPath $installer
        }
    }
}
foreach ($extension in @('OpenAI.chatgpt', 'Anthropic.claude-code')) {
    Install-Optional $extension {
        & code --install-extension $extension
        if ($LASTEXITCODE -ne 0) { throw 'Install this extension from VS Code Extensions' }
    }
}
Write-Host "Optional tools finished ($failures failed steps). No sign-in was started. Open a new terminal to use installed CLIs. Copilot CLI on Windows requires PowerShell 6 or later."
if ($failures -gt 0) { exit 1 }
