# Tools — Scripts d'aide

Utilitaires pour accéder rapidement aux fichiers générés par StoryKit.

## Compatibilité par OS

| Script | Windows | Linux | macOS |
|--------|---------|-------|-------|
| `storykit-run` | `.ps1` ✅ | `.sh` ✅ | `.sh` ✅ |
| `batch-run` | `.ps1` ✅ | `.sh` ✅ | `.sh` ✅ |
| `open-latest` | `.ps1` ✅ | — | — |
| `open-latest-response` | `.ps1` ✅ | — | — |

## Prérequis

**Windows:**
- Windows PowerShell ou PowerShell Core
- `code` (VS Code) doit être dans le `PATH` si vous utilisez l'éditeur `code`; sinon, `notepad` est utilisé.
- Si nécessaire, autoriser l'exécution des scripts dans la session courante:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

**Linux / macOS:**
- Bash shell
- Rendre les scripts exécutables:

```bash
chmod +x tools/storykit-run.sh tools/batch-run.sh
```

## Scripts

### 1) Helpers d'exécution (multiplateforme)

#### Windows: `storykit-run.ps1` / `batch-run.ps1`
- **But**: exécuter les commandes CLI depuis n'importe quel répertoire du projet
- **Encodage**: force UTF-8 automatiquement
- **Usage**:

```powershell
# Depuis livre1-truby, livre2-monsoon, etc.
../storykit-run.ps1 validate
../storykit-run.ps1 assemble --target premise
../batch-run.ps1 list --limit 10
../batch-run.ps1 draft-variants --chapter story/drafting/Chap01.md --styles minimaliste
```

#### Linux/macOS: `storykit-run.sh` / `batch-run.sh`
- **But**: exécuter les commandes CLI depuis n'importe quel répertoire du projet
- **Encodage**: force UTF-8 automatiquement
- **Usage**:

```bash
# Depuis livre1-truby, livre2-monsoon, etc.
../storykit-run.sh validate
../storykit-run.sh assemble --target premise
../batch-run.sh list --limit 10
../batch-run.sh draft-variants --chapter story/drafting/Chap01.md --styles minimaliste
```

### 2) Ouvrir le dernier prompt généré (Windows)
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

### 3) Ouvrir la dernière réponse IA (Windows)
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

## Notes
- Les helpers (`storykit-run.ps1`, `batch-run.ps1`, `storykit-run.sh`, `batch-run.sh`) détectent automatiquement le livre en remontant depuis le répertoire courant pour trouver `storykit.config.yaml`.
- Sur macOS/Linux, utilisez les versions `.sh` des helpers.
- Windows PowerShell nécessite parfois : `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned`

