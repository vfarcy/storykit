# -*- coding: utf-8 -*-
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

param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Arguments
)

$repoRoot = $PSScriptRoot

Push-Location $repoRoot
try {
    # Construire la commande avec les arguments correctement échappés
    $argList = $Arguments -join "',  '"
    if ($argList) { $argList = "'$argList'" }
    
    # Utiliser des slashes pour les chemins Windows en Python
    $repoRootPy = $repoRoot.Replace('\', '/')
    
    $pythonCmd = @"
import sys
sys.path.insert(0, '$repoRootPy')
sys.argv = ['cli.batch', $argList]
from cli.batch import main
main()
"@
    
    & python -c $pythonCmd
}
finally {
    Pop-Location
}
