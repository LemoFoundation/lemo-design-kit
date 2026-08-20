# Rebuild build/lemo-encore-design.zip from skill/lemo-encore-design.
#
# NOT Compress-Archive: Windows PowerShell 5.1 writes entry paths with BACKSLASHES, which the ZIP
# spec forbids (4.4.17.1 - forward slashes only). Some extractors then treat
# "lemo-encore-design\SKILL.md" as one flat filename instead of a folder, and the skill fails to
# load. Build the entries by hand.
#
# Output is gitignored - attach it to a GitHub release rather than committing it.

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

$root = $PSScriptRoot
$src  = Join-Path $root 'skill'
$name = 'lemo-encore-design'
$out  = Join-Path $root "build\$name.zip"

if (-not (Test-Path (Join-Path $src $name))) { throw "missing $src\$name" }

New-Item -ItemType Directory -Force -Path (Split-Path $out) | Out-Null
if (Test-Path $out) { Remove-Item $out -Force }

$zip = [System.IO.Compression.ZipFile]::Open($out, 'Create')
try {
  Get-ChildItem -Path (Join-Path $src $name) -Recurse -File | ForEach-Object {
    $rel = $_.FullName.Substring($src.Length + 1).Replace('\', '/')
    [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip, $_.FullName, $rel) | Out-Null
    Write-Host "  + $rel"
  }
} finally { $zip.Dispose() }

Write-Host "`nBuilt $out"
Write-Host "Attach this to a GitHub release; do not commit it."
