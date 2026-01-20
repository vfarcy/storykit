# StoryKit — Écrire avec la méthode Truby + un workflow “spec-driven”

StoryKit transpose à l’écriture (roman, fiction, non-fiction narrative) une logique inspirée de SpecKit :
on **prépare des artefacts** (Markdown/YAML) qui rendent les intentions **claires et vérifiables**, puis on
**assemble un prompt** propre et reproductible à destination d’un assistant IA (au choix), sans runtime
propriétaire.

> Principe : **commande → artefacts → prompt → IA → texte**.

---

## 1) Pourquoi la méthode Truby ?

John Truby est un pédagogue de la dramaturgie reconnu pour une approche **organique** de l’histoire,
qui dépasse la stricte “structure en trois actes”. Son cadre relie **personnages, intrigue, thème,
monde et symboles** dans un système vivant où chaque élément agit sur les autres. Truby met
notamment l’accent sur :  
- une **prémisse** forte (la “graine” qui détermine le potentiel du récit),  
- un **fil thématique** formulé en **argument moral** (thèse ↔ antithèse ↔ synthèse),  
- une **progression** structurée par les **7 étapes fondamentales** et, au besoin, par **22 étapes**
plus détaillées,  
- le **web de personnages** (contrastes/fonctions),  
- un **scene‑weave** (tissage de scènes) préparé **avant** la rédaction.

### 1.1 Les 7 étapes fondamentales
Le “squelette” que partagent toutes les bonnes histoires selon Truby :
**faiblesse & besoin → désir → opposant → plan → bataille → auto‑révélation → nouvel équilibre**.
Elles modélisent la transformation du/de la protagoniste et rendent l’arc **nécessaire** et **satisfaisant**.

### 1.2 Les 22 étapes (pour les récits plus denses)
Les **22 steps** détaillent les pivots (révélations/décisions, fausse défaite, “visite à la mort”,
bataille, décision morale, etc.) et aident à tisser une progression **précise** qui reste logique mais
surprenante. C’est une extension **pratique** — pas un carcan — pour prévenir les “trous” de causalité.

### 1.3 Web de personnages, argument moral, monde & symboles
- **Web de personnages** : définir chacun par **contraste** (valeurs, fonctions dramatiques).  
- **Argument moral** : articuler **thèse/antithèse** et viser une **synthèse incarnée** par les actes
(éviter le “message plaqué”).  
- **Monde & symboles** : le **story world** reflète l’intériorité du héros et les **symboles** compressent
du sens pour guider scènes et motifs.

### 1.4 Genres : promesse, “beats” et philosophie
Dans *The Anatomy of Genres*, Truby montre que chaque genre s’appuie sur des **beats** profonds (événements
structurants) et **porte une philosophie** (une “manière d’agir dans le monde”). Maîtriser ces beats est
crucial pour respecter la **promesse au lectorat** tout en innovant (mélanges de genres inclus).

---
> **Pour approfondir la méthode Truby :** voir [TRUBY_GUIDE.md](TRUBY_GUIDE.md) — guide complet avec exemples, 
> exercices pratiques et intégration avec StoryKit.

---
## 2) Ce que fait StoryKit

StoryKit fournit :
- des **modèles** Markdown/YAML pour **prémisse**, **7 étapes**, **22 étapes**, **web de personnages**,
**argument moral**, **beats de genre**, **scene‑weave** ;
- un **CLI Python minimal** (`storykit`) qui **assemble un prompt** clair (contexte + instructions) à partir
de ces fichiers ;
- des **templates d’issues** (slash‑commands) pour guider la collaboration et garder la **traçabilité**.

> Le kit **n’impose pas** de modèle IA : vous restez libre d’utiliser Copilot, Claude, Gemini, etc.  
> L’assemblage produit un **prompt reproductible** que vous collez tel quel dans l’assistant IA.

---

## 3) Arborescence

```
story/
├─ truby/            # Prémisse, 7 étapes, 22 étapes, web de personnages, argument moral, monde, symboles
├─ genre/            # Choix de genre & beats requis
├─ outline/          # Scene‑weave & carte des actes/chapitres
├─ research/         # Sources, notes (utile en non‑fiction)
├─ drafting/         # Brouillons de chapitres
├─ tasks/            # Tâches éditoriales
config/              # storykit.config.yaml (IA, langue)
cli/                 # storykit.py (assemble prompts) + adapters (Claude/OpenAI/Gemini)
.github/ISSUE_TEMPLATE # Issues modèles (slash‑commands)
out/prompts/         # Prompts générés (dry‑run)
```

### 3.1) Fichiers obligatoires et optionnels

#### Fichiers obligatoires (requis pour `validate`)

La commande `python -m cli.storykit validate` vérifie la présence et la cohérence de **5 fichiers minimum** :

1. **`story/config/style.md`**  
   - Rubriques requises : `Ton`, `Voix`, `Rythme`
   - Auto-fix : si `style.autofix: true`, les rubriques manquantes sont ajoutées automatiquement
   - Sections optionnelles : contrôlées par `style.optional_autofix` (`forbidden`, `examples`, `both`, ou `none`)

2. **`story/genre/genre_choice.yaml`**  
   - Genre valide et structure correcte
   - Définit la promesse au lectorat

3. **`story/genre/genre_beats.yaml`**  
   - IDs uniques (format `gNN`)
   - Statuts valides pour chaque beat
   - Noms présents pour tous les beats

4. **`story/truby/seven_steps.yaml`**  
   - Champs requis minimum :
     - `weakness_need` : faiblesse psychologique (accepte string simple ou mapping avec `internal`)
     - `desire` : objectif conscient poursuivi
     - `opponent` : identité de l'opposant (accepte string simple ou mapping avec `name`)
   - ⚠️ **Nouveauté** : Validation robuste acceptant deux formats de YAML (string directe ou structure dict)

5. **`story/outline/scene_weave.md`**  
   - Présence des pivots obligatoires : First Revelation, Midpoint, Battle
   - Références aux beats valides (depuis `genre_beats.yaml`)
   - Tissage de scènes cohérent avec la structure

Ces 5 fichiers forment le **squelette minimal** pour qu'un projet passe la validation et garantit la cohérence de base entre genre, structure et scènes.

#### Fichiers optionnels (utilisés par `assemble` mais non vérifiés par `validate`)

Ces fichiers enrichissent le contexte et la profondeur du récit selon la complexité du projet :

**Structure avancée (Truby) :**

- **`story/truby/twenty_two_steps.yaml`**  
  *Utilité* : Détailler la structure pour récits complexes  
  - Complète les 7 étapes avec 22 pivots précis (révélations, gauntlet, visite à la mort, etc.)
  - Prévient les "trous" de causalité  
  - Utilisé par `assemble --target truby22`  
  *Quand l'utiliser* : romans longs, intrigues multiples, arcs narratifs denses

- **`story/truby/character_web.yaml`**  
  *Utilité* : Définir les personnages par contraste  
  - Fonctions dramatiques (allié, rival, mentor, faux allié...)
  - Valeurs en tension vs protagoniste
  - Trajectoires relationnelles  
  *Quand l'utiliser* : cast étendu, dynamiques de groupe complexes

- **`story/truby/moral_argument.md`**  
  *Utilité* : Articuler le thème sans "message plaqué"  
  - Thèse ↔ antithèse ↔ synthèse
  - Incarner le débat moral par des actes (pas des discours)
  - Guider les choix moraux du protagoniste  
  *Quand l'utiliser* : fiction thématique, récit à portée philosophique

