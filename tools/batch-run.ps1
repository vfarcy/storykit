# -*- coding: utf-8 -*-
param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Arguments
)

<#
.SYNOPSIS
Helper pour lancer les commandes batch depuis n'importe où

.DESCRIPTION
Ce script lance les commandes batch (cli.batch) depuis la racine du repo,
peu importe le répertoire courant.

.EXAMPLE
./batch-run.ps1 list --limit 10
./batch-run.ps1 draft-variants --chapter story/drafting/Chap01.md --styles minimaliste --wait
./batch-run.ps1 status msgbatch_XXXXX
#>

# Force l'encodage UTF-8 pour PowerShell
$env:PYTHONIOENCODING = 'utf-8'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# $PSScriptRoot pointe vers tools/, donc repo root = parent
$repoRoot = Split-Path -Parent $PSScriptRoot
$originalCwd = Get-Location  # On veut respecter le chemin depuis lequel l'utilisateur lance la commande

Push-Location $repoRoot
try {
    # Construire la commande avec les arguments correctement échappés
    $argList = $Arguments -join "',  '"
    if ($argList) { $argList = "'$argList'" }
    
    # Utiliser des slashes pour les chemins Windows en Python
    # Forcer les slashes pour éviter les problèmes d'escape Python
    $repoRootPy = $repoRoot -replace '\\','/'
    $originalCwdPy = $originalCwd.Path -replace '\\','/'
    
    $pythonCmd = @"
import os, sys
# Garder l'emplacement où l'utilisateur était (pour les chemins relatifs de chapitres)
os.chdir(r'$originalCwdPy')
sys.path.insert(0, r'$repoRootPy')
sys.argv = ['cli.batch', $argList]
from cli.batch import main
main()
"@
    
    & python -c $pythonCmd
}
finally {
    Pop-Location
}
