$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$flowerPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $flowerPython)) {
    throw 'Create .venv and install requirements-flower.txt first.'
}
$env:GC_PREVIEW_MODE = '0'
$env:PYTHONIOENCODING = 'utf-8'
& $flowerPython -m flask --app flower_classification_backend.backend.app:create_app run --host 127.0.0.1 --port 5001 --no-reload
