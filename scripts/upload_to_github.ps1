param(
    [Parameter(Mandatory = $true)]
    [string]$RepoUrl
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Set-Location (Split-Path -Parent $PSScriptRoot)

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "Git is not installed or not available in PATH."
}

if (-not (Test-Path .git)) {
    git init
}

git add .
git commit -m "Initial Amazon ops AI agent"
git branch -M main

$existingRemote = git remote
if ($existingRemote -notcontains "origin") {
    git remote add origin $RepoUrl
}

git push -u origin main

