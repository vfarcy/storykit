param(
    [ValidateSet('notepad','code')]
    [string]$Editor = 'notepad',
    [bool]$FallbackToPrompt = $true
)

function Open-File([string]$path) {
    switch ($Editor.ToLower()) {
        'code'    { code $path }
        default   { notepad $path }
    }
}

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

$responsesDir = Join-Path $bookRoot 'out' 'responses'
$promptsDir   = Join-Path $bookRoot 'out' 'prompts'

if (-not (Test-Path $responsesDir)) {
    if ($FallbackToPrompt -and (Test-Path $promptsDir)) {
        Write-Warning "Aucun dossier de réponses IA trouvé (mode dry-run probable). Ouverture du dernier prompt à la place."
        $latestPrompt = Get-ChildItem $promptsDir -Filter *.md -ErrorAction SilentlyContinue |
            Sort-Object LastWriteTime -Descending |
            Select-Object -First 1
        if ($latestPrompt) { Open-File $latestPrompt.FullName; exit 0 }
    }
    Write-Error "Dossier introuvable: $responsesDir"
    exit 1
}

$latest = Get-ChildItem $responsesDir -Filter *.md -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if (-not $latest) {
    if ($FallbackToPrompt -and (Test-Path $promptsDir)) {
        Write-Warning "Aucune réponse IA trouvée. Ouverture du dernier prompt à la place."
        $latestPrompt = Get-ChildItem $promptsDir -Filter *.md -ErrorAction SilentlyContinue |
            Sort-Object LastWriteTime -Descending |
            Select-Object -First 1
        if ($latestPrompt) { Open-File $latestPrompt.FullName; exit 0 }
    }
    Write-Error "Aucun fichier .md trouvé dans $responsesDir"
    exit 1
}

Open-File $latest.FullName
