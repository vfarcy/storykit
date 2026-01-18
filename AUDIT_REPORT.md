# Rapport d'Audit — StoryKit

**Date :** 18 janvier 2026  
**Portée :** Code Python, documentation, configuration, dépendances  
**Verdict global :** 🟡 **BON avec recommandations critiques**

---

## 1. Structure et Organisation

### ✅ Points forts

- **Arborescence logique et bien organisée** : `cli/`, `story/`, `templates/`, `tools/` séparés clairement
- **Conventions de nommage cohérentes** : fichiers, dossiers, variables (snake_case)
- **Fichiers de config centralisés** : `.env`, `storykit.config.yaml`, `requirements.txt`
- **Documentation complète** : README très détaillé (712 lignes), TRUBY_GUIDE.md
- **Git bien configuré** : `.gitignore`, `.github/ISSUE_TEMPLATE` présent

### ⚠️ Améliorations possibles

- **Aucun fichier `__init__.py` dans `cli/adapters/`** → risque d'import fragile
  - **Fix :** Ajouter `cli/adapters/__init__.py` pour expliciter le package
- **Dossier `out/` non gitignore** → les prompts/réponses générées sont versionnées
  - **Fix :** Ajouter `out/` à `.gitignore`

---

## 2. Qualité du Code Python

### ✅ Points forts

- **Gestion d'erreurs robuste** : try/except sur les imports optionnels (anthropic, openai, google-genai)
- **Fallback intelligents** : si `rich` non dispo, utilise classes de secours
- **Séparation des responsabilités** : CLI, adapters, validation dans des modules distincts
- **Utilisation de `pathlib.Path`** : chemins cross-platform corrects
- **Docstrings présentes** : toutes les fonctions principales documentées
- **Prompt Caching bien implémenté** : réduction ~90% des coûts Claude

### 🔴 Erreurs critiques détectées

#### **claude.py — Erreurs de typage (Pylance)**

1. **Ligne 57 :** Paramètre `system` reçoit une liste au lieu d'une string ou itérable
   ```python
   system=system_blocks,  # ❌ Devrait être une list de TextBlockParam, pas dict bruts
   ```
   **Fix :** Utiliser le type correct de la lib Anthropic

2. **Ligne 68 :** Accès à `.text` sur tous les types de content block
   ```python
   content = response.content[0].text  # ❌ ThinkingBlock, ToolUseBlock n'ont pas .text
   ```
   **Fix :** Filtrer par type ou utiliser une boucle sécurisée

3. **Ligne 83 :** Référence à `anthropic.APIError` quand `anthropic` peut être `None`
   ```python
   except anthropic.APIError as e:  # ❌ anthropic peut être None au runtime
   ```
   **Fix :** Utiliser `Exception` générique ou vérifier le type

#### **validate.py — Duplication de code**

- Même code de validation existe dans `storykit.py` ET `validate.py`
- **Fix :** Centraliser dans un module `cli/validators.py`

### ⚠️ Points d'attention

- **Pas de type hints complets** : `send()` reçoit `dict` sans typage (dict[str, Any])
  - **Impact faible :** Le code fonctionne, mais rend la maintenance plus difficile
- **Pas de logging** : Tous les messages via `console.print()` (pas de trace structurée)
  - **Recommandation :** Ajouter `logging.getLogger()` pour CI/CD

---

## 3. Documentation

### ✅ Points forts

- **README extraordinaire** : 712 lignes, très complet
  - Explication de Truby
  - Flux complet (Installation → Commandes → Workflow)
  - Sections "Prompt Caching" bien expliquées (nouveau)
  - Exemples PowerShell utiles
- **TRUBY_GUIDE.md** : Guide pédagogique complet
- **Commentaires en code** : bien présents, en français

### ⚠️ Amélirations

- **Pas de docstring module** : `cli/adapters/base.py` manque
- **Pas de guide contribution** : CONTRIBUTING.md absent
- **Pas de CHANGELOG** : Difficile de tracer les évolutions
- **Pas de API docs générées** : Pour les développeurs de plugins

---

## 4. Configuration et Dépendances

### ✅ Points forts

- **requirements.txt allégé** (11 lignes seulement)
- **Dépendances optionnelles clairement marquées** (anthropic, openai, google-genai)
- **.env.example présent** : guide pour les clés API
- **storykit.config.yaml bien structuré**

### 🟡 Attention

- **Google Generative AI** : Import recent (google.genai vs google.generativeai)
  - Risque d'obsolescence si changements d'API
  - **Recommandation :** Tester régulièrement

---

## 5. Tests et Couverture

### 🔴 Critique : Aucun test automatisé

