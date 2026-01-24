# StoryKit — Écrire avec la méthode Truby + un workflow "spec-driven"

StoryKit transpose à l'écriture (roman, fiction, non-fiction narrative) une logique inspirée de SpecKit :
on **prépare des artefacts** (Markdown/YAML) qui rendent les intentions **claires et vérifiables**, puis on
**assemble un prompt** propre et reproductible à destination d'un assistant IA (au choix), sans runtime
propriétaire.

> Principe : **commande → artefacts → prompt → IA → texte**.

---

## 1) Pourquoi la méthode Truby ?

John Truby est un pédagogue de la dramaturgie reconnu pour une approche **organique** de l'histoire,
qui dépasse la stricte "structure en trois actes". Son cadre relie **personnages, intrigue, thème,
monde et symboles** dans un système vivant où chaque élément agit sur les autres. Truby met
notamment l'accent sur :  
- une **prémisse** forte (la "graine" qui détermine le potentiel du récit),  
- un **fil thématique** formulé en **argument moral** (thèse ↔ antithèse ↔ synthèse),  
- une **progression** structurée par les **7 étapes fondamentales** et, au besoin, par **22 étapes**
plus détaillées,  
- le **web de personnages** (contrastes/fonctions),  
- un **scene‑weave** (tissage de scènes) préparé **avant** la rédaction.

### 1.1 Les 7 étapes fondamentales
Le "squelette" que partagent toutes les bonnes histoires selon Truby :
**faiblesse & besoin → désir → opposant → plan → bataille → auto‑révélation → nouvel équilibre**.
Elles modélisent la transformation du/de la protagoniste et rendent l'arc **nécessaire** et **satisfaisant**.

### 1.2 Les 22 étapes (pour les récits plus denses)
Les **22 steps** détaillent les pivots (révélations/décisions, fausse défaite, "visite à la mort",
bataille, décision morale, etc.) et aident à tisser une progression **précise** qui reste logique mais
surprenante. C'est une extension **pratique** — pas un carcan — pour prévenir les "trous" de causalité.

### 1.3 Web de personnages, argument moral, monde & symboles
- **Web de personnages** : définir chacun par **contraste** (valeurs, fonctions dramatiques).  
- **Argument moral** : articuler **thèse/antithèse** et viser une **synthèse incarnée** par les actes
(éviter le "message plaqué").  
- **Monde & symboles** : le **story world** reflète l'intériorité du héros et les **symboles** compressent
du sens pour guider scènes et motifs.

### 1.4 Genres : promesse, "beats" et philosophie
Dans *The Anatomy of Genres*, Truby montre que chaque genre s'appuie sur des **beats** profonds (événements
structurants) et **porte une philosophie** (une "manière d'agir dans le monde"). Maîtriser ces beats est
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
- des **templates d'issues** (slash‑commands) pour guider la collaboration et garder la **traçabilité**.

> Le kit **n'impose pas** de modèle IA : vous restez libre d'utiliser Copilot, Claude, Gemini, etc.  
> L'assemblage produit un **prompt reproductible** que vous collez tel quel dans l'assistant IA.

---

## 3) Arborescence — Architecture multi-livres

**Depuis janvier 2026**, StoryKit supporte **plusieurs livres indépendants** dans un seul repository :