- **`story/truby/story_world.md`**  
  *Utilité* : Monde narratif reflétant l'intériorité du héros  
  *Quand l'utiliser* : univers élaborés, SF/fantasy, thrillers géographiques

- **`story/truby/symbol_web.yaml`**  
  *Utilité* : Symboles récurrents compressant du sens  
  *Quand l'utiliser* : récits à forte dimension poétique ou métaphorique

**Documentation et planification :**


**`story/truby/premise.md`**  
  *Utilité* : Cristalliser l'intention initiale  
  - 1 phrase = germe de l'histoire
  - Principe organisateur (ce qui rend le récit unique)
  - Promesse de genre  
  *Quand l'utiliser* : phase exploratoire, pitcher le projet

- **`story/research/*`**  
  *Utilité* : Sources et documentation  
  - Contexte historique/géographique
  - Jargon professionnel (polar, médical, juridique...)
  - Références culturelles  
  *Quand l'utiliser* : non-fiction narrative, romans documentés, thriller technique

- **`story/tasks/*`**  
  *Utilité* : Tâches éditoriales et checklists  
  - Suivi des révisions
  - Points à approfondir
  - Notes de relecture  
  *Quand l'utiliser* : gestion de projet, collaboration

**Rédaction :**

- **`story/drafting/*`**  
  *Utilité* : Brouillons de chapitres  
  - Versioning des rédactions successives
  - Comparaison avant/après révisions  
  *Quand l'utiliser* : phase de rédaction (`assemble --target draft`)

#### Stratégie d'utilisation progressive

**Minimal viable** (5 fichiers obligatoires) :  
→ Genre, beats, 7 étapes, weave, style  
→ **Suffit pour** : nouvelles, projets courts, structure simple

**Complexité moyenne** (+ 3-4 optionnels) :  
→ Ajouter : 22 étapes, character web, moral argument  
→ **Pour** : romans standards, arcs travaillés, personnages multiples

**Projet ambitieux** (tous fichiers) :  
→ Inclure : research, story world, symbol web, tasks  
→ **Pour** : saga, thriller documenté, fiction littéraire, univers complexes

**Principe** : commencer minimal, enrichir progressivement si le prompt manque de contraintes ou de contexte. Les fichiers optionnels sont des outils à mobiliser selon le besoin, pas des obligations.

#### Pourquoi les 22 étapes ne sont-elles pas validées ?

La commande `validate` se concentre sur les **5 fichiers obligatoires** et ne vérifie pas les 22 étapes pour plusieurs raisons de design :

1. **Redondance structurelle**  
   Les 22 étapes sont une **expansion détaillée** des 7 étapes. Si `seven_steps.yaml` est valide, le squelette narratif fondamental est garanti. Les 22 étapes ajoutent de la granularité mais ne changent pas la logique de base (faiblesse → désir → opposant → bataille → transformation).

2. **Principe de minimalité**  
   StoryKit suit une philosophie **"minimal viable"** :
   - Les **7 étapes** = socle universel (toute histoire en a besoin)
   - Les **22 étapes** = raffinement optionnel (seulement si la complexité le justifie)
   
   Obliger la validation des 22 étapes forcerait tous les projets à les remplir, même les nouvelles ou récits courts qui n'en ont pas besoin.

3. **Complexité de validation**  
   Valider 22 pivots avec leurs **interdépendances causales** serait beaucoup plus lourd :
   - Vérifier que "Apparent Defeat" suit logiquement "Gauntlet"
   - S'assurer que "Visit to Death" précède "Battle"
   - Contrôler la cohérence des révélations successives
   
   Cette validation nécessiterait des règles métier complexes qui alourdiraient le CLI sans bénéfice proportionnel.

4. **Distinction cohérence vs exhaustivité**  
   `validate` vérifie la **cohérence minimale** (les fichiers essentiels existent et sont structurés correctement), pas l'**exhaustivité narrative**. Les 5 fichiers obligatoires garantissent :
   - Genre défini (promesse au lecteur)
   - Structure de base (7 étapes)
   - Beats de genre présents
   - Scènes tissées avec pivots clés
   - Style défini
   
   C'est suffisant pour démarrer `assemble` et produire des prompts cohérents.

5. **Responsabilité créative**  
   Les **22 étapes** relèvent du **travail créatif avancé**. Les valider automatiquement impliquerait d'imposer des contraintes rigides sur des choix narratifs subtils. StoryKit préfère :
   - **Valider** les fondations (7 étapes, beats, weave)
   - **Faire confiance** à l'auteur pour les raffinements (22 étapes, character web, moral argument)

Cette approche permet à StoryKit de rester **flexible** tout en garantissant une base solide. Les fichiers optionnels enrichissent le contexte pour `assemble` sans alourdir le processus de validation.

---

### 3.3) Améliorations récentes (Janvier 2026)

**Validation robuste de `seven_steps.yaml` :**
- ✅ Accepte maintenant **deux formats YAML** pour `weakness_need` et `opponent`
- Format simple : `weakness_need: "texte"` ou `opponent: "nom"`
- Format structuré : `weakness_need: { internal: "texte" }` ou `opponent: { name: "nom" }`
- Plus d'erreur `AttributeError: 'str' object has no attribute 'get'`

**Estimation automatique du budget tokens :**
- ✅ Calcul de la taille du prompt d'entrée avant envoi à l'API
- ⚠️ Avertissement jaune si prompt > 80% de `max_tokens` (risque de troncature)
- ❌ Avertissement rouge si prompt > 100% de `max_tokens` (requête rejetée)
- Aide à ajuster `max_tokens` **avant** l'appel coûteux

**Meilleur support Windows :**
- ✅ Déclaration `# -*- coding: utf-8 -*-` dans tous les fichiers Python
- ✅ Documentation pour configurer l'encodage UTF-8 sous PowerShell
- Fini les problèmes d'affichage des caractères accentués

---

## 4) Installation

```bash
python -m venv .venv
# Sous Windows PowerShell :
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

> Les packages LLM sont **optionnels**. Vous pouvez utiliser `assemble` et `validate` sans aucun provider.
> Pour activer un adaptateur et envoyer les prompts à une API, installe le module du provider
> (voir section « Adaptateurs IA réels »).

### Windows PowerShell — aide‑mémoire

```powershell
# Activer l'environnement virtuel
.venv\Scripts\Activate.ps1

# Vérifier l'interpréteur Python utilisé (chemin dans .venv)
python -c "import sys; print(sys.executable)"

# Mettre à jour pip et installer les dépendances de base
python -m pip install --upgrade pip
pip install -r requirements.txt

# Créer le fichier .env à partir du template et l'ouvrir
Copy-Item .env.example .env
notepad .env

# (Optionnel) Définir les clés API pour la session courante
# Utiliser selon le provider choisi
$env:ANTHROPIC_API_KEY = "sk-ant-..."    # Claude
$env:OPENAI_API_KEY    = "sk-proj-..."   # OpenAI / Copilot
$env:GOOGLE_API_KEY    = "AIza..."       # Gemini

# Premier check de cohérence du projet
python -m cli.storykit validate

# (Optionnel) Sans auto-fix de style.md
python -m cli.storykit validate --no-autofix-style
```

Astuce PowerShell (chemins avec espaces) :

```powershell
# Utiliser l'opérateur d'appel & avec un chemin entre guillemets
& "C:\Users\vfarc\OneDrive - Groupe ESIEA\Dev\story-repo-polar\.venv\Scripts\python.exe" -m cli.storykit validate

