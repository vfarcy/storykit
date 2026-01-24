# -*- coding: utf-8 -*-
<#
.SYNOPSIS
Helper pour lancer storykit CLI avec détection automatique du livre en cours

.DESCRIPTION
Ce script détecte le livre en cours (en cherchant storykit.config.yaml vers le haut)
et lance le CLI StoryKit avec les bonnes variables d'environnement.

.EXAMPLE
./storykit-run.ps1 validate
./storykit-run.ps1 assemble --target truby7
#>

param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Arguments
)

# Détecter le livre en cours
function Find-CurrentBook {
    $current = Get-Location
    $root = Split-Path -Parent $current
    
    while ($current -ne $root) {
        $configPath = Join-Path $current "storykit.config.yaml"
        if (Test-Path $configPath) {
            return $current
        }
        $current = Split-Path -Parent $current
    }
    
    # Fallback: rechercher livre1-truby ou livre2-monsoon en remontant
    $current = Get-Location
    $maxLevels = 5
    for ($i = 0; $i -lt $maxLevels; $i++) {
        if (Test-Path (Join-Path $current "storykit.config.yaml")) {
            return $current
        }
        $parent = Split-Path -Parent $current
        if ($parent -eq $current) { break }  # on est à la racine
        $current = $parent
    }
    
    return $null
}

$repoRoot = Split-Path -Parent $PSScriptRoot
$bookPath = Find-CurrentBook

if (-not $bookPath) {
    Write-Error "Erreur: impossible de détecter le livre en cours (storykit.config.yaml non trouvé)"
    exit 1
}

Write-Host "[*] Livre détecté: $bookPath" -ForegroundColor Cyan

# Lancer le CLI depuis la racine du repo, mais avec le répertoire courant au livre
Push-Location $bookPath
try {
    & python -m cli.storykit $Arguments
}
finally {
    Pop-Location
}