```
Repository/
├─ .venvWORK/              # Environnement virtuel Python (ou .venv)
├─ .vscode/
│  └─ tasks.json           # Tâches VS Code pour batch.py
├─ .env / .env.example     # Variables d'environnement (clés API, config)
├─ storykit-run.ps1        # ✨ Helper pour CLI (cross-directory)
├─ storykit-run.sh         # ✨ Helper pour CLI (Linux/macOS)
├─ batch-run.ps1           # ✨ Helper pour batch (cross-directory)
├─ batch-run.sh            # ✨ Helper pour batch (Linux/macOS)
│
├─ cli/                    # 🐍 Modules Python
│  ├─ storykit.py          # CLI principal (validate, assemble)
│  ├─ batch.py             # CLI batch (draft-variants, research, etc.)
│  ├─ validate.py          # Validations YAML/MD
│  └─ adapters/            # Adaptateurs IA (Claude, OpenAI, Gemini)
│     ├─ base.py
│     ├─ claude.py
│     ├─ copilot.py
│     └─ gemini.py
│
├─ tools/                  # 🔧 Scripts utilitaires
│  ├─ storykit-run.sh      # Helper Linux/macOS
│  ├─ batch-run.sh         # Helper Linux/macOS
│  ├─ open-latest.ps1      # Ouvrir dernier prompt (Windows)
│  ├─ open-latest-response.ps1
│  └─ README.md
│
├─ templates/              # 📋 Modèles d'artefacts
│  ├─ Truby/
│  │  ├─ premise.example.md
│  │  ├─ seven_steps.example.yaml
│  │  ├─ twenty_two_steps.example.yaml
│  │  ├─ character_web.example.yaml
│  │  ├─ moral_argument.example.md
│  │  ├─ story_world.example.md
│  │  └─ symbol_web.example.yaml
│  ├─ Genre/
│  │  ├─ genre_choice.example.yaml
│  │  └─ genre_beats.example.yaml
│  ├─ Outline/
│  │  ├─ act_map.example.yaml
│  │  └─ scene_weave.example.md
│  └─ Style/
│     ├─ style.example.md
│     ├─ style.forbidden.example.md
│     ├─ style.advanced.example.md
│     └─ style.md.example.md
│
├─ livre1-truby/           # 📖 PROJET 1 (isolé, structure complète)
│  ├─ storykit.config.yaml # Config du projet
│  ├─ story/
│  │  ├─ truby/            # Prémisse, 7 étapes, 22 étapes, web, argument moral, monde, symboles
│  │  │  ├─ premise.md
│  │  │  ├─ seven_steps.yaml
│  │  │  ├─ twenty_two_steps.yaml    # Optionnel
│  │  │  ├─ character_web.yaml
│  │  │  ├─ moral_argument.md
│  │  │  ├─ story_world.md           # Optionnel
│  │  │  └─ symbol_web.yaml          # Optionnel
│  │  ├─ genre/            # Choix de genre & beats
│  │  │  ├─ genre_choice.yaml
│  │  │  └─ genre_beats.yaml
│  │  ├─ outline/          # Scene‑weave & carte actes/chapitres
│  │  │  ├─ scene_weave.md
│  │  │  └─ act_map.yaml              # Optionnel
│  │  ├─ config/           # Configuration stylistique
│  │  │  └─ style.md       # Ton, Voix, Rythme (requis)
│  │  ├─ research/         # Sources, notes, documentation
│  │  │  └─ *.md
│  │  ├─ drafting/         # Brouillons de chapitres
│  │  │  ├─ LeSilenceDesAlgorithmes/
│  │  │  ├─ SolitudeGeometrique/
│  │  │  ├─ ClaudeSonnet4-5/
│  │  │  └─ Gemini3/
│  │  └─ tasks/            # Tâches éditoriales
│  │     └─ tasks.yaml
│  └─ out/                 # 💾 Artefacts générés (par livre!)
│     ├─ prompts/          # Prompts assemblés
│     │  ├─ 20260124_132149_premise.md
│     │  ├─ 20260124_132214_truby7.md
│     │  ├─ ...
│     │  └─ YYYYMMDD_HHMMSS_<target>.md
│     └─ responses/        # Réponses IA téléchargées
│        └─ YYYYMMDD_HHMMSS_<target>_response.md
│
├─ livre2-monsoon/         # 📖 PROJET 2 (structure identique, isolée)
│  ├─ storykit.config.yaml
│  ├─ story/
│  │  ├─ truby/
│  │  ├─ genre/
│  │  ├─ outline/
│  │  ├─ config/
│  │  ├─ research/
│  │  ├─ drafting/
│  │  └─ tasks/
│  └─ out/                 # Prompts/réponses ISOLÉS pour livre2
│     ├─ prompts/
│     └─ responses/
│
├─ [autres livres...]      # Ajouter autant de livres que nécessaire
│
├─ Documentation
│  ├─ README.md            # Ce fichier
│  ├─ TRUBY_GUIDE.md       # Guide Truby complet
│  ├─ BATCH_README.md      # Documentation batch API
│  ├─ AUDIT_REPORT.md      # Historique améliorations
│  └─ LICENSE
│
└─ custom-styles/          # 🎨 Styles personnalisés (optionnel)
```

