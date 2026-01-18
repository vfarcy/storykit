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
     - `weakness_need.internal` : faiblesse psychologique du protagoniste
     - `desire` : objectif conscient poursuivi
     - `opponent.name` : identité de l'opposant principal

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

---

## 5) Configuration

Édite `story/config/storykit.config.yaml` :

```yaml
ai:
  provider: dry-run        # dry-run | claude | copilot | gemini
  model: ""                # ex: claude-3-5-sonnet, gpt-4o, gemini-1.5
  max_tokens: 1800
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

**Économies réelles :**

Premier appel (création du cache) :
```bash
python -m cli.storykit assemble --target truby7
# [Cache: 6582 créés, 0 lus]
# → Coût normal sur 6582 tokens + petite surcharge de création
```

Appels suivants (< 5 min) :
```bash
python -m cli.storykit assemble --target truby7
# [Cache: 6582 lus]
# → ~90% d'économie sur les 6582 tokens en cache !
```

**Stratégies d'optimisation :**

1. **Enchaînez vos commandes rapidement** (< 5 min entre chaque)
   ```bash
   python -m cli.storykit assemble --target truby7
   # Analyser la réponse, ajuster les fichiers
   python -m cli.storykit assemble --target truby22  # Cache réutilisé !
   python -m cli.storykit assemble --target weave    # Cache réutilisé !
   ```

2. **Itérations rapides** : testez plusieurs versions d'une même commande
   ```bash
   # Modifier story/truby/seven_steps.yaml
   python -m cli.storykit assemble --target truby7
   # Ajuster encore...
   python -m cli.storykit assemble --target truby7  # Cache réutilisé
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

### Assemble : générer des prompts

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
- **Draft** : modèles puissants (Opus, GPT-4o, Pro) + `max_tokens: 8192` pour chapitres longs

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

**Phase 4 — Rédaction & révisions**
- `drafting/` : brouillons de chapitres via `--target draft`.  
- Relectures centrées sur **l’argument moral** et les **valeurs** scène par scène.  
- Ajuster les **beats de genre** pour honorer la promesse au lectorat.

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
