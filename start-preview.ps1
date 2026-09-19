$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$previewPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $previewPython)) {
    throw 'Missing .venv. Create it and install requirements-preview.txt first.'
}
$env:FLOWER_PREVIEW_MODE = '1'
$env:PYTHONIOENCODING = 'utf-8'
& $previewPython -m flask --app flower_classification_backend.backend.app:create_app run --host 127.0.0.1 --port 5001 --no-reload