**Points clés :**
- **Chaque livre** = dossier indépendant avec sa propre config et artefacts
- **Détection automatique** : CLI détecte le livre en cherchant `storykit.config.yaml` en remontant depuis le répertoire courant
- **Isolement complet** : prompts/réponses sont dans `livre/out/`, **pas** dans un dossier global
- **Helpers cross-directory** : `storykit-run.ps1` et `batch-run.ps1` permettent d'utiliser le CLI/batch de n'importe quel répertoire

### 3.1) Fichiers obligatoires et optionnels

#### Fichiers obligatoires (requis pour `validate`)

La commande `../storykit-run.ps1 validate` vérifie la présence et la cohérence de **5 fichiers minimum** :

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

- **`story/truby/premise.md`**  
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

### 3.2) Améliorations récentes (Janvier 2026)

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

**Architecture multi-livres (Janvier 2026) :**
- ✅ Chaque livre = dossier indépendant avec config et artefacts isolés
- ✅ Détection automatique du livre en remontant depuis le répertoire courant
- ✅ Prompts/réponses isolés dans `livre/out/` (pas de mélange global)
- ✅ Helpers PowerShell (`storykit-run.ps1`, `batch-run.ps1`) pour cross-directory
- ✅ Support de la Batch API Anthropic pour parallélisation massive

---

## 4) Installation & Configuration

### Étape 1 — Environnement Python

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

### Étape 2 — Clés API

```powershell
# Créer le fichier .env à partir du template
Copy-Item .env.example .env

# Éditer .env et renseigner vos clés
notepad .env

# (Optionnel) Définir les clés API pour la session courante
$env:ANTHROPIC_API_KEY = "sk-ant-..."    # Claude
$env:OPENAI_API_KEY    = "sk-proj-..."   # OpenAI / Copilot
$env:GOOGLE_API_KEY    = "AIza..."       # Gemini
```

### Étape 3 — Configuration par livre

Chaque livre possède son propre `storykit.config.yaml` (voir section « Configuration »).
Pour modifier la config d'un livre spécifique :

```powershell
# Depuis n'importe quel répertoire
cd livre1-truby
notepad storykit.config.yaml

cd ../livre2-monsoon
notepad storykit.config.yaml
```

### Windows PowerShell — aide‑mémoire

```powershell
# Activer l'environnement virtuel (depuis le repo root)
.venv\Scripts\Activate.ps1

# Vérifier l'interpréteur Python utilisé
python -c "import sys; print(sys.executable)"

# Depuis n'importe quel répertoire (livre1-truby, livre2-monsoon, etc.)
../storykit-run.ps1 validate
../storykit-run.ps1 assemble --target premise
../batch-run.ps1 list --limit 10

# Si vous préférez utiliser Python directement (depuis repo root)
.venv\Scripts\python.exe -m cli.storykit validate
.venv\Scripts\python.exe -m cli.batch list --limit 10
```

**Encodage UTF-8 (Windows PowerShell):**  
Les helpers `storykit-run.ps1` et `batch-run.ps1` **forcent automatiquement** l'encodage UTF-8 pour PowerShell.  
Si vous utilisez directement `python -m cli.*`, définissez l'encodage manuellement:

