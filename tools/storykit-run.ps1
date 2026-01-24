# -*- coding: utf-8 -*-
param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Arguments
)

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

# Force l'encodage UTF-8 pour PowerShell
$env:PYTHONIOENCODING = 'utf-8'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# $PSScriptRoot pointe vers tools/, donc repo root = parent
$repoRoot = Split-Path -Parent $PSScriptRoot

# Détecter le livre en cours en cherchant depuis le répertoire courant
function Find-CurrentBook {
    $current = (Get-Location).Path
    
    # Chercher storykit.config.yaml en montant l'arborescence
    while ($current) {
        $configPath = Join-Path $current "storykit.config.yaml"
        if (Test-Path $configPath) {
            return $current
        }
        
        $parent = Split-Path -Parent $current
        if ($parent -eq $current -or -not $parent) { 
            break  # on est à la racine
        }
        $current = $parent
    }
    
    return $null
}

$bookPath = Find-CurrentBook

if (-not $bookPath) {
    Write-Host "✗ ERREUR : Impossible de détecter le livre en cours" -ForegroundColor Red
    Write-Host "   Le fichier storykit.config.yaml n'a pas été trouvé" -ForegroundColor Yellow
    Write-Host "" -ForegroundColor White
    Write-Host "   Pour utiliser StoryKit, naviguez vers un livre :" -ForegroundColor Cyan
    Write-Host "   - cd livre1-truby" -ForegroundColor White
    Write-Host "   - cd livre2-monsoon" -ForegroundColor White
    Write-Host "   - ou un autre dossier contenant storykit.config.yaml" -ForegroundColor White
    Write-Host "" -ForegroundColor White
    Write-Host "   Puis relancez : sk validate" -ForegroundColor Green
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



