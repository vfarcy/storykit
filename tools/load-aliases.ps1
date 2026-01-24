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

# Vérifier que le repo est valide
if (!(Test-Path "$repoRoot\livre1-truby\storykit.config.yaml")) {
    Write-Host "✗ ERREUR : Impossible de trouver le répertoire du projet StoryKit" -ForegroundColor Red
    Write-Host "   Assurez-vous d'être dans le repository story-repo-polar" -ForegroundColor Yellow
    Write-Host "   Chemin attendu : $repoRoot" -ForegroundColor Gray
    break
}

# Fonction pour détecter le chemin de tools depuis n'importe où
function Get-ToolsPath {
    # Chercher tools/ en remontant depuis le répertoire courant
    $current = (Get-Location).Path
    while ($current) {
        if (Test-Path "$current\tools\storykit-run.ps1") {
            return "$current\tools"
        }
        $parent = Split-Path -Parent $current
        if ($parent -eq $current -or -not $parent) { 
            break  # on est à la racine
        }
        $current = $parent
    }
    # Aucun repo trouvé
    return $null
}

# ============================================
# Fonctions courtes avec arguments
# ============================================

# sk = storykit (détecte le dossier tools automatiquement)
function sk {
    $toolsPath = Get-ToolsPath
    if (-not $toolsPath) {
        Write-Host "✗ ERREUR : Vous n'êtes pas dans un répertoire valide" -ForegroundColor Red
        Write-Host "   Naviguez vers un livre (livre1-truby, livre2-monsoon, etc.)" -ForegroundColor Yellow
        Write-Host "   ou vers un sous-dossier du repository" -ForegroundColor Gray
        return
    }
    & "$toolsPath\storykit-run.ps1" @args
}

# batch = cli batch (fonctionne depuis la racine du repo)
function batch {
    $toolsPath = Get-ToolsPath
    if (-not $toolsPath) {
        # Fallback : utiliser le chemin absolu si on est vraiment loin
        $toolsPath = "$(Split-Path -Parent $PSScriptRoot)\tools"
    }
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