```powershell
# Pour la session courante
$env:PYTHONIOENCODING = "utf-8"
python -m cli.storykit validate

# Ou permanent : ajouter à votre profil PowerShell
notepad $PROFILE
# Ajouter la ligne : $env:PYTHONIOENCODING="utf-8"
```

### Linux / macOS — aide‑mémoire

```bash
# Activer l'environnement virtuel (depuis le repo root)
source .venv/bin/activate

# Vérifier l'interpréteur Python utilisé
python -c "import sys; print(sys.executable)"

# Depuis n'importe quel répertoire (livre1-truby, livre2-monsoon, etc.)
../storykit-run.sh validate
../storykit-run.sh assemble --target premise
../batch-run.sh list --limit 10

# Si vous préférez utiliser Python directement (depuis repo root)
python -m cli.storykit validate
python -m cli.batch list --limit 10
```

**Encodage UTF-8 (Linux / macOS):**  
Les helpers `storykit-run.sh` et `batch-run.sh` **forcent automatiquement** l'encodage UTF-8.  
Si vous utilisez directement `python -m cli.*`, définissez l'encodage en session:

```bash
# Pour la session courante
export PYTHONIOENCODING=utf-8
python -m cli.storykit validate

# Ou permanent : ajouter à votre ~/.bashrc ou ~/.zshrc
echo 'export PYTHONIOENCODING=utf-8' >> ~/.bashrc
source ~/.bashrc
```

---

## 5) Configuration

Chaque livre possède sa propre config : **`livre/storykit.config.yaml`**

```yaml
ai:
  provider: dry-run        # dry-run | claude | copilot | gemini
  model: ""                # ex: claude-3-5-sonnet-20241022, gpt-4o, gemini-2.5-flash
  max_tokens: 8000         # Budget de sortie (8000 recommandé pour chapitres complets)
project:
  root: ./story            # Relatif au dossier du livre (ne pas modifier)
language: fr
format:
  line_width: 100
style:
  autofix: true            # insérer automatiquement le squelette Ton/Voix/Rythme si manquant
  optional_autofix: none   # none | forbidden | examples | both (sections optionnelles)
```

**Chemins importants** (détectés automatiquement) :
- `Config` : `livre/storykit.config.yaml`
- `Story root` : `livre/story/`
- `Output prompts` : `livre/out/prompts/`
- `Output responses` : `livre/out/responses/`

La détection fonctionne en remontant depuis le répertoire courant pour trouver le premier `storykit.config.yaml`.

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
../storykit-run.ps1 assemble --target truby7

# Les fichiers générés :
# - livre/out/prompts/YYYYMMDD_HHMMSS_truby7.md (prompt envoyé)
# - livre/out/responses/YYYYMMDD_HHMMSS_truby7_response.md (réponse IA)
```

Les adaptateurs se chargent dynamiquement selon les modules installés et les clés disponibles.

### Prompt Caching (Claude) — Réduire les coûts de ~90%

L'adaptateur Claude implémente le **Prompt Caching** d'Anthropic pour réduire drastiquement les coûts sur les appels répétés.

**Comment ça marche :**
- Le contexte stable (prémisse, style, artefacts Truby, beats) est automatiquement mis en cache
- Les instructions finales (variables selon la commande) ne sont pas cachées
- Cache valide pendant **~5 minutes**
- **Minimum 1024 tokens** requis pour activer le cache

**Économies réelles :**

Premier appel (création du cache) :
```bash
../storykit-run.ps1 assemble --target truby7
# [Cache: 6582 créés, 0 lus]
# → Coût normal sur 6582 tokens + petite surcharge de création
```

Appels suivants (< 5 min) :
```bash
../storykit-run.ps1 assemble --target truby7
# [Cache: 6582 lus]
# → ~90% d'économie sur les 6582 tokens en cache !
```

**Stratégies d'optimisation :**

1. **Enchaînez vos commandes rapidement** (< 5 min entre chaque)
   ```bash
   ../storykit-run.ps1 assemble --target truby7
   # Analyser la réponse, ajuster les fichiers
   ../storykit-run.ps1 assemble --target truby22  # Cache réutilisé !
   ../storykit-run.ps1 assemble --target weave    # Cache réutilisé !
   ```

2. **Itérations rapides** : testez plusieurs versions d'une même commande
   ```bash
   # Modifier story/truby/seven_steps.yaml
   ../storykit-run.ps1 assemble --target truby7
   # Ajuster encore...
   ../storykit-run.ps1 assemble --target truby7  # Cache réutilisé
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

