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

## 2) Ce que fait StoryKit

StoryKit fournit :
- des **modèles** Markdown/YAML pour **prémisse**, **7 étapes**, **22 étapes**, **web de personnages**,
**argument moral**, **beats de genre**, **scene‑weave** ;
- un **CLI Python minimal** (`storykit`) qui **assemble un prompt** clair (contexte + instructions) à partir
de ces fichiers ;
- des **templates d’issues** (slash‑commands) pour guider la collaboration et garder la **traçabilité**.

> Le kit **n’impose pas** de modèle IA : tu restes libre d’utiliser Copilot, Claude, Gemini, etc.  
> L’assemblage produit un **prompt reproductible** que tu colles tel quel dans l’assistant IA.

---

## 3) Arborescence

```
story/
├─ premise/          # Prémisse & principe organisateur
├─ truby/            # 7 étapes, 22 étapes, web de personnages, argument moral, monde, symboles
├─ genre/            # Choix de genre & beats requis
├─ outline/          # Scene‑weave & carte des actes/chapitres
├─ research/         # Sources, notes (utile en non‑fiction)
├─ drafting/         # Brouillons de chapitres
├─ tasks/            # Tâches éditoriales
config/              # storykit.config.yaml (IA, langue)
cli/                 # storykit.py (assemble prompts) + adapters (stubs)
.github/ISSUE_TEMPLATE # Issues modèles (slash‑commands)
out/prompts/         # Prompts générés (dry‑run)
```

---

## 4) Installation

```bash
python -m venv .venv
# Sous Windows PowerShell :
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install pyyaml rich
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
| **gemini** | `google-generativeai` | `GOOGLE_API_KEY` | `gemini-1.5-pro` |

**Installation :**
```bash
# Choisir selon votre provider
pip install anthropic              # Claude
pip install openai                 # OpenAI/Copilot
pip install google-generativeai    # Gemini
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
  model: claude-3-5-sonnet-20241022  # ou: gpt-4o, gemini-1.5-pro
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

5) **Brouillon de chapitre** (à partir du scene‑weave)  
```bash
python -m cli.storykit assemble --target draft --chapter 1
```

> Chaque commande génère `out/prompts/YYYYMMDD_HHMMSS_<target>.md`.  
> **Colle** ce prompt dans ton assistant IA, **intègre** la réponse dans les fichiers du dossier `story/`, puis **commit**.

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
  model: gemini-1.5-pro                 # Recommandé
  # model: gemini-1.5-flash             # Plus rapide
  # model: gemini-2.0-flash-exp         # Expérimental (si accès)
  max_tokens: 4096
```

**Conseils d'usage :**
- **Premise/Genre** : modèles légers suffisent (Haiku, GPT-3.5, Flash)
- **Truby7/22, Weave** : modèles équilibrés (Sonnet, GPT-4o, Pro)
- **Draft** : modèles puissants (Opus, GPT-4o, Pro) + `max_tokens: 8192` pour chapitres longs

---

## 7) Workflow recommandé (Truby → texte)

**Phase 1 — Intention**
- `premise/premise.md` : 1 phrase + principe organisateur + promesse de genre.  
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

**Licence** : MIT