# Variante relative depuis le repo
& .\.venv\Scripts\python.exe -m cli.storykit validate

# Alias pratique pour la session courante
Set-Alias vpy "$PWD\.venv\Scripts\python.exe"
vpy -m cli.storykit validate
```

**Encodage UTF-8 (Windows PowerShell) :**  
Si vous rencontrez des problèmes d'affichage des caractères accentués :

```powershell
# Pour la session courante
$env:PYTHONIOENCODING="utf-8"
python -m cli.storykit validate

# Ou lancer Python avec flag UTF-8
python -X utf8 -m cli.storykit validate

# Permanent : ajouter à votre profil PowerShell
notepad $PROFILE
# Ajouter la ligne : $env:PYTHONIOENCODING="utf-8"
```

---

## 5) Configuration

Édite `story/config/storykit.config.yaml` :

```yaml
ai:
  provider: dry-run        # dry-run | claude | copilot | gemini
  model: ""                # ex: claude-sonnet-4-5, gpt-4o, gemini-2.5-flash
  max_tokens: 8000         # Budget de sortie (8000 recommandé pour chapitres complets)
project:
  root: ./story
language: fr
format:
  line_width: 100
style:
  autofix: true            # insérer automatiquement le squelette Ton/Voix/Rythme si manquant
  optional_autofix: none   # none | forbidden | examples | both (sections optionnelles)
```

- **dry-run** écrit simplement le **prompt** dans `out/prompts/` (aucun appel réseau).
- **max_tokens** : Recommandé `8000` pour les chapitres complets ; StoryKit estime la taille du prompt et affiche un avertissement si elle approche cette limite.

**Avertissements automatiques de budget tokens :**
- ⚠️ **Jaune** : si le prompt d'entrée > 80% de `max_tokens` → risque de réponse tronquée
- ❌ **Rouge** : si le prompt d'entrée > 100% de `max_tokens` → requête rejetée par l'API

Exemple de sortie :
```
Attention: Le prompt d'entrée (3953 tokens estimés) approche la limite max_tokens (4000). 
La réponse risque d'être tronquée.
```

L'estimation utilise une heuristique simple (~1 token par 4 caractères pour le français). Pour plus de précision, vous pouvez intégrer `tiktoken` (bibliothèque OpenAI de comptage exact de tokens) ou utiliser l'API native du provider.

### Adaptateurs IA réels

StoryKit supporte trois adaptateurs pour envoyer vos prompts directement aux APIs :

| Provider | Module requis | Clé API | Modèle par défaut |
|----------|--------------|---------|-------------------|
| **claude** | `anthropic` | `ANTHROPIC_API_KEY` | `claude-3-5-sonnet-20241022` |
| **openai/copilot** | `openai` | `OPENAI_API_KEY` | `gpt-4o` |
| **gemini** | `google-genai` | `GOOGLE_API_KEY` | `gemini-2.5-flash` |

**Installation :**
```bash
# Choisir selon votre provider
pip install anthropic              # Claude
pip install openai                 # OpenAI/Copilot
pip install google-genai           # Gemini (nouveau)
```

**Configuration des clés API :**
```bash
# Copier le template
copy .env.example .env

# Éditer .env et renseigner vos clés
# ANTHROPIC_API_KEY=sk-ant-...
# OPENAI_API_KEY=sk-proj-...
# GOOGLE_API_KEY=AIza...
```

**Activer dans storykit.config.yaml :**
```yaml
ai:
  provider: claude         # claude | openai | copilot | gemini
  model: claude-3-5-sonnet-20241022  # ou: gpt-4o, gemini-2.5-flash
  max_tokens: 4096
```

**Utilisation :**
```bash
# Assemblage avec appel API direct
python -m cli.storykit assemble --target truby7

