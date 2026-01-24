# -*- coding: utf-8 -*-
<#
.SYNOPSIS
Helper pour lancer storykit CLI avec détection automatique du livre en cours

.DESCRIPTION
Ce script détecte le livre en cours (en cherchant storykit.config.yaml vers le haut)
et lance le CLI StoryKit avec le répertoire courant approprié.

.EXAMPLE
./storykit-run.ps1 validate
./storykit-run.ps1 assemble --target truby7
#>

param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Arguments
)

$repoRoot = Split-Path -Parent $PSScriptRoot

# Détecter le livre en cours en cherchant depuis le répertoire courant
function Find-CurrentBook {
    $current = Get-Location
    
    # Chercher storykit.config.yaml en montant l'arborescence
    while ($true) {
        $configPath = Join-Path $current "storykit.config.yaml"
        if (Test-Path $configPath) {
            return $current
        }
        
        $parent = Split-Path -Parent $current
        if ($parent -eq $current) { 
            break  # on est à la racine
        }
        $current = $parent
    }
    
    return $null
}

$bookPath = Find-CurrentBook

if (-not $bookPath) {
    Write-Error "Erreur: impossible de détecter le livre en cours (storykit.config.yaml non trouvé)"
    exit 1
}

$bookName = Split-Path -Leaf $bookPath
Write-Host "[*] Livre détecté: $bookName" -ForegroundColor Cyan

# Changer le répertoire courant au livre et lancer le CLI
# En utilisant un wrapper Python qui ajoute le repo root au sys.path
Push-Location $bookPath
try {
    # Écrire un wrapper temporaire pour charger le module avec le bon sys.path
    $wrapperCode = @"
if __name__ == '__main__':
    import sys
    import os
    # Ajouter le repo root au sys.path AVANT d'importer
    repo_root = r'$repoRoot'
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)
    
    from cli.storykit import main
    main($($Arguments | ConvertTo-Json))
"@
    
    # Lancer le wrapper
    & python -c $wrapperCode
}
finally {
    Pop-Location
}



