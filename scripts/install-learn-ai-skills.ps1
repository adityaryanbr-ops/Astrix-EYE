# Install Devpost Learn AI Basics skills for Cursor (and other agents).
# Requires: Node.js, Git
# https://github.com/challengepost/learn-ai-basics

$ErrorActionPreference = "Stop"
Set-Location (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent)
if (-not (Test-Path (Join-Path $PSScriptRoot ".."))) { Set-Location (Resolve-Path (Join-Path $PSScriptRoot "..")) }
Set-Location (Resolve-Path (Join-Path $PSScriptRoot ".."))
Write-Host "Installing skills into $(Get-Location) ..."
npx skills add challengepost/learn-ai-basics --all -y
Write-Host "Done. Cursor skills: .cursor/skills/1-start ... 6-ship"
