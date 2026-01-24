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
- **But**: ouvre le plus récent `.md` dans `livre/out/prompts` (détecte automatiquement le livre courant)
- **Usage**:

```powershell
# Depuis n'importe quel répertoire du livre (livre1-truby, livre2-monsoon, etc.)

# Notepad (par défaut)
../../tools/open-latest.ps1

# VS Code
../../tools/open-latest.ps1 -Editor code
```

### 2) Ouvrir la dernière réponse IA
- **Chemin**: `tools/open-latest-response.ps1`
- **But**: ouvre le plus récent `.md` dans `livre/out/responses` (détecte automatiquement le livre courant)
- **Usage**:

```powershell
# Depuis n'importe quel répertoire du livre

# Notepad (par défaut)
../../tools/open-latest-response.ps1

# VS Code
../../tools/open-latest-response.ps1 -Editor code
```

Notes:
- En mode **dry-run**, il n'y a pas de `livre/out/responses`. Le script **bascule automatiquement** vers le dernier prompt (`livre/out/prompts`) si `FallbackToPrompt` est activé (par défaut).
- Pour forcer l'erreur si aucune réponse n'est disponible, désactivez le fallback: `../../tools/open-latest-response.ps1 -FallbackToPrompt:$false`.

## Options communes
- `-Editor`: `notepad` (défaut) ou `code` (VS Code)

## Scripts helpers du CLI (depuis n'importe quel répertoire)

### 3) Helper StoryKit CLI
- **Chemin**: `../storykit-run.ps1`
- **But**: lancer les commandes CLI StoryKit depuis n'importe quel répertoire (même sans .venv activé)
- **Usage**:

```powershell
# Détecte automatiquement le livre courant
../storykit-run.ps1 validate
../storykit-run.ps1 assemble --target premise
../storykit-run.ps1 assemble --target truby7
../storykit-run.ps1 assemble --target draft --chapter 1
```

### 4) Helper Batch CLI
- **Chemin**: `../batch-run.ps1`
- **But**: lancer les commandes batch depuis n'importe quel répertoire (même sans .venv activé)
- **Usage**:

```powershell
# Détecte automatiquement le livre courant
../batch-run.ps1 list --limit 10
../batch-run.ps1 download msgbatch_XXXX
../batch-run.ps1 status msgbatch_XXXX
```

## Notes
- Ces scripts ciblent Windows PowerShell. Sur macOS/Linux, adaptez avec `bash`/`zsh` et les utilitaires disponibles.
- Les helpers (`storykit-run.ps1`, `batch-run.ps1`) détectent automatiquement le livre en remontant depuis le répertoire courant pour trouver `storykit.config.yaml`.

