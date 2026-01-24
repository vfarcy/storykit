param(
    [ValidateSet('notepad','code')]
    [string]$Editor = 'notepad'
)

# Détecter le livre courant en cherchant storykit.config.yaml
function Find-BookRoot {
    $current = Get-Location
    while ($current) {
        $configPath = Join-Path $current 'storykit.config.yaml'
        if (Test-Path $configPath) { return $current }
        $parent = Split-Path $current -Parent
        if ($parent -eq $current) { break }  # Racine atteinte
        $current = $parent
    }
    return $null
}

$bookRoot = Find-BookRoot
if (-not $bookRoot) {
    Write-Error "Aucun livre détecté (storykit.config.yaml introuvable). Lancez depuis un répertoire livre*/ ou ses sous-dossiers."
    exit 1
}

$promptsDir = Join-Path $bookRoot 'out' 'prompts'
if (-not (Test-Path $promptsDir)) {
    Write-Error "Dossier introuvable: $promptsDir"
    exit 1
}

$latest = Get-ChildItem $promptsDir -Filter *.md -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if (-not $latest) {
    Write-Error "Aucun fichier .md trouvé dans $promptsDir"
    exit 1
}

switch ($Editor.ToLower()) {
    'notepad' { notepad $latest.FullName }
    'code'    { code $latest.FullName }
    default   { notepad $latest.FullName }
}
