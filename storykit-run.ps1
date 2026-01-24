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

$repoRoot = $PSScriptRoot

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
# Le répertoire courant doit être celui du livre pour la détection de config
Push-Location $bookPath
try {
    # Construire la commande avec les arguments correctement échappés
    $argList = $Arguments -join "',  '"
    if ($argList) { $argList = "'$argList'" }
    
    # Utiliser des slashes pour les chemins Windows en Python
    $repoRootPy = $repoRoot.Replace('\', '/')
    
    $pythonCmd = @"
import sys; sys.path.insert(0, '$repoRootPy'); from cli.storykit import main; main([$argList])
"@
    
    & python -c $pythonCmd
}
finally {
    Pop-Location
}



