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

$responsesDir = Join-Path $PSScriptRoot '..' 'out' 'responses'
$promptsDir   = Join-Path $PSScriptRoot '..' 'out' 'prompts'

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