# Les fichiers générés :
# - out/prompts/YYYYMMDD_HHMMSS_truby7.md (prompt envoyé)
# - out/responses/YYYYMMDD_HHMMSS_truby7_response.md (réponse IA)
```

Les adaptateurs se chargent dynamiquement selon les modules installés et les clés disponibles.

### Prompt Caching (Claude) — Réduire les coûts de ~90%

L'adaptateur Claude implémente le **Prompt Caching** d'Anthropic pour réduire drastiquement les coûts sur les appels répétés.

**Comment ça marche :**
- Le contexte stable (prémisse, style, artefacts Truby, beats) est automatiquement mis en cache
- Les instructions finales (variables selon la commande) ne sont pas cachées
- Cache valide pendant **~5 minutes**
- **Minimum 1024 tokens** requis pour activer le cache

**Vitesses réelles de disponibilité des résultats :**

| Scénario | Temps d'attente | Détails |
|----------|-----------------|---------|
| **Premier appel** (création cache) | 8-12 sec | Latence API + création cache (6500 tokens typique) |
| **Appels suivants** (cache réutilisé) | **4-6 sec** | **~50% plus rapide** grâce au cache |
| **Commande `truby7`** | 8-10 sec (1er) / 5 sec (suivants) | Structure légère, texte ~1000-1500 mots |
| **Commande `truby22`** | 12-15 sec (1er) / 6 sec (suivants) | Structure dense, 22 étapes détaillées |
| **Commande `draft`** (chapitre 5000 mots) | 35-45 sec (1er) / 20-25 sec (cache) | Génération complète, sortie longue |
| **Batch (5 variations)** | 2-3 min (50% réduction) | Traitement asynchrone, 5 requêtes parallèles |

**Économies réelles en flux normal :**

Premier appel (création du cache) :
```bash
python -m cli.storykit assemble --target truby7
# [Cache: 6582 créés, 0 lus]
# ⏱️  Durée : ~9 secondes (création cache + réponse IA)
# → Coût normal sur 6582 tokens + petite surcharge de création
```

Appels suivants (< 5 min) :
```bash
python -m cli.storykit assemble --target truby7
# [Cache: 6582 lus]
# ⏱️  Durée : ~5 secondes (~45% plus rapide)
# → ~90% d'économie sur les 6582 tokens en cache !
```

**Workflow temps réel (10 commandes d'affilée) :**
```
Minute 0:00 → assemble --target premise          [9 sec, cache créé]
Minute 0:10 → assemble --target genre            [5 sec, cache réutilisé]
Minute 0:15 → assemble --target truby7           [5 sec, cache réutilisé]
Minute 0:20 → assemble --target truby22          [6 sec, cache réutilisé]
Minute 0:26 → assemble --target weave            [6 sec, cache réutilisé]
Minute 0:32 → assemble --target web              [5 sec, cache réutilisé]
Minute 0:37 → assemble --target draft --chapter 1 [22 sec, cache réutilisé + génération]
Minute 0:59 → assemble --target draft --chapter 2 [23 sec, cache réutilisé + génération]
────────────────────────────────────────────────────
TOTAL : 1 minute 21 secondes pour 8 commandes
→ Temps sauvegardé vs sans cache : ~30 secondes
```

**Stratégies d'optimisation :**

1. **Enchaînez vos commandes rapidement** (< 5 min entre chaque)
   ```bash
   python -m cli.storykit assemble --target truby7    # 9 sec
   # Analyser la réponse, ajuster les fichiers
   python -m cli.storykit assemble --target truby22   # 6 sec (cache réutilisé!)
   python -m cli.storykit assemble --target weave     # 6 sec (cache réutilisé!)
   # → Gain : 6 + 6 = 12 sec économisés
   ```

2. **Itérations rapides** : testez plusieurs versions d'une même commande
   ```bash
   # Modifier story/truby/seven_steps.yaml
   python -m cli.storykit assemble --target truby7      # 9 sec
   # Ajuster encore...
   python -m cli.storykit assemble --target truby7      # 5 sec (cache réutilisé)
   python -m cli.storykit assemble --target truby7      # 5 sec (cache réutilisé)
   # → Gain cumul : 4 + 4 = 8 sec économisés
   ```

3. **Désactiver ponctuellement** : si le contexte change radicalement
   ```yaml
   # Dans storykit.config.yaml (ou via code)
   ai:
     use_cache: false  # Désactive le cache temporairement
   ```

**Statistiques affichées :**
- `[Cache: X créés]` : tokens mis en cache (premier appel)
- `[Cache: Y lus]` : tokens lus depuis le cache (économie ~90%)
- Aucun message : prompt trop court (< 1024 tokens) pour bénéficier du cache

**Coût estimé :**
- Tokens normaux : ~$0.003 / 1K tokens input (Sonnet 3.5)
- Tokens en cache (création) : ~$0.00375 / 1K tokens (~25% surcharge)
- Tokens en cache (lecture) : ~$0.0003 / 1K tokens (**90% d'économie**)

Pour un projet StoryKit typique (6000 tokens de contexte) :
- Sans cache : $0.018 par appel
- Avec cache (après 1er appel) : $0.002 par appel
- **Économie : $0.016 par appel (~89%)**

**Temps vs coût : le compromis :**

| Stratégie | Temps total | Coût total | Idéal pour |
|-----------|------------|-----------|-----------|
| Sans cache (7 appels) | 65 sec | $0.126 | Pas d'itération, une passation unique |
| Avec cache (7 appels rapides) | 47 sec | $0.020 | Itérations rapides, raffinement actif |
| Batch (50% réduction) | 120 sec | $0.063 | Génération de masse (5-10 chapitres) |
| Cache + Batch (cumulé) | 100 sec | $0.010 | Production maximale (coût + vitesse) |

**Observations terrain :**
- La première requête (création cache) coûte plus cher mais pose la base pour 20-30 appels rapides (~5 min de validité)
- Après 5 min, le cache expire → retour à la latence normale
- Les commandes `draft` (génération longue) bénéficient **moins** du cache (temps IA > temps cache), mais toujours 50% + rapide
- Le batch mode (asynchrone) est idéal pour générer 5+ chapitres sans surveillance active

### Style & Voix
- Emplacement: `story/config/style.md`. Ce fichier définit le ton, la voix et le rythme attendus.
- Rubriques requises: Titres ou labels pour **Ton**, **Voix**, **Rythme** (ex: `# Ton` ou `Ton:`).
- Inclusion automatique: la section “Style & Voix” est ajoutée au prompt assemblé après la **Prémisse**.
- Rappels d’instructions: un rappel “Respecter le style défini dans Style & Voix.” est inclus pour `truby7`, `truby22`, `weave` et `draft`.
- Validation: `python -m cli.storykit validate` vérifie que `style.md` contient ces rubriques.
- Auto-fix: si `style.autofix: true` (par défaut), les rubriques manquantes sont ajoutées automatiquement avec un squelette et un message est affiché.
- Désactiver ponctuellement: `python -m cli.storykit validate --no-autofix-style` (prioritaire sur la config).
- Sections optionnelles: `optional_autofix` contrôle l'insertion automatique de sections facultatives :
  - `none` (défaut) : Ton/Voix/Rythme uniquement
  - `forbidden` : ajoute "Interdits stylistiques" si absente
  - `examples` : ajoute "Éxemples" (conforme/non conforme) si absente
  - `both` : ajoute les deux sections facultatives

Exemples d'usage :
```bash
# Config par défaut (Ton/Voix/Rythme uniquement)
python -m cli.storykit validate

# Activer auto-insertion des interdits : éditer storykit.config.yaml
# style:
#   optional_autofix: forbidden
python -m cli.storykit validate
# → affiche "Section 'Interdits' ajoutée" si absente

# Activer auto-insertion des exemples et interdits
# style:
#   optional_autofix: both
python -m cli.storykit validate
```

Conseils pratiques pour `style.md`:
- Clarté: phrases concrètes, critères observables (éviter les injonctions vagues).
- Voix: préciser focalisation, niveau de langue, champs lexicaux à privilégier/éviter.
- Rythme: donner des repères (longueur moyenne de phrases, variation court/long, taille des paragraphes).
- Exemples: 2–3 mini-exemples de style conforme et non conforme aident beaucoup l’IA.
- Cohérence: garder `style.md` bref et resserré; c’est un contrat stylistique.

Exemple minimal (copier-coller dans `story/config/style.md`):

```markdown
# Ton
Sobre, concret, ironie mesurée ; éviter pathos et clichés.

# Voix
Focalisation interne limitée ; lexique précis ; phrase affirmatives.

# Rythme
Phrases 12–18 mots ; alternance court/long ; paragraphes 3–5 phrases.
```

Templates utiles:
- Exemple minimal: voir [templates/style.example.md](templates/style.example.md)
- Interdits stylistiques: voir [templates/style.forbidden.example.md](templates/style.forbidden.example.md)
- Exemples avancés (conforme / non conforme): voir [templates/style.advanced.example.md](templates/style.advanced.example.md)

---

## 6) Commandes disponibles

### Batch Processing : génération en masse avec 50% de réduction de coût 🚀

StoryKit inclut un **système de batch processing** via l'API Message Batches de Claude, permettant de générer plusieurs chapitres ou variations en parallèle avec **50% de réduction de coût**.

#### Pourquoi utiliser le batch ?

