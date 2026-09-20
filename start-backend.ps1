$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$flowerPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $flowerPython)) {
    throw 'Create .venv and install requirements.txt first.'
}
$env:FLOWER_PREVIEW_MODE = '0'
$env:PYTHONIOENCODING = 'utf-8'
& $flowerPython scripts/download_flower_model.py
if ($LASTEXITCODE -ne 0) { throw 'Model verification failed. See docs/FLOWER_MODEL.md.' }
& $flowerPython -m flask --app flower_classification_backend.backend.app:create_app run --host 127.0.0.1 --port 5001 --no-reload