### Style & Voix
- Emplacement: `story/config/style.md`. Ce fichier définit le ton, la voix et le rythme attendus.
- Rubriques requises: Titres ou labels pour **Ton**, **Voix**, **Rythme** (ex: `# Ton` ou `Ton:`).
- Inclusion automatique: la section "Style & Voix" est ajoutée au prompt assemblé après la **Prémisse**.
- Rappels d'instructions: un rappel "Respecter le style défini dans Style & Voix." est inclus pour `truby7`, `truby22`, `weave` et `draft`.
- Validation: `../storykit-run.ps1 validate` vérifie que `style.md` contient ces rubriques.
- Auto-fix: si `style.autofix: true` (par défaut), les rubriques manquantes sont ajoutées automatiquement avec un squelette et un message est affiché.
- Désactiver ponctuellement: `../storykit-run.ps1 validate --no-autofix-style` (prioritaire sur la config).
- Sections optionnelles: `optional_autofix` contrôle l'insertion automatique de sections facultatives :
  - `none` (défaut) : Ton/Voix/Rythme uniquement
  - `forbidden` : ajoute "Interdits stylistiques" si absente
  - `examples` : ajoute "Éxemples" (conforme/non conforme) si absente
  - `both` : ajoute les deux sections facultatives

Exemples d'usage :
```bash
# Config par défaut (Ton/Voix/Rythme uniquement)
../storykit-run.ps1 validate

# Activer auto-insertion des interdits : éditer storykit.config.yaml
# style:
#   optional_autofix: forbidden
../storykit-run.ps1 validate
# → affiche "Section 'Interdits' ajoutée" si absente

# Activer auto-insertion des exemples et interdits
# style:
#   optional_autofix: both
../storykit-run.ps1 validate
```

Conseils pratiques pour `style.md`:
- Clarté: phrases concrètes, critères observables (éviter les injonctions vagues).
- Voix: préciser focalisation, niveau de langue, champs lexicaux à privilégier/éviter.
- Rythme: donner des repères (longueur moyenne de phrases, variation court/long, taille des paragraphes).
- Exemples: 2–3 mini-exemples de style conforme et non conforme aident beaucoup l'IA.
- Cohérence: garder `style.md` bref et resserré; c'est un contrat stylistique.

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

### Utilisation via helpers PowerShell (recommandé)

```powershell
# Depuis n'importe quel répertoire (livre1-truby, livre2-monsoon, etc.)
# Aucun besoin d'activer .venv ou de cd au repo root

../storykit-run.ps1 validate
../storykit-run.ps1 assemble --target premise
../storykit-run.ps1 assemble --target truby7 --styles minimaliste
../batch-run.ps1 list --limit 10
../batch-run.ps1 download msgbatch_XXXX
```

### Utilisation directe (depuis le repo root)

```powershell
# Activer l'environnement virtuel
.venv\Scripts\Activate.ps1

# Puis changer vers le livre désiré
cd livre1-truby
python -m cli.storykit validate
python -m cli.storykit assemble --target premise

cd ../livre2-monsoon
python -m cli.batch list --limit 10
```

### Assemble : générer des prompts

1) **Affiner la prémisse** (1 phrase + principe organisateur)  
```powershell
../storykit-run.ps1 assemble --target premise
```