- ✅ **50% moins cher** que le mode normal
- ✅ **Génération parallèle** (jusqu'à 100,000 requêtes par batch)
- ✅ **Compatible avec prompt caching** (économies cumulées jusqu'à 95%)
- ✅ **Asynchrone** : lancez et continuez votre travail
- ✅ **Contexte enrichi automatique** : charge les artefacts Truby, scene_weave, style

#### Commandes batch disponibles

| Commande | Objectif | Exemple |
|----------|----------|---------|
| **draft-variants** | Variations stylistiques d'UN chapitre | `python -m cli.batch draft-variants --chapter Chap10.md --styles "mélancolique,brutal,poétique"` |
| **draft-chapters** | Générer PLUSIEURS chapitres différents | `python -m cli.batch draft-chapters --project MonProjet --chapters "8,9,10"` |
| **research** | Documentation thématique en masse | `python -m cli.batch research --topic "IA" --subtopics "histoire,éthique,GPT"` |
| **list** | Lister tous les batchs | `python -m cli.batch list` |
| **status** | Vérifier l'avancement | `python -m cli.batch status --batch-id msgbatch_XXX` |
| **download** | Récupérer les résultats | `python -m cli.batch download --batch-id msgbatch_XXX` |

#### Vitesses réelles de disponibilité des résultats

| Opération | Délai de disponibilité | Détails |
|-----------|----------------------|---------|
| **Soumission du batch** | Immédiate (< 2 sec) | Batch ID retourné, statut = `processing` |
| **Première vérification** | ~10-15 sec | Statut passe à `in_progress` |
| **5 variations** (draft-variants) | **20-30 min** | Traitement parallèle rapide, coûte ~$0.075 |
| **3 chapitres** (draft-chapters) | **25-35 min** | Génération ~1500 mots chacun |
| **10 chapitres** (draft-chapters) | **45-90 min** | Traitement parallèle, plus gros volume |
| **20 fiches recherche** (research) | **30-50 min** | Générations courtes (~300 mots) |
| **Batch complet** (100 requêtes) | **1-3 heures** | Parallélisation massive |
| **Récupération** (download) | < 5 sec | Une fois le batch complété |

**Pattern de vérification :**
```bash
# Soumettre le batch
python -m cli.batch draft-chapters --chapters "1,2,3" --project MonProjet
# → Retour immédiat : batch_id = msgbatch_016Rx96kiN2QqVme4LqfNAMy

# Vérifier le statut (première vérification après ~15 sec)
python -m cli.batch status --batch-id msgbatch_016Rx96kiN2QqVme4LqfNAMy
# → Statut : in_progress (0/3 complétés)
# → Statut : in_progress (1/3 complétés)
# → Statut : in_progress (2/3 complétés)
# → Statut : completed (3/3 complétés) → télécharger !

# Récupérer les résultats
python -m cli.batch download --batch-id msgbatch_016Rx96kiN2QqVme4LqfNAMy
# → Fichiers écrits dans story/drafting/ ou story/research/
```

**Observations terrain :**
- Les batchs **démarrent immédiatement** : pas de file d'attente visible
- **Traitement très parallélisé** : 3-5 requêtes complétées en ~25-30 min (vs 2-3h en mode API normal)
- **Pics d'utilisation** : délais peuvent augmenter de 30-50% (14h30-18h UTC)
- **Off-peaks** : délais optimaux (22h-08h UTC, délais réduits de 20%)
- Le `--wait` bloque localement jusqu'à achèvement (polling toutes les 5 sec)
- **Recommandé** : utiliser `--wait` pour les petits batchs (< 10 requêtes), soumettre sans `--wait` pour les gros (> 20 requêtes)

#### Exemples d'utilisation

**1. Tester 5 variations stylistiques d'un chapitre**
```bash
python -m cli.batch draft-variants \
  --chapter "story/drafting/MonProjet/Chap10.md" \
  --styles "mélancolique,brutal,poétique,minimaliste,lyrique" \
  --wait
```
→ Batch soumis
→ 5 versions disponibles dans **20-30 min** pour ~$0.075 (vs $0.15 en mode normal)
```bash
# Ou sans --wait, vérifier après 15 sec
python -m cli.batch status --batch-id msgbatch_016Rx96kiN2QqVme4LqfNAMy

# Télécharger après ~25 min
python -m cli.batch download --batch-id msgbatch_016Rx96kiN2QqVme4LqfNAMy
```

**2. Générer plusieurs chapitres d'un coup**
```bash
python -m cli.batch draft-chapters \
  --project "MonProjet" \
  --chapters "8,9,10" \
  --wait
```
→ Batch soumis
→ 3 chapitres complets disponibles dans **25-35 min** avec contexte Truby automatique
```bash
# Ou checker status progressivement
python -m cli.batch status --batch-id msgbatch_017qbwwmJKHUmUnNPNUYie1T

# Download quand complété
python -m cli.batch download --batch-id msgbatch_017qbwwmJKHUmUnNPNUYie1T
```

**3. Construire votre documentation en masse**
```bash
python -m cli.batch research \
  --topic "Intelligence artificielle et littérature" \
  --subtopics "histoire,éthique,créativité,prix_littéraires" \
  --count 5
```
→ Batch soumis (20 fiches = 5 subtopics × 5 count)
→ 20 fiches de recherche disponibles dans **30-50 min**
```bash
# Lancer d'autres batchs pendant ce temps (parallèle CPU-side)
python -m cli.batch draft-chapters --chapters "5,6,7"

# Vérifier l'historique complet
python -m cli.batch list
# → msgbatch_016Rx96kiN2QqVme4LqfNAMy [research] completed
# → msgbatch_017qbwwmJKHUmUnNPNUYie1T [draft-chapters] in_progress
```

**4. Voir l'historique de tous vos batchs et leur statut**
```bash
python -m cli.batch list
# → Affiche tous les batchs avec ID, type, statut et date de création
```

#### Workflows recommandés

**Workflow vitesse** (premier draft complet en 48h) :
```bash
# Jour 1 : Recherche
python -m cli.batch research --topic "Votre thème" --subtopics "A,B,C,D,E" --count 5

# Jour 2 : Génération de tous les chapitres
python -m cli.batch draft-chapters --project "MonProjet" --chapters "1,2,3,4,5,6,7,8,9,10"
```

**Workflow qualité** (itératif) :
```bash
# Phase 1 : Draft initial
python -m cli.batch draft-chapters --chapters "1,2,3,4,5,6,7,8,9,10"

# Phase 2 : Raffinement des chapitres clés
python -m cli.batch draft-variants --chapter Chap01.md --styles "A,B,C"
python -m cli.batch draft-variants --chapter Chap06.md --styles "D,E,F"
python -m cli.batch draft-variants --chapter Chap10.md --styles "G,H,I"
```

#### Coûts et économies

| Scénario | Mode normal | Mode batch | Économie |
|----------|-------------|------------|----------|
| 5 variations d'un chapitre | $0.15 | **$0.075** | 50% |
| 3 chapitres différents | $0.15 | **$0.075** | 50% |
| 10 chapitres complets | $0.50 | **$0.25** | 50% |
| 20 fiches recherche | $0.30 | **$0.15** | 50% |
| Roman complet (10 ch) + recherche | $1.07 | **$0.535** | 50% |

**Avec prompt caching :** Économies cumulées jusqu'à **95%** si les requêtes partagent le même contexte système.

#### Documentation complète

Consultez [cli/README_BATCH.md](cli/README_BATCH.md) pour :
- Guide complet des 6 commandes
- 5 cas d'usage détaillés
- 3 workflows complets (vitesse/qualité/équilibre)
- Stratégies d'optimisation des coûts
- Matrice de décision draft-variants vs draft-chapters
- Troubleshooting et bonnes pratiques

---

### Assemble : générer des prompts (mode standard)

1) **Affiner la prémisse** (1 phrase + principe organisateur)  
```bash
python -m cli.storykit assemble --target premise
```

2) **7 étapes** (faiblesse/besoin → nouvel équilibre)  
```bash
python -m cli.storykit assemble --target truby7
```

3) **22 étapes** (chaînage fin : révélations, décisions, gauntlet…)  
```bash
python -m cli.storykit assemble --target truby22
```

4) **Scene‑weave** (liste de scènes, conflit/décision/valeur/beat de genre)  
```bash
python -m cli.storykit assemble --target weave
```

5) **Genre (beats + choix)**  
```bash
python -m cli.storykit assemble --target genre
```

6) **Web de personnages**  
```bash
python -m cli.storykit assemble --target web
```

7) **Brouillon de chapitre** (à partir du scene‑weave)  
```bash
python -m cli.storykit assemble --target draft --chapter 1
```

> Chaque commande génère `out/prompts/YYYYMMDD_HHMMSS_<target>.md`.  
> **Collez** ce prompt dans votre assistant IA, **intégrez** la réponse dans les fichiers du dossier `story/`, puis **commit**.

