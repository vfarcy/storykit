param(
    [ValidateSet('notepad','code')]
    [string]$Editor = 'notepad'
)

$responsesDir = Join-Path $PSScriptRoot '..' 'out' 'responses'
if (-not (Test-Path $responsesDir)) {
    Write-Error "Dossier introuvable: $responsesDir"
    exit 1
}

$latest = Get-ChildItem $responsesDir -Filter *.md -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if (-not $latest) {
    Write-Error "Aucun fichier .md trouvé dans $responsesDir"
    exit 1
}

switch ($Editor.ToLower()) {
    'notepad' { notepad $latest.FullName }
    'code'    { code $latest.FullName }
    default   { notepad $latest.FullName }
}
