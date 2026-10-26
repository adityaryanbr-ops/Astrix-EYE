# Devpost Learn AI Basics — skill pack installer
# https://github.com/challengepost/learn-ai-basics
# Requires Node.js and Git.

$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)

Write-Host "Installing challengepost/learn-ai-basics skills..."
npx skills add challengepost/learn-ai-basics --all -y

$src = Join-Path $PWD ".agents\skills"
$dst = Join-Path $PWD ".cursor\skills"
if (-not (Test-Path $src)) {
    Write-Error ".agents/skills not found after install."
}
New-Item -ItemType Directory -Force -Path $dst | Out-Null
Get-ChildItem $src -Directory | ForEach-Object {
    $target = Join-Path $dst $_.Name
    if (Test-Path $target) { Remove-Item -Recurse -Force $target }
    Copy-Item -Recurse $_.FullName $target
}
Write-Host "Synced skills to .cursor/skills for Cursor."