### Validate : vérifier la cohérence

```bash
# Valider tout le projet
python -m cli.storykit validate

# Désactiver l'auto-fix de style.md
python -m cli.storykit validate --no-autofix-style
```

**Contrôles effectués :**
- `genre_choice.yaml` : genre valide, structure correcte
- `genre_beats.yaml` : ids uniques (gNN), statuts valides, noms présents
- `seven_steps.yaml` : champs requis (weakness_need.internal, desire, opponent.name)
- `scene_weave.md` : présence de pivots (First Revelation/Midpoint/Battle), références aux beats valides
- `style.md` : rubriques Ton/Voix/Rythme présentes (auto-fix selon config)

Si des problèmes sont détectés, un tableau récapitulatif s'affiche avec le numéro et le message d'erreur.

### Choix des modèles LLM

Modifier `story/config/storykit.config.yaml` selon le provider :

**Claude (Anthropic) :**
```yaml
ai:
  provider: claude
  model: claude-3-5-sonnet-20241022    # Recommandé pour écriture
  # model: claude-3-5-haiku-20241022   # Plus rapide, moins cher
  # model: claude-3-opus-20240229      # Le plus puissant, plus cher
  max_tokens: 4096
```

**OpenAI / Copilot :**
```yaml
ai:
  provider: openai
  model: gpt-4o                         # Recommandé multimodal
  # model: gpt-4-turbo                  # Turbo (moins cher)
  # model: gpt-3.5-turbo                # Budget (rapide, moins précis)
  max_tokens: 4096
```

**Gemini (Google) :**
```yaml
ai:
  provider: gemini
  model: gemini-2.5-flash               # Recommandé (2026)
  # model: gemini-2.0-flash             # Version précédente
  # model: gemini-1.5-flash             # Ancienne version (si encore disponible)
  max_tokens: 4096
```

**Transmission de la config au CLI :**

La commande `python -m cli.storykit assemble` lit automatiquement `ai.model` et `ai.max_tokens` depuis `story/config/storykit.config.yaml` et les transmet aux adaptateurs via `meta`. Cela signifie :

- Si vous définissez `model: gemini-2.5-pro`, ce modèle sera utilisé pour **tous les appels**.
- Si vous laissez `model: ""` (vide), l'adaptateur applique sa logique par défaut (ex. Gemini choisit flash ou pro selon la tâche).

**Sélection automatique du modèle Gemini :**

Par défaut, si `model:` est vide, StoryKit choisit automatiquement le modèle Gemini le plus adapté selon la tâche :

- `premise`, `genre`, `truby7` : modèle rapide/économique (`gemini-2.5-flash`)
- `draft`, `truby22`, `weave` : modèle qualitatif/long (`gemini-2.5-pro`)

Si vous renseignez explicitement `model:` dans la config, ce modèle sera utilisé pour tous les appels (override). Sinon, la sélection automatique s'applique.

Ce mécanisme garantit :
- Robustesse (jamais d’erreur 404 si un modèle disparaît)
- Performance optimale selon la tâche
- Liberté utilisateur pour forcer un modèle précis si besoin

> Astuce : vous pouvez toujours surcharger ponctuellement le modèle via la config YAML ou en passant `model` dans les options avancées Python.
> ⚠️ Les modèles Gemini évoluent régulièrement. Si une erreur "404 NOT_FOUND" apparaît, essayez la version la plus récente (ex : gemini-2.5-flash). Utilisez la commande ListModels de l'API Google pour voir les modèles disponibles avec votre clé.

**Conseils d'usage :**
- **Premise/Genre** : modèles légers suffisent (Haiku, GPT-3.5, Flash)
- **Truby7/22, Weave** : modèles équilibrés (Sonnet, GPT-4o, Pro)
- **Draft** : modèles puissants (Opus, GPT-4o, Pro) + `max_tokens: 8000` pour chapitres longs

**Avertissements automatiques de tokens :**
StoryKit estime désormais la taille du prompt d'entrée et affiche un avertissement si vous approchez la limite `max_tokens` :
- ⚠️ **Jaune** : si input > 80% du budget → risque de réponse tronquée
- ❌ **Rouge** : si input > 100% du budget → requête rejetée par l'API

Exemple de sortie :
```
Attention: Le prompt d'entrée (3953 tokens estimés) approche la limite max_tokens (4000). 
La réponse risque d'être tronquée.
```

Solution : augmentez `max_tokens` dans la config :
```yaml
ai:
  max_tokens: 8000  # Pour chapitres complets
```

L'estimation utilise une heuristique simple (1 token ≈ 4 caractères pour le français). Pour plus de précision, vous pouvez intégrer `tiktoken` (OpenAI) ou l'API native du provider.

---

## 7) Workflow recommandé (Truby → texte)

**Phase 1 — Intention**
- `truby/premise.md` : 1 phrase + principe organisateur + promesse de genre.  
- `genre/` : genre principal, beats obligatoires, philosophie du genre.

**Phase 2 — Structure**
- `truby/seven_steps.yaml` : verrouiller faiblesse/besoin, désir, opposant, plan…  
- `truby/twenty_two_steps.yaml` : dérouler les pivots (révélations/décisions).  
- `truby/character_web.yaml` : contrastes/fonctions, valeurs en tension.  
- `truby/moral_argument.md` : thèse ↔ antithèse ↔ synthèse (incarnée par des actes).

**Phase 3 — Scènes**
- `outline/scene_weave.md` : tissage des scènes **avant** d’écrire (conflit, décision, valeur, beat).

**Phase 3.5 — Scene Weave (avant rédaction)**
- `outline/scene_weave.md` : tableau structurant les scènes selon les 7 étapes, beats de genre et pivots narratifs.  
- Détail ci-dessous.

**Phase 4 — Rédaction & révisions**
- `drafting/` : brouillons de chapitres via `--target draft`.  
- Relectures centrées sur **l'argument moral** et les **valeurs** scène par scène.  
- Ajuster les **beats de genre** pour honorer la promesse au lectorat.

---

## 7.5) Scene Weave — Structurer les scènes avec les 7 étapes

Le **scene_weave** est le tableau qui **concrétise** les 7 étapes en **scènes narratives numérotées**. C'est le plan détaillé avant rédaction.

### Pourquoi le scene_weave ?

Les 7 étapes donnent la **structure émotionnelle** (arc du héros) ; le scene_weave ajoute la **structure tactique** (lieux, conflits, décisions, beats) scène par scène.

**Avantage** : avant d'écrire un chapitre, tu sais exactement :
- Quelle fonction narrative elle remplit (Ghost, Inciting Event, Desire, Opponent, etc.)
- Où elle se situe (lieu)
- Quel conflit elle contient
- Quelle décision le héros y prend (irréversible)
- Quel beat de genre elle valide

### Structure du tableau scene_weave

