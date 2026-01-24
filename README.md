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

StoryKit supporte plusieurs livres indépendants dans un seul repository :

```
.env
.env.example
.git/
.github/
.gitignore
.venvHOME/
.venvWORK/
.vscode/
AUDIT_REPORT.md
BATCH_README.md
cli/
  adapters/
  batch.py
  storykit.py
  validate.py
  __pycache__/
custom-styles/
LICENSE
README.md
requirements.txt
temp/
  deleted-files-unstaged.txt
  image-cache/
templates/
  Genre/
  Outline/
  Style/
  Truby/
tools/
  batch-run.ps1
  batch-run.sh
  load-aliases.ps1
  open-latest-response.ps1
  open-latest.ps1
  README.md
  storykit-run.ps1
  storykit-run.sh
TRUBY_GUIDE.md
writing/
  livre1-truby/
    out/
    story/
      config/
      drafting/
      genre/
      outline/
      research/
      tasks/
      truby/
    storykit.config.yaml
  livre2-maigretlike/
    out/
    story/
      config/
      drafting/
      genre/
      outline/
      research/
      tasks/
      truby/
    storykit.config.yaml
  livre3-sana/
    out/
    story/
      config/
        style.md
      drafting/
      genre/
        genre_beats.md
        genre_beats.yaml
        genre_choice.yaml
      outline/
        act_map.yaml
        scene_weave.md
      research/
      tasks/
      truby/
        character_web.yaml
        moral_argument.md
        premise.md
        seven_steps.yaml
        story_world.md
        symbol_web.yaml
    storykit.config.yaml
```

Chaque livre possède sa propre structure, artefacts et configuration, garantissant l’isolement des prompts et des réponses IA. Les scripts et helpers fonctionnent dans tous les sous-dossiers, et l’ajout d’un nouveau livre se fait simplement en copiant la structure existante.
