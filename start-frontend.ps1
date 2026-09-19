$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath (Join-Path $PSScriptRoot 'flower_classification_frontend')
& npm.cmd run dev -- --host 127.0.0.1 --port 3000 --strictPort