```markdown
| # | Fonction Truby        | Lieu             | Conflit                    | Décision                 | Beat |
|----|----------------------|------------------|--------------------------|----------------------|------|
| 1  | Ghost                | Appartement Léo  | Page blanche vs Ambition  | Ouvrir StoriKit      | g01  |
| 2  | Inciting Event       | Bureau Éditeur   | Contrat offert par erreur | Signer sans lire     | g01  |
| 3  | Desire               | Plateau TV       | On le questionne          | Mentir en citant l'IA| g02  |
| 4  | Opponent/Mystery     | Chambre Léo      | L'IA écrit ses secrets    | Accepter l'aide      | g02  |
| 5  | Fake-Ally Opponent   | Soirée littéraire| L'ami doute               | Rompre avec l'ami    | g03  |
| 6  | Midpoint Reversal    | Bureau Léo       | L'IA génère une fin       | Se plier à l'algo    | g04  |
| 7  | Method Revelation    | Interface StoriKit| Vol de données           | Choisir la vérité    | g05  |
| 8  | Visit to Death       | Miroir salle SdB | Dissolution d'identité    | Continuer au Prix    | g07  |
| 9  | Battle               | Restaurant Drouant| Question piège du jury    | Mensonge ou aveu ?   | g09  |
|10  | Self-Revelation      | Place Gaillon    | Il a tué l'auteur         | Détruire le manuscrit| g10  |
```

### Colonnes expliquées

#### 1. **#** (numéro de scène)
- Ordre narrative (1-10+ généralement)
- Correspond approximativement à 1 chapitre ou groupe de scènes

#### 2. **Fonction Truby**
Lien avec les 7 étapes :

| Étape Truby | Fonction(s) narrative(s) | Scènes typiques |
|-------------|-------------------------|-----------------|
| **1. Faiblesse & Besoin** | `Ghost` : montrer l'état initial, le monde du héros | Scène 1 : le héros dans sa faiblesse |
| **2. Désir** | `Inciting Event` → `Desire` : le déclenchement, l'engagement | Scènes 2-3 : l'événement qui déclenche tout + la décision d'agir |
| **3. Opposant** | `Opponent` / `Mystery` : révéler la force antagoniste | Scènes 4-5 : révélation progressive de l'opposant, premiers doutes |
| **5. Bataille** | `Midpoint Reversal` → `Method Revelation` → `Visit to Death` → `Battle` : escalade et confrontation | Scènes 6-9 : le plan échoue → révélations → point de non-retour → affrontement |
| **6. Auto-révélation** | `Self-Revelation` : l'épiphanie, la compréhension | Scène 10 : le héros comprend ce qu'il doit vraiment faire |
| **7. Nouvel équilibre** | Dénouement : conséquences et nouvelle réalité | Scène 10+ : les actions finales, la nouvelle réalité établie |

**⚠️ Note importante** : L'**Étape 4 (Plan)** n'apparaît pas comme fonction à elle seule — elle est **intégrée** dans les scènes 5-6 comme "préparation" et "fausse victoire" (Fake-Ally Opponent + Midpoint Reversal).

### Mapping détaillé : 7 étapes → 10 scènes

Voici comment **structurer concrètement** tes scènes pour respecter les 7 étapes :

**ÉTAPE 1 : Faiblesse & Besoin (Scène 1)**
```
Fonction : Ghost
Objectif : Montrer le héros dans sa faiblesse intérieure
Conflit interne : La lutte du héros avec lui-même
Décision : Aucune (c'est le point de départ)
Exemple : Léo, page blanche, contemple son inactivité
```

**ÉTAPE 2 : Désir (Scènes 2-3)**
```
Scène 2 — Inciting Event (l'événement déclencheur)
Fonction : Opportunity / Call to Adventure
Objectif : Un événement externe pousse le héros à agir
Conflit : Opportunité vs doute
Décision : Le héros s'engage (accepte le défi)
Exemple : Léo reçoit un contrat d'édition (par erreur)

Scène 3 — Desire (le désir explicité)
Fonction : Commitment
Objectif : Le héros s'engage publiquement dans sa quête
Conflit : Garder le secret vs être honnête
Décision : Le héros choisit le mensonge/masquage
Exemple : Léo ment à la télévision sur son processus créatif
```

**ÉTAPE 3 : Opposant (Scènes 4-5)**
```
Scène 4 — Opponent Revealed (révélation de l'opposant)
Fonction : Raising Stakes
Objectif : L'adversaire/l'obstacle apparaît
Conflit : Le héros découvre qu'il n'est pas seul/pas invisible
Décision : Le héros accepte l'aide malgré le malaise
Exemple : L'IA (StoriKit) écrit les secrets intimes de Léo

Scène 5 — Fake-Ally Opponent (faux allié)
Fonction : Complications
Objectif : Montrer que certains "alliés" posent problème
Conflit : La confiance du héros est ébranlée
Décision : Le héros rompt avec cet allié pour protéger le secret
Exemple : L'ami littéraire de Léo commence à douter → Léo le lâche
```

**ÉTAPE 4 : Plan (Scènes 5-6) — intégré au conflit**
```
Scène 6 — Midpoint Reversal (retournement du point médian)
Fonction : Changed Circumstances / False Victory
Objectif : Le plan semble fonctionner MAIS montre ses failles
Conflit : Le héros obtient ce qu'il désire (succès apparent) mais découvre le coût
Décision : Le héros se plie à la logique de l'AI plutôt que de lutter
Exemple : L'IA génère une fin magnifique → Léo réalise qu'il n'a plus de contrôle créatif
```

**ÉTAPE 5 : Bataille (Scènes 7-9) — l'escalade**
```
Scène 7 — Method Revelation (révélation du "comment")
Fonction : Discovery / Turning Point
Objectif : Le héros découvre le fonctionnement réel de l'opposant
Conflit : Comprendre qu'il a été manipulé/trahi
Décision : Choisir la complaisance (continuer) ou la vérité
Exemple : Léo réalise que l'IA a accédé à ses données privées

Scène 8 — Visit to Death (visite à la mort)
Fonction : All is Lost / Dark Night of the Soul
Objectif : Le point le plus bas, le doute total
Conflit : Dissolution d'identité, nihilisme
Décision : Le héros choisit de continuer malgré tout (au lieu d'abandonner)
Exemple : Léo se regarde dans le miroir et ne reconnaît plus son reflet

Scène 9 — Battle (affrontement majeur)
Fonction : Climax
Objectif : La confrontation finale avec l'opposant
Conflit : Le moment de vérité — mensonge ou révélation ?
Décision : Le héros fait son choix crucial (mensonge vs aveu)
Exemple : Le jury pose une question piège au banquet du Prix Goncourt
```

**ÉTAPE 6 : Auto-révélation (Scène 10)**
```
Fonction : Self-Revelation / Realization
Objectif : Le héros comprend enfin ce dont il avait BESOIN
Conflit : Accepter la transformation intérieure
Décision : Le héros agit sur cette révélation
Exemple : Léo réalise qu'il a "tué l'auteur" (lui-même) → il détruit le manuscrit gagnant
```

**ÉTAPE 7 : Nouvel équilibre (Scène 10+)**
```
Fonction : New Equilibrium / Resolution
Objectif : Établir la nouvelle réalité post-transformation
Conflit : Aucun (le conflit est résolu)
Décision : Le héros vit selon sa nouvelle compréhension
Exemple : Léo, libéré du mensonge, recommence à écrire humblement
```

### Tableau de progression : Étapes → Scènes → Conflits

#### 3. **Lieu**
Où la scène se déroule
- Varie pour rythmer le lecteur
- Reflète souvent l'état interne du héros (prison interne = chambre, bataille = confrontation dehors)

#### 4. **Conflit**
Le cœur dramatique de la scène
- Externe (affrontement, obstacle) ou interne (doute, révélation)
- Doit escalader progressivement vers le climax

#### 5. **Décision**
L'action irréversible du héros
- Le héros doit choisir (ne pas agir = une décision)
- Chaque décision le rapproche du nouvel équilibre
- Ce choix crée les conséquences de la scène suivante

