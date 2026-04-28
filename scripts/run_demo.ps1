Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Set-Location (Split-Path -Parent $PSScriptRoot)

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
amazon-agent ads --report examples/sample_ads_report.csv --out output/ads_analysis.json

Write-Host "Demo finished. See output/ads_analysis.json"