2) **7 étapes** (faiblesse/besoin → nouvel équilibre)  
```powershell
../storykit-run.ps1 assemble --target truby7
```

3) **22 étapes** (chaînage fin : révélations, décisions, gauntlet…)  
```powershell
../storykit-run.ps1 assemble --target truby22
```

4) **Scene‑weave** (liste de scènes, conflit/décision/valeur/beat de genre)  
```powershell
../storykit-run.ps1 assemble --target weave
```

5) **Genre (beats + choix)**  
```powershell
../storykit-run.ps1 assemble --target genre
```

6) **Web de personnages**  
```powershell
../storykit-run.ps1 assemble --target web
```

7) **Brouillon de chapitre** (à partir du scene‑weave)  
```powershell
../storykit-run.ps1 assemble --target draft --chapter 1
```

> Chaque commande génère `livre/out/prompts/YYYYMMDD_HHMMSS_<target>.md`.  
> Les prompts sont **isolés par livre** : `livre1-truby/out/` vs `livre2-monsoon/out/`.  
> **Collez** ce prompt dans votre assistant IA, **intégrez** la réponse dans `livre/story/`, puis **commit**.

### Validate : vérifier la cohérence

```powershell
# Valider le livre courant
../storykit-run.ps1 validate

# Désactiver l'auto-fix de style.md
../storykit-run.ps1 validate --no-autofix-style
```

**Contrôles effectués :**
- `genre_choice.yaml` : genre valide, structure correcte
- `genre_beats.yaml` : ids uniques (gNN), statuts valides, noms présents
- `seven_steps.yaml` : champs requis (weakness_need.internal, desire, opponent.name)
- `scene_weave.md` : présence de pivots (First Revelation/Midpoint/Battle), références aux beats valides
- `style.md` : rubriques Ton/Voix/Rythme présentes (auto-fix selon config)

Si des problèmes sont détectés, un tableau récapitulatif s'affiche avec le numéro et le message d'erreur.

### Choix des modèles LLM

Modifier `livre/storykit.config.yaml` selon le provider :

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

La commande `../storykit-run.ps1 assemble` lit automatiquement `ai.model` et `ai.max_tokens` depuis `livre/storykit.config.yaml` et les transmet aux adaptateurs via `meta`. Cela signifie :

- Si vous définissez `model: gemini-2.5-pro`, ce modèle sera utilisé pour **tous les appels**.
- Si vous laissez `model: ""` (vide), l'adaptateur applique sa logique par défaut (ex. Gemini choisit flash ou pro selon la tâche).

**Sélection automatique du modèle Gemini :**

Par défaut, si `model:` est vide, StoryKit choisit automatiquement le modèle Gemini le plus adapté selon la tâche :

- `premise`, `genre`, `truby7` : modèle rapide/économique (`gemini-2.5-flash`)
- `draft`, `truby22`, `weave` : modèle qualitatif/long (`gemini-2.5-pro`)

Si vous renseignez explicitement `model:` dans la config, ce modèle sera utilisé pour tous les appels (override). Sinon, la sélection automatique s'applique.

