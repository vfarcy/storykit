# StoryKit Batch Processing — Guide complet

## Vue d'ensemble

Le mode **batch** de StoryKit utilise l'API Message Batches de Claude pour générer du contenu en masse avec **50% de réduction de coût** par rapport aux appels standards.

**Avantages :**
- 💰 Coût réduit de 50%
- ⚡ Traitement asynchrone (24h max)
- 📦 Génération en masse (jusqu'à 10 000 requêtes)
- 🔄 Résilience (retry automatique)

**Cas d'usage :**
- Variations stylistiques d'un même chapitre
- Recherche documentaire massive
- Génération de chapitres multiples
- Tests de tonalités narratives

---

## Prérequis

1. **Environnement virtuel activé** avec `anthropic` installé :
   ```powershell
   pip install anthropic
   ```

2. **Clé API Claude** dans `.env` :
   ```env
   ANTHROPIC_API_KEY=sk-ant-...
   ```

3. **Configuration** dans `story/config/storykit.config.yaml` :
   ```yaml
   ai:
     provider: claude  # PAS dry-run pour les batchs
     model: "claude-sonnet-4-5-20250929"
   ```

---

## Commandes disponibles

### 1. `draft-variants` — Variations stylistiques

Génère plusieurs versions d'un même chapitre avec des tonalités différentes.

**Syntaxe :**
```powershell
python -m cli.batch draft-variants `
  --chapter <chemin_vers_chapitre.md> `
  --styles "style1,style2,style3" `
  [--wait]
```

**Paramètres :**
- `--chapter` : Chemin vers le fichier markdown du chapitre source
- `--styles` : Tonalités séparées par virgules (ex: "mélancolique,brutal,poétique,minimaliste")
- `--wait` : (optionnel) Attend la fin du traitement avant de terminer

**Exemple :**
```powershell
python -m cli.batch draft-variants `
  --chapter story/drafting/LeSilenceDesAlgorithmes/20260118_213305_draft_response.md `
  --styles "mélancolique,brutal,poétique,minimaliste" `
  --wait
```

**Sortie :**
- Fichiers générés dans `story/drafting/<titre_histoire>/`
- Nommage : `YYYYMMDD_HHMMSS_draft_variant_<style>.md`
- Métadonnées dans `story/drafting/batches/msgbatch_<id>_metadata.json`

---

### 2. `research` — Recherche documentaire massive

Génère plusieurs fiches de recherche structurées sur un thème.

**Syntaxe :**
```powershell
python -m cli.batch research `
  --topic "<thème_principal>" `
  --subtopics "sous-thème1,sous-thème2,sous-thème3" `
  [--count <nombre>] `
  [--wait]
```

**Paramètres :**
- `--topic` : Thème principal de recherche
- `--subtopics` : Sous-thèmes séparés par virgules
- `--count` : Nombre de variations par sous-thème (défaut: 5)
- `--wait` : (optionnel) Attend la fin du traitement

**Exemple :**
```powershell
python -m cli.batch research `
  --topic "Intelligence artificielle et écriture créative" `
  --subtopics "histoire,éthique,GPT,littérature" `
  --count 3 `
  --wait
```

**Sortie :**
- Fichiers dans `story/research/`
- Nommage : `YYYYMMDD_HHMMSS_research_<sous-thème>_<index>_<angle>.md`
- Angles générés : "Histoire et évolution", "Enjeux contemporains", "Exemples marquants", etc.

---

### 3. `status` — Vérifier l'avancement

Affiche le statut détaillé d'un batch en cours ou terminé.

**Syntaxe :**
```powershell
python -m cli.batch status --batch-id <msgbatch_id>
```

**Exemple :**
```powershell
python -m cli.batch status --batch-id msgbatch_014R2qqquriKSPkS2WYBkRXv
```

**Informations affichées :**
- Statut global : `in_progress`, `ended`, `failed`
- Progression : réussis / erreurs / en cours
- Dates de création et d'expiration
- Suggestion de téléchargement si terminé

---

### 4. `download` — Récupérer les résultats

Télécharge et sauvegarde tous les résultats d'un batch terminé.

**Syntaxe :**
```powershell
python -m cli.batch download --batch-id <msgbatch_id>
```

**Exemple :**
```powershell
python -m cli.batch download --batch-id msgbatch_014R2qqquriKSPkS2WYBkRXv
```

**Comportement :**
- Télécharge tous les résultats depuis l'API
- Sauvegarde selon le type de batch :
  - `draft-variants` → `story/drafting/<titre>/`
  - `research` → `story/research/`
- Crée/met à jour le fichier `_metadata.json`
- Affiche un résumé : fichiers sauvegardés, erreurs éventuelles

---

### 5. `list` — Lister les batchs récents

Liste les derniers batchs avec leur statut.

**Syntaxe :**
```powershell
python -m cli.batch list [--limit <nombre>]
```

**Exemple :**
```powershell
python -m cli.batch list --limit 10
```

**Affichage :**
- ID du batch
- Type (draft-variants, research, unknown)
- Statut et progression
- Date de création
- Indicateur de téléchargement
- Commande suggérée pour télécharger

---

## Workflow type

### Scénario 1 : Variations d'un chapitre

```powershell
# 1. Lancer la génération
python -m cli.batch draft-variants `
  --chapter story/drafting/MonHistoire/chapitre_01.md `
  --styles "sombre,léger,lyrique"

# Sortie : msgbatch_abc123xyz

# 2. Vérifier l'avancement (après quelques minutes)
python -m cli.batch status --batch-id msgbatch_abc123xyz

# 3. Télécharger quand terminé (ended)
python -m cli.batch download --batch-id msgbatch_abc123xyz

# 4. Consulter les fichiers générés
ls story/drafting/MonHistoire/*_variant_*.md
```

### Scénario 2 : Recherche documentaire

```powershell
# 1. Lancer la recherche
python -m cli.batch research `
  --topic "Prémisse Truby" `
  --subtopics "identité,moi" `
  --count 5 `
  --wait  # Attend la fin (peut prendre 10-60 min)

# 2. Fichiers automatiquement sauvegardés dans story/research/
# 3. Consulter les résultats
ls story/research/*_research_*.md
```

---

## Structure des métadonnées

Chaque batch génère un fichier `msgbatch_<id>_metadata.json` :

```json
{
  "batch_id": "msgbatch_014R2qqquriKSPkS2WYBkRXv",
  "type": "draft_variants",
  "created_at": "2026-01-21T14:25:01.154076",
  "chapter_file": "story/drafting/.../chapitre.md",
  "styles": ["mélancolique", "brutal", "poétique"],
  "status": "completed",
  "request_count": 3,
  "completed_at": "2026-01-21T15:30:45.123456",
  "saved_files": 3,
  "errors": 0
}
```

---

## Limitations et bonnes pratiques

### Limitations
- ⏱️ **Délai de traitement** : 10 minutes à 24h selon la charge
- 📊 **Quota** : 10 000 requêtes par batch max
- ⏰ **Expiration** : Résultats disponibles 24h après la fin
- 💾 **Pas de streaming** : Résultats disponibles uniquement en bloc

### Bonnes pratiques

✅ **À faire :**
- Utiliser `--wait` pour les petits batchs (< 10 requêtes)
- Télécharger les résultats dans les 24h
- Conserver les `batch_id` pour traçabilité
- Vérifier `status` avant `download`

❌ **À éviter :**
- Lancer plusieurs batchs identiques simultanément
- Oublier de télécharger dans les 24h (perte des résultats)
- Utiliser batch pour 1-2 requêtes (surcoût de latence)

---

## Dépannage

### Erreur : "No module named 'anthropic'"
```powershell
pip install anthropic
```

### Erreur : "API key not found"
Vérifier `.env` :
```env
ANTHROPIC_API_KEY=sk-ant-...
```

### Batch reste en "in_progress" très longtemps
- Normal si > 100 requêtes (peut prendre 1-2h)
- Vérifier après 30 min avec `status`
- Ne pas relancer de batch identique

### Résultats non téléchargés
- Vérifier que statut = "ended" avec `status`
- Télécharger avant expiration (24h)
- Utiliser `list` pour retrouver l'ID

---

## Intégration avec les tâches VS Code

Vous pouvez ajouter des tâches dans `.vscode/tasks.json` :

```json
{
  "label": "Batch: Draft variants (minimaliste)",
  "type": "shell",
  "command": "${workspaceFolder}/.venvHOME/Scripts/python.exe",
  "args": [
    "-m", "cli.batch", "draft-variants",
    "--chapter", "story/drafting/MonHistoire/chapitre.md",
    "--styles", "minimaliste",
    "--wait"
  ],
  "group": "build"
}
```

---

## Pour aller plus loin

- 📖 Documentation Claude Batches API : https://docs.anthropic.com/en/api/messages-batches
- 🔧 Code source : [cli/batch.py](cli/batch.py)
- 🧪 Exemples de prompts : `out/prompts/`
- 📊 Métadonnées : `story/drafting/batches/`

---

**Dernière mise à jour** : 2026-01-23
