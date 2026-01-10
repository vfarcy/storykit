# Tools — Scripts d'aide (PowerShell)

Petits utilitaires pour accéder rapidement aux fichiers générés par StoryKit sous Windows PowerShell.

## Prérequis
- Windows PowerShell
- `code` (VS Code) doit être dans le `PATH` si vous utilisez l'éditeur `code`; sinon, `notepad` est utilisé.
- Si nécessaire, autoriser l'exécution des scripts dans la session courante:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

## Scripts

### 1) Ouvrir le dernier prompt généré
- **Chemin**: `tools/open-latest.ps1`
- **But**: ouvre le plus récent `.md` dans `out/prompts`
- **Usage**:

```powershell
# Notepad (par défaut)
./tools/open-latest.ps1

# VS Code
./tools/open-latest.ps1 -Editor code
```

### 2) Ouvrir la dernière réponse IA
- **Chemin**: `tools/open-latest-response.ps1`
- **But**: ouvre le plus récent `.md` dans `out/responses`
- **Usage**:

```powershell
# Notepad (par défaut)
./tools/open-latest-response.ps1

# VS Code
./tools/open-latest-response.ps1 -Editor code
```

Notes:
- En mode **dry-run**, il n'y a pas de `out/responses`. Le script **bascule automatiquement** vers le dernier prompt (`out/prompts`) si `FallbackToPrompt` est activé (par défaut).
- Pour forcer l'erreur si aucune réponse n'est disponible, désactivez le fallback: `./tools/open-latest-response.ps1 -FallbackToPrompt:$false`.

## Options communes
- `-Editor`: `notepad` (défaut) ou `code` (VS Code)

## Notes
- Ces scripts ciblent Windows PowerShell. Sur macOS/Linux, adaptez avec `bash`/`zsh` et les utilitaires disponibles.
