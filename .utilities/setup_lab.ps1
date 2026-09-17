$ErrorActionPreference = 'Stop'
$step = 'finding the lab folder'
try {
    $root = Split-Path $PSScriptRoot -Parent
    Set-Location -LiteralPath $root
    $uvVersion = '0.12.15'
    $uv = Join-Path $root '.tools/uv/uv.exe'
    $step = 'installing the lab copy of uv'
    if (!(Test-Path $uv) -or ((& $uv --version) -notlike "uv $uvVersion*")) {
        $installer = Join-Path ([IO.Path]::GetTempPath()) ([IO.Path]::GetRandomFileName() + '.ps1')
        Invoke-WebRequest "https://astral.sh/uv/$uvVersion/install.ps1" -OutFile $installer -UseBasicParsing
        $env:UV_INSTALL_DIR = Join-Path $root '.tools/uv'
        $env:UV_NO_MODIFY_PATH = '1'
        & powershell -NoProfile -ExecutionPolicy Bypass -File $installer
        if ($LASTEXITCODE -ne 0) { throw 'uv installer failed' }
        Remove-Item -LiteralPath $installer
    }
    $step = 'installing Python and the locked lab packages'
    $env:UV_PROJECT_ENVIRONMENT = Join-Path $root '.venv'
    $env:UV_PYTHON_PREFERENCE = 'only-managed'
    & $uv sync --locked
    if ($LASTEXITCODE -ne 0) { throw 'uv sync failed' }
    $step = 'registering the lab notebook kernel'
    & "$root/.venv/Scripts/python.exe" -m ipykernel install --prefix "$root/.venv" --name cflabs --display-name 'Corporate Finance Labs (.venv)'
    if ($LASTEXITCODE -ne 0) { throw 'kernel registration failed' }
    Write-Host 'Setup complete. Open the notebook and select Corporate Finance Labs (.venv), or Python Environments > .venv.'
} catch {
    Write-Error "Setup failed while ${step}: $_. Run Setup lab environment again; if it still fails, show this message to your tutor."
    exit 1
}