#### 6. **Beat**
Référence au beat de genre (depuis `genre_beats.yaml`)
- Format : `gNN` (ex: `g01`, `g02`, `g09`)
- Chaque scène valide un beat structurant du genre
- Assure que la promesse au lecteur est honorée

### Comment créer un scene_weave

#### Étape 1 : partir des 7 étapes

Desde `seven_steps.yaml`, liste les pivots clés :
- Étape 1 (Faiblesse) : Où commence l'histoire ?
- Étape 2 (Désir) : Quel événement déclenche l'action ?
- Étape 3 (Opposant) : Qui/quoi apparaît comme obstacle ?
- Étape 4 (Plan) : Comment le héros se prépare ?
- Étape 5 (Bataille) : Quel affrontement majeur ?
- Étape 6 (Auto-révélation) : Quelle prise de conscience ?
- Étape 7 (Nouvel équilibre) : Quelle nouvelle réalité ?

#### Étape 2 : détailler les scènes entre les pivots

Entre chaque pivot majeur, ajoute des scènes qui :
- Développent le conflit progressivement
- Révèlent des informations au lecteur
- Nouent des alliances ou trahisons
- Créent des fausses victoires (midpoint reversal)

Exemple :
- Scènes 1-2 : Faiblesse + Inciting Event (étapes 1-2)
- Scènes 3-4 : Introduction Opposant (étape 3)
- Scènes 5-6 : Plan et préparation (étape 4)
- Scènes 7-9 : Bataille et révélations (étape 5)
- Scène 10+ : Auto-révélation et dénouement (étapes 6-7)

#### Étape 3 : relier les beats de genre

Pour chaque scène, identifie quel beat de genre elle valide :
- Consulte `genre_beats.yaml`
- Chaque scène doit valider au moins 1 beat (parfois 2-3)
- Les beats doivent être présents dans l'ordre logique du genre

#### Étape 4 : valider et affiner

```bash
# Vérifie que le scene_weave est structurellement valide
python -m cli.storykit validate

# Génère le prompt complet avec le weave
python -m cli.storykit assemble --target weave
```

### Utiliser le scene_weave pour générer les chapitres

Une fois le scene_weave validé, tu peux lancer la génération en batch :

```bash
# Le système charge automatiquement scene_weave.md
# et génère 1 chapitre par scène (ou groupe)
python -m cli.batch draft-chapters \
  --project "MonProjet" \
  --chapters "1,2,3,4,5,6,7,8,9,10" \
  --wait
```

**Le contexte injecté inclut** :
- La scène correspondante (fonction, lieu, conflit, décision)
- Les 7 étapes complètes
- Les beats de genre validés
- Le style défini
- La prémisse et l'argument moral

Chaque chapitre généré respecte donc la structure préparée.

### Checklist scene_weave

- ✅ **Chaque scène a une fonction Truby** (Ghost, Inciting Event, etc.)
- ✅ **Lieux distincts** (variation d'ambiance)
- ✅ **Conflits escaladants** (vers le climax)
- ✅ **Décisions irréversibles** (le héros avance toujours)
- ✅ **Beats de genre présents** (g01, g02... valides)
- ✅ **Pivots clés identifiés** :
  - First Revelation (première révélation)
  - Midpoint (point médian / retournement)
  - Battle (bataille majeure)
- ✅ **8-15 scènes minimum** pour un arc complet (ajustable selon la longueur)

### Exemple : du scene_weave au chapitre

**Scene_weave, Scène 5 :**
```
| 5 | Fake-Ally Opponent | Soirée littéraire | L'ami doute de la paternité | Rompre avec l'ami | g03 |
```

**Prompt généré pour le chapitre 5** :
```
Scène 5 — Fake-Ally Opponent
Lieu : Soirée littéraire
Conflit : Un ami (allié apparent) commence à douter que Léo ait vraiment écrit le texte.
Décision : Léo rompt avec cet ami pour protéger son secret.
Beat de genre : g03 (à valider selon genre_beats.yaml)

Contexte Truby :
- 7 étapes : [complètes]
- Argument moral : [thèse/antithèse/synthèse]
- Style : [Ton/Voix/Rythme]

Instructions : Générer la scène en 1500-2000 mots, respectant le style défini.
```

---

**Licence** : Apache License 2.0

---

## 8) Premiers pas

Trois commandes pour tester le flux minimal :

```powershell
# 1) Vérifier la cohérence des artefacts
python -m cli.storykit validate

# 2) Générer le prompt de la prémisse
python -m cli.storykit assemble --target premise

# 3) Ouvrir le prompt généré
# → out/prompts/YYYYMMDD_HHMMSS_premise.md
```

Ensuite, collez le prompt dans votre assistant IA et intégrez la réponse dans les fichiers du dossier `story/`.

### Ouvrir le dernier prompt généré (one‑liner PowerShell)

```powershell
# Ouvrir le plus récent dans Notepad
Get-ChildItem .\out\prompts -Filter *.md | Sort-Object LastWriteTime -Descending | Select-Object -First 1 | ForEach-Object { notepad $_.FullName }

# (Alternative) Ouvrir dans VS Code si disponible
Get-ChildItem .\out\prompts -Filter *.md | Sort-Object LastWriteTime -Descending | Select-Object -First 1 | ForEach-Object { code $_.FullName }
```

Ou via le script utilitaire :

```powershell
# Notepad par défaut
./tools/open-latest.ps1

# Ouvrir avec VS Code
./tools/open-latest.ps1 -Editor code
```

### Ouvrir la dernière réponse IA (script PowerShell)

```powershell
# Notepad par défaut
./tools/open-latest-response.ps1

# Ouvrir avec VS Code
./tools/open-latest-response.ps1 -Editor code
```

Pour plus de détails et options, voir [tools/README.md](tools/README.md)

## 3.2) Dossier templates/

Le dossier `templates/` contient des exemples de fichiers modèles (Markdown ou YAML) pour chaque artefact narratif attendu par StoryKit :

- `premise.example.md` : Exemple de prémisse structurée (phrase, principe organisateur, promesse).
- `seven_steps.example.yaml` : Exemple des 7 étapes Truby, pour structurer l’arc du protagoniste.
- `twenty_two_steps.example.yaml` : Exemple détaillé des 22 étapes Truby (pour récits complexes).
- `character_web.example.yaml` : Modèle pour cartographier les personnages et leurs fonctions.
- `moral_argument.example.md` : Exemple d’argument moral (thèse, antithèse, synthèse).
- `story_world.example.md` : Exemple de description du monde narratif.
- `symbol_web.example.yaml` : Modèle pour structurer les symboles récurrents du récit.
- `genre_choice.example.yaml` : Exemple de choix de genre, philosophie et promesse au lecteur.
- `genre_beats.example.yaml` : Modèle de beats de genre (moments-clés à respecter).
- `scene_weave.example.md` : Exemple de tissage de scènes (scene weave).
- `act_map.example.yaml` : Exemple de carte des actes/chapitres.
- `style.example.md`, `style.forbidden.example.md`, `style.advanced.example.md` : Exemples de styles d’écriture, d’interdits stylistiques et de variantes avancées.

Ces fichiers servent de référence pour créer tes propres artefacts dans le dossier story/. Ils garantissent la bonne structure, la cohérence des rubriques et facilitent la prise en main de StoryKit.