Ce mécanisme garantit :
- Robustesse (jamais d'erreur 404 si un modèle disparaît)
- Performance optimale selon la tâche
- Liberté utilisateur pour forcer un modèle précis si besoin

> Astuce : vous pouvez toujours surcharger ponctuellement le modèle via la config YAML ou en passant `model` dans les options avancées Python.
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
- `outline/scene_weave.md` : tissage des scènes **avant** d'écrire (conflit, décision, valeur, beat).

**Phase 4 — Rédaction & révisions**
- `drafting/` : brouillons de chapitres via `--target draft`.  
- Relectures centrées sur **l'argument moral** et les **valeurs** scène par scène.  
- Ajuster les **beats de genre** pour honorer la promesse au lectorat.

---

**Licence** : Apache License 2.0

---

## 8) Premiers pas — Architecture multi-livres

Trois commandes pour tester le flux minimal dans un livre spécifique :

```powershell
# 1) Se placer dans le répertoire du livre
cd livre1-truby

# 2) Vérifier la cohérence des artefacts (détecte auto le livre)
../storykit-run.ps1 validate

# 3) Générer le prompt de la prémisse
../storykit-run.ps1 assemble --target premise

# 4) Ouvrir le prompt généré
# → livre1-truby/out/prompts/YYYYMMDD_HHMMSS_premise.md
```

Ensuite, collez le prompt dans votre assistant IA et intégrez la réponse dans `livre1-truby/story/`.

### Basculer vers un autre livre

```powershell
# Changer vers livre2-monsoon
cd ../livre2-monsoon

# Même flux, mais dans le contexte de livre2-monsoon
../storykit-run.ps1 validate
../storykit-run.ps1 assemble --target premise

# Les outputs se créent dans livre2-monsoon/out/prompts/
# → Isolement complet garanti
```

### Ajouter un nouveau livre

```powershell
# Copier la structure d'un livre existant
Copy-Item -Recurse livre1-truby livre3-nouveau-projet

# Éditer la config
cd livre3-nouveau-projet
notepad storykit.config.yaml

# Modifier les artefacts dans story/ selon vos besoins
# La détection automatique fonctionne immédiatement
../storykit-run.ps1 validate
```

### Ouvrir le dernier prompt généré

```powershell
# Depuis n'importe quel répertoire du livre (livre1-truby, livre2-monsoon, etc.)
# Les scripts ouvrent le dernier fichier du dossier courant

# Ouvrir avec Notepad (par défaut)
../../tools/open-latest.ps1

# Ouvrir avec VS Code
../../tools/open-latest.ps1 -Editor code
```

Pour plus de détails et options, voir [tools/README.md](tools/README.md)

### Ouvrir la dernière réponse IA

```powershell
# Depuis n'importe quel répertoire du livre

# Ouvrir avec Notepad
../../tools/open-latest-response.ps1

# Ouvrir avec VS Code
../../tools/open-latest-response.ps1 -Editor code
```

> **Note** : En mode dry-run, `out/responses/` est vide. Les scripts basculent automatiquement vers le dernier prompt si aucune réponse n'est disponible.

## 3.2) Dossier templates/

Le dossier `templates/` contient des exemples de fichiers modèles (Markdown ou YAML) pour chaque artefact narratif attendu par StoryKit :

- `premise.example.md` : Exemple de prémisse structurée (phrase, principe organisateur, promesse).
- `seven_steps.example.yaml` : Exemple des 7 étapes Truby, pour structurer l'arc du protagoniste.
- `twenty_two_steps.example.yaml` : Exemple détaillé des 22 étapes Truby (pour récits complexes).
- `character_web.example.yaml` : Modèle pour cartographier les personnages et leurs fonctions.
- `moral_argument.example.md` : Exemple d'argument moral (thèse, antithèse, synthèse).
- `story_world.example.md` : Exemple de description du monde narratif.
- `symbol_web.example.yaml` : Modèle pour structurer les symboles récurrents du récit.
- `genre_choice.example.yaml` : Exemple de choix de genre, philosophie et promesse au lecteur.
- `genre_beats.example.yaml` : Modèle de beats de genre (moments-clés à respecter).
- `scene_weave.example.md` : Exemple de tissage de scènes (scene weave).
- `act_map.example.yaml` : Exemple de carte des actes/chapitres.
- `style.example.md`, `style.forbidden.example.md`, `style.advanced.example.md` : Exemples de styles d'écriture, d'interdits stylistiques et de variantes avancées.

Ces fichiers servent de référence pour créer tes propres artefacts dans le dossier story/. Ils garantissent la bonne structure, la cohérence des rubriques et facilitent la prise en main de StoryKit.