**Constat :**
- ❌ Pas de fichier `test_*.py`
- ❌ Pas de `pytest.ini` ou `tox.ini`
- ❌ Pas de couverture de code mesurée
- ❌ Pas de CI/CD (GitHub Actions, etc.)

**Impact :**
- Risque de régressions silencieuses
- Impossible de déployer en confiance
- Maintenance difficile

**Recommandation critique :**
```bash
# Créer tests minimaux pour :
test_cli/
  ├── test_storykit.py          # Tests de CLI parsing
  ├── test_validation.py         # Tests des validations YAML
  ├── test_adapters.py           # Tests des adapters (mock API)
  └── test_prompt_assembly.py    # Tests de construction de prompts
```

---

## 6. Sécurité

### ✅ Points forts

- **Gestion sécurisée des clés API** : via `.env` (jamais en dur)
- **Clés API non affichées en console** (évite les fuites de logs)
- **Encoding UTF-8 explicite** : sur tous les fichiers

### ⚠️ Attention

- **Pas de validation input** : Les noms de chapitres/targets ne sont pas validés
  - **Risque faible :** CLI contrôlé, mais attention en cas d'API web future
- **Path traversal potentiel** : Si les chemins de fichiers viennent d'input externe
  - **Mitigation :** Utiliser `pathlib.resolve()` pour vérifier qu'on ne sort pas de `STORY`

---

## 7. Performance et Optimisations

### ✅ Excellent

- **Prompt Caching Claude implémenté** ✨
  - Réduit les coûts de ~90% sur appels répétés
  - Économies réelles mesurées (6582 tokens cachés)
- **Chargement lazy** des modules optionnels (anthropic, openai, etc.)

### 🟡 Opportunités

- **Cache local de prompts** : Pourrait éviter regeneration avec mêmes artefacts
  - Coût très faible (checksumming YAML)
- **Parallelisation** : Si chapitre = Draft complet, on pourrait générer chapitres en parallèle

---

## 8. Problèmes Critiques à Adresser Immédiatement

| Sévérité | Problème | Impact | Fix |
|----------|----------|--------|-----|
| 🔴 **CRITIQUE** | Aucun test automatisé | Régressions silencieuses | Créer `tests/` avec pytest |
| 🔴 **CRITIQUE** | Erreurs de typage Claude API | Crash runtime possible | Corriger les types Anthropic |
| 🟠 **MAJEUR** | Code dupliqué (validate.py ↔ storykit.py) | Maintenance difficile | Centraliser dans `validators.py` |
| 🟠 **MAJEUR** | Pas de CI/CD | Risque déploiement | Ajouter GitHub Actions |
| 🟡 **MINEUR** | Pas d'`__init__.py` dans adapters | Import fragile | Créer le fichier |

---

## 9. Roadmap Recommandée

### Priorité 1 (Immédiate — 1-2 jours)
- [ ] Corriger erreurs de typage claude.py
- [ ] Centraliser validations → `cli/validators.py`
- [ ] Ajouter `cli/adapters/__init__.py`
- [ ] Ajouter `out/` à `.gitignore`

### Priorité 2 (Court terme — 1 semaine)
- [ ] Créer suite de tests minimale (`tests/`)
- [ ] Mettre en place GitHub Actions (lint + tests)
- [ ] Ajouter logging structuré
- [ ] Créer CONTRIBUTING.md

### Priorité 3 (Moyen terme — 2 semaines)
- [ ] Type hints complets (cli/*.py)
- [ ] Documentation API (Sphinx ou mkdocs)
- [ ] Cache local de prompts
- [ ] Telemetrie/monitoring (coûts API)

---

## 10. Conclusion

**Verdict :** 🟡 **Projet bien structuré, mais fragile sans tests**

### Résumé des forces
✅ Architecture propre et modulaire  
✅ Documentation exceptionnelle  
✅ Gestion robuste des dépendances optionnelles  
✅ Prompt Caching innovant (économies réelles)  
✅ Séparation CLI/API claire  

### Résumé des faiblesses
❌ **Aucun test automatisé** ← CRITIQUE  
❌ Erreurs de typage (Claude API)  
❌ Code dupliqué  
❌ Pas de CI/CD  
⚠️ Logging insuffisant  

### Recommendation finale

**Le projet est **production-ready** pour usage personnel/équipe réduite**, mais **à risque pour collaboration large ou déploiement institutionnel**. 

Les corrections immédiatement nécessaires sont principalement les tests et la CI/CD. Une fois en place, le projet sera robuste et maintenable à long terme.

---

**Signé :** Audit automatisé  
**Date :** 18/01/2026
