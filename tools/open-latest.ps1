param(
    [ValidateSet('notepad','code')]
    [string]$Editor = 'notepad'
)

$promptsDir = Join-Path $PSScriptRoot '..' 'out' 'prompts'
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
