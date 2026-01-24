# -*- coding: utf-8 -*-
<#
.SYNOPSIS
Charge les alias et fonctions courtes pour StoryKit

.DESCRIPTION
Crée des aliases et des fonctions pour éviter de taper ../tools/ systématiquement.
À importer dans votre profil PowerShell.

.EXAMPLE
. "C:\path\to\tools\load-aliases.ps1"
sk validate
batch list

.INSTALLATION
Pour charger automatiquement cet alias à chaque démarrage de PowerShell :

1. Ouvrir le profil PowerShell :
   notepad $PROFILE

2. Ajouter cette ligne au fichier (créer le fichier s'il n'existe pas) :
   . "C:\Users\vfarc\OneDrive - Groupe ESIEA\Dev\story-repo-polar\tools\load-aliases.ps1"

3. Sauvegarder et redémarrer PowerShell

4. Vérifier que ça fonctionne :
   sk validate

OU en une ligne (exécuter dans PowerShell) :
   if (!(Test-Path $PROFILE)) { New-Item -ItemType File -Path $PROFILE -Force | Out-Null }; Add-Content $PROFILE '. "C:\Users\vfarc\OneDrive - Groupe ESIEA\Dev\story-repo-polar\tools\load-aliases.ps1"'
#>

# Déterminer la racine du repo
$repoRoot = Split-Path -Parent $PSScriptRoot

# Fonction pour détecter le chemin de tools depuis n'importe où
function Get-ToolsPath {
    # Chercher tools/ en remontant depuis le répertoire courant
    $current = Get-Location
    while ($current -ne $current.Parent) {
        if (Test-Path "$current\tools\storykit-run.ps1") {
            return "$current\tools"
        }
        $current = $current.Parent
    }
    # Fallback : utiliser le chemin absolu du repo
    return $repoRoot + "\tools"
}

# ============================================
# 1. Alias rapides pour les scripts
# ============================================

# sk = storykit
New-Alias -Name sk -Value (Get-ToolsPath) + "\storykit-run.ps1" -Force

# b = batch
New-Alias -Name b -Value (Get-ToolsPath) + "\batch-run.ps1" -Force

# ============================================
# 2. Fonctions courtes avec arguments
# ============================================

function sk {
    $toolsPath = Get-ToolsPath
    & "$toolsPath\storykit-run.ps1" @args
}

function batch {
    $toolsPath = Get-ToolsPath
    & "$toolsPath\batch-run.ps1" @args
}

# ============================================
# 3. Navigation rapide
# ============================================

function repo {
    Set-Location $repoRoot
}

function story {
    $current = Get-Location
    while ($current -ne $current.Parent) {
        if (Test-Path "$current\storykit.config.yaml") {
            Set-Location "$current\story"
            return
        }
        $current = $current.Parent
    }
    Write-Host "✗ Impossible de trouver storykit.config.yaml" -ForegroundColor Red
}

function tools {
    $current = Get-Location
    while ($current -ne $current.Parent) {
        if (Test-Path "$current\tools\storykit-run.ps1") {
            Set-Location "$current\tools"
            return
        }
        $current = $current.Parent
    }
    Write-Host "✗ Impossible de trouver le dossier tools/" -ForegroundColor Red
}

function livres {
    $current = Get-Location
    while ($current -ne $current.Parent) {
        if (Test-Path "$current\livre1-truby") {
            Write-Host "Dossiers de projets disponibles :" -ForegroundColor Green
            Get-ChildItem -Path $current -Directory | Where-Object {$_.Name -match "^livre"} | ForEach-Object {
                Write-Host "  - $($_.Name)/" -ForegroundColor Cyan
            }
            return
        }
        $current = $current.Parent
    }
    Write-Host "✗ Impossible de trouver les projets" -ForegroundColor Red
}

# ============================================
# 4. Affichage du statut
# ============================================

Write-Host "✓ Alias StoryKit chargés :" -ForegroundColor Green
Write-Host "  Commandes: sk, batch" -ForegroundColor Cyan
Write-Host "  Navigation: repo, story, tools, livres" -ForegroundColor Cyan
Write-Host ""
Write-Host "Exemples :" -ForegroundColor Yellow
Write-Host "  sk validate" -ForegroundColor White
Write-Host "  sk assemble --target truby7" -ForegroundColor White
Write-Host "  batch draft-variants --chapter ..." -ForegroundColor White
Write-Host "  story" -ForegroundColor White
Write-Host "  livres" -ForegroundColor White
