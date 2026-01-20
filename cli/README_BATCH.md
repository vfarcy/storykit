# StoryKit Batch CLI 🚀

**Génération en masse avec réduction de coût de 50%** via l'API Message Batches de Claude.

## 📋 Prérequis

```bash
pip install anthropic pyyaml
```

Assurez-vous que votre clé API Claude est configurée dans `.env` :
```
ANTHROPIC_API_KEY=sk-ant-...
```

---

## 🎯 Vue d'ensemble des commandes

| Commande | Objectif | Cas d'usage typique | Coût/chapitre |
|----------|----------|---------------------|---------------|
| **draft-variants** | Variations d'UN même chapitre | Tester différents styles/tonalités | ~$0.025 |
| **draft-chapters** | Générer PLUSIEURS chapitres différents | Écrire Chap 8-15 en une fois | ~$0.025 |
| **research** | Documentation thématique | Alimenter story/research/ | ~$0.015 |
| **list** | Lister tous les batchs | Voir l'historique complet | Gratuit |
| **status** | Vérifier l'avancement | Polling d'un batch en cours | Gratuit |
| **download** | Récupérer les résultats | Télécharger les fichiers générés | Gratuit |

---

## 🎯 Commandes disponibles

### 1. **draft-variants** — Variations stylistiques d'UN chapitre

**Objectif** : Générer plusieurs versions du MÊME chapitre avec des tonalités différentes.

**Usage** : Explorer différentes approches stylistiques avant de choisir la meilleure.

#### Exemple simple
```bash
python -m cli.batch draft-variants \
  --chapter "story/drafting/LeSilenceDesAlgorithmes/20260118_213305_draft_response.md" \
  --styles "mélancolique,brutal,poétique"
```

#### Avec attente automatique
```bash
python -m cli.batch draft-variants \
  --chapter "story/drafting/LeSilenceDesAlgorithmes/20260118_213305_draft_response.md" \
  --styles "mélancolique,brutal,poétique,minimaliste,lyrique" \
  --waitdraft-chapters** — Générer PLUSIEURS chapitres différents

**Objectif** : Générer plusieurs chapitres DISTINCTS en parallèle (ex: Chap8, Chap9, Chap10).

**Usage** : Accélérer l'écriture en générant plusieurs chapitres en une seule commande.

#### Exemple simple
```bash
python -m cli.batch draft-chapters \
  --project "LeSilenceDesAlgorithmes" \
  --chapters "8,9,10"
```

#### Avec attente automatique
```bash
python -m cli.batch draft-chapters \
  --project "LeSilenceDesAlgorithmes" \
  --chapters "8,9,10" \
  --wait
```

**Résultat** : Fichiers générés dans `story/drafting/LeSilenceDesAlgorithmes/`
- `Chap08_20260120_174500_draft.md`
- `Chap09_20260120_174501_draft.md`
- `Chap10_20260120_174502_draft.md`

#### Générer TOUS les chapitres manquants
```bash
python -m cli.batch draft-chapters \
  --project "LeSilenceDesAlgorithmes" \
  --chapters "1,2,3,4,5,6,7,8,9,10"
```

**Ce qui est automatiquement chargé** :
- ✅ `story/truby/premise.md` — Prémisse du roman
- ✅ `story/truby/character_web.yaml` — Personnages principaux
- ✅ `story/outline/scene_weave.md` — Plan des scènes
- ✅ `story/config/style.md` — Guide de style

**Coût estimé** :
- Coût estimé** :
- 20 fiches de recherche : **~$0.15** (vs $0.30 en mode normal)

---

### 4

### 3. **research** — Génération de contenu de recherche

**Objectif** : Alimenter `story/research/` avec du contenu documentaire thématique.

**Usage** : Construire du background solide avant l'écriture (worldbuilding, contextes historiques, psychologie des personnages)
**Résultat** : Fichiers générés dans `story/drafting/LeSilenceDesAlgorithmes/`
- `20260120_143022_draft_variant_mélancolique.md`
- `20260120_143023_draft_variant_brutal.md`
- etc.

**Coût estimé** :
- Mode normal (5 variations) : ~$0.15
- Mode batch : **~$0.075** (50% moins cher)

---

### 2. **research** — Génération de contenu de recherche

Alimenter votre dossier `story/research/` avec du contenu documentaire.

####5Exemple : Recherche sur un thème
```bash
python -m cli.batch research \
  --topic "Intelligence artificielle et littérature" \
  --subtopics "histoire,éthique,créativité,prix_littéraires" \
  --count 5
```

**Résultat** : 20 fiches de recherche générées (4 sous-thèmes × 5 variations)
- `20260120_150000_research_histoire_00_Histoire_et_évolution.md`
- `20260120_150001_research_histoire_01_Enjeux_contemporains.md`
- etc.

#### Exemple : Recherche pour personnage
```bash
python -m cli.batch research \
  --topic "Syndrome de l'imposteur dans le milieu littéraire" \
  --subtopics "psychologie,témoignages,manifestations,dépassement" \
  --count 3 \
  --wait
```

**Usage** : Parfait pour construire du background solide avant l'écriture.

---

### 4. **list** — Lister tous les batchs

**Objectif** : Voir l'historique complet de tous vos batchs (en cours, terminés, annulés).

**Usage** : Retrouver rapidement un batch précédent ou vérifier tous les jobs en cours.

#### Exemple basique
```bash
python -m cli.batch list
```

#### Limiter l'affichage
```bash
python -m cli.batch list --limit 20
```

**Affichage** :
```
📋 Liste des 10 derniers batchs

✅ msgbatch_016Rx96kiN2QqVme4LqfNAMy
   Type: draft_variants
   Variations: mélancolique, brutal, poétique
   Statut: ended (100% complété)
   Créé: 2026-01-20 17:34:44
   💡 python -m cli.batch download --batch-id msgbatch_016Rx96kiN2QqVme4LqfNAMy

⏳ msgbatch_015AbcXYZ123456789
   Type: draft_chapters
   Chapitres: 8, 9, 10
   Statut: in_progress (33% complété)
   Créé: 2026-01-20 16:00:00
   💡 python -m cli.batch status --batch-id msgbatch_015AbcXYZ123456789
```

**Avantages** :
- ✅ Vue d'ensemble de tous vos batchs
- ✅ Statut en un coup d'œil (⏳ en cours, ✅ terminé, ❌ erreur)
- ✅ Suggestions de commandes contextuelles
- ✅ Chargement automatique des metadata pour détails enrichis

---

### 5. **status** — Vérifier l'avancement d'un batch

```bash
python -m cli.batch status --batch-id msgbatch_01ABC123
```

**Affichage** :
```
📦 Batch : msgbatch_01ABC123
📊 Statut : in_progress
📅 Créé le : 2026-01-20T14:30:00Z
⏰ Expire le : 2026-01-21T14:30:00Z

🎯 Progression :
   ✅ Réussis : 12/20
   ⏳ En cours : 8
   ❌ Erreurs : 0
   ⚠️  Annulés : 0
   ⏱️  Expirés : 0
```

---

### 6. **download** — Télécharger les résultats

```bash
python -m cli.batch download --batch-id msgbatch_01ABC123
```

**Résultat** :
```
📥 Téléchargement des résultats...
📦 20 résultats récupérés
✅ 20260120_150000_research_histoire_00.md
✅ 20260120_150001_research_histoire_01.md
...
📊 Résumé :
   ✅ Fichiers sauvegardés : 20
   ❌ Erreurs : 0

📁 Fichiers dans : story/research/
```

---

## 📖 Cas d'usage typiques
 existant

**Problème** : Vous avez écrit le Chapitre 10, mais hésitez sur le style.

**Solution** : `draft-variants`
```bash
python -m cli.batch draft-variants \
  --chapter "story/drafting/LeSilenceDesAlgorithmes/20260118_213305_draft_response.md" \
  --styles "mélancolique,minimaliste,lyrique,brutal,contemplatif" \
  --wait
```

**Résultat** : 5 versions complètes à comparer, **pour moitié prix**.

---

### Cas 2 : Écrire plusieurs chapitres d'un coup

**Problème** : Vous avez les chapitres 1-7, vous voulez générer 8-10 en une seule fois.

**Solution** : `draft-chapters`
```bash
python -m cli.batch draft-chapters \
  --project "LeSilenceDesAlgorithmes" \
  --chapters "8,9,10" \
  --wait
```

**Résultat** : 3 chapitres complets (différents) générés en parallèle.

**Avantage clé** : Les 3 chapitres partagent automatiquement :
- Le contexte Truby (prémisse, personnages)
- Le plan narratif (scene_weave.md)
- Le guide de style (style.md)

→ **Cohérence narrative garantie**

---

### Cas 3 : Recherche documentaire massive

**Problème** : Vous voulez documenter l'univers startup/tech parisien pour votre worldbuilding.

**Solution** : `research`
```bash
python -m cli.batch research \
  --topic "Écosystème startup parisien 2020-2025" \
  --subtopics "incubateurs,financement,échecs_célèbres,culture_travail,IA_générative" \
  --count 10
```

**Résultat** : 50 fiches (5 sous-thèmes × 10 variations) dans `story/research/`.

---

### Cas 4 : Premier draft complet du roman

**Problème** : Vous avez terminé votre plan Truby, vous voulez un premier draft complet RAPIDEMENT.

**Solution** : `draft-chapters` avec tous les chapitres
```bash
python -m cli.batch draft-chapters \
  --project "LeSilenceDesAlgorithmes" \
  --chapters "1,2,3,4,5,6,7,8,9,10"
```

**Résultat** : 10 chapitres complets en ~90 minutes pour **$0.25** (vs $0.50 en mode normal).
 & Économies

### Batch vs Mode normal

| Action | Mode normal | Mode batch | Économie |
|--------|-------------|------------|----------|
| 1 chapitre (3k tokens) | $0.03 | $0.015 | 50% |
| 5 variations (draft-variants) | $0.15 | **$0.075** | 50% |
| 3 chapitres (draft-chapters) | $0.15 | **$0.075** | 50% |
| 10 chapitres complets | $0.50 | **$0.25** | 50% |
| 20 fiches recherche | $0.30 | **$0.15** | 50% |
| Roman complet (10 ch) | $0.50 | **$0.25** | 50% |

### Scénarios réalistes

**Scénario 1 : Premier draft complet (10 chapitres)**
- Mode normal : 10 × $0.05 = **$0.50**
- Mode batch : **$0.25** ⚡ Économie : $0.25

**Scénario 2 : Raffinement de 3 chapitres (5 variations chacun)**
- Mode normal : 3 × 5 × $0.03 = **$0.45**
- Mode batch : **$0.225** ⚡ Économie : $0.225

**Scénario 3 : Workflow complet (recherche + draft + raffinement)**
- Recherche : 40 fiches → $0.30 → **$0.15** en batch
- Draft : 10 chapitres → $0.50 → **$0.25** en batch
- Raffinement : 3 × 3 variations → $0.27 → **$0.135** en batch
- **Total : $0.535** (vs $1.07 en mode normal)

### Compatibilité avec Prompt Caching

Si vos requêtes partagent le même `system_context`, le cache peut être utilisé :
- Cache hit : 90% de réduction sur les tokens cachés
- **Réductions cumulées** : batch (50%) + cache (90%) = **jusqu'à 95% d'économie**

**Exemple avec cache** :
```bash
# 10 chapitres avec contexte Truby identique
python -m cli.batch draft-chapters --chapters "1,2,3,4,5,6,7,8,9,10"

# Coût avec cache hit (30-98% selon timing) :
# - Sans cache : $0.25
# - Avec cache 70% : ~$0.10
# - Avec cache 90% : ~$0.05
```
```

---

## 🎨 Styles disponibles (exemples)

Tonalités littéraires :
- `mélancolique` — Atmosphère nostalgique, rythme lent
- `brutal` — Direct, cru, économie de mots
- `poétique` — Métaphores, images fortes
- `minimaliste` — Épuré, silences signifiants
- `lyrique` — Flux de conscience, introspection
- `ironique` — Distance, second degré
- `contemplatif` — Observations, réflexions
- `sombre` — Tension, inquiétude
- `lumineux` — Espoir, ouverture

**Astuce** : Combinez-les avec des nuances :
```bash
--styles "mélancolique_et_poétique,brutal_et_ironique,contemplatif_et_lumineux"
```

---

## 💰 Tarification

### Batch vs Mode normal
s recommandés

### Workflow A : Premier draft complet du roman (méthode rapide)

**Objectif** : Obtenir un premier jet complet en 48h pour valider la structure.

#### Jour 1 : Phase de recherche
```bash
# MatiDifférences clés entre les commandes

### draft-variants vs draft-chapters

| Critère | draft-variants | draft-chapters |
|---------|----------------|----------------|
| **Input** | 1 fichier existant | Numéros de chapitres |
| **Output** | N versions du même chapitre | N chapitres différents |
| **Usage** | Exploration stylistique | Génération de contenu nouveau |
| **Contexte** | Chapitre original | Truby + scene_weave |
| **Exemple** | Chap10 en 5 styles | Chap8, 9, 10 d'un coup |

### Quand utiliser quoi ?

**Utilisez `draft-variants` si** :
- ✅ Vous avez déjà un chapitre écrit
- ✅ Vous hésitez sur le style/tonalité
- ✅ Vous voulez comparer plusieurs approches
- ✅ Vous affinez un chapitre clé (début, midpoint, fin)

**Utilisez `draft-chapters` si** :
- ✅ Vous partez de zéro sur plusieurs chapitres
- ✅ Vous voulez un premier draft rapide
- ✅ Vous avez un plan clair (scene_weave.md)
- ✅ Vous voulez garantir la cohérence narrative

**Utilisez `research` si** :
- ✅ Vous construisez votre worldbuilding
- ✅ Vous avez besoin de documentation thématique
- ✅ Vous explorez des sujets connexes au roman

---

## 📊 Metadata et traçabilité

Chaque batch génère un fichier `{batch_id}_metadata.json` dans `story/drafting/batches/` :

```json
{
  "batch_id": "msgbatch_01ABC123",
  "type": "draft_chapters",
  "created_at": "2026-01-20T14:30:00",
  "project_name": "LeSilenceDesAlgorithmes",
  "chapters": [
    {"number": 8, "title": "Chapitre 8"},
    {"number": 9, "title": "Chapitre 9"},
    {"number": 10, "title": "Chapitre 10"}
  ],
  "status": "completed",
  "request_count": 3,
  "saved_files": 3,
  "errors": 0,
  "🎯 Stratégies d'utilisation optimale

### Stratégie 1 : Vitesse maximale (pour MVP/premier draft)
```bash
# Jour 1 : Tout en batch
python -m cli.batch draft-chapters --chapters "1,2,3,4,5,6,7,8,9,10" --wait
```
**Résultat** : Roman complet en 90 minutes

---

### Stratégie 2 : Qualité maximale (itératif)
```bash
# Semaine 1 : Draft initial
python -m cli.batch draft-chapters --chapters "1,2,3,4,5,6,7,8,9,10"

# Semaine 2 : Raffinement des chapitres clés
python -m cli.batch draft-variants --chapter Chap01.md --styles "A,B,C"
python -m cli.batch draft-variants --chapter Chap06.md --styles "D,E,F"
python -m cli.batch draft-variants --chapter Chap10.md --styles "G,H,I"
```
**Résultat** : Roman de qualité avec 3 chapitres hyper-affinés

---

### Stratégie 3 : Équilibre (recommandé)
```bash
# Phase 1 : Recherche (1 jour)
python -m cli.batch research --topic "Thème principal" --subtopics "A,B,C,D,E" --count 5

# Phase 2 : Draft (1 jour)
python -m cli.batch draft-chapters --chapters "1,2,3,4,5,6,7,8,9,10"

# Phase 3 : Lecture sélective (2 jours)
# Identifier les 2-3 chapitres à améliorer

# Phase 4 : Raffinement ciblé (1 jour)
python -m cli.batch draft-variants --chapter ChapXX.md --styles "variations"
```
**Résultat** : Roman complet en 5 jours avec qualité contrôlée

---

## 🚀 Prochaines étapes

### Pour démarrer maintenant

**Option A : Voir tous vos batchs**
```bash
python -m cli.batch list
```

**Option B : Tester avec variations stylistiques**
```bash
python -m cli.batch draft-variants \
  --chapter "story/drafting/LeSilenceDesAlgorithmes/20260118_213305_draft_response.md" \
  --styles "mélancolique,brutal,poétique" \
  --wait
```

**Option C : Générer les prochains chapitres**
```bash
python -m cli.batch draft-chapters \
  --project "LeSilenceDesAlgorithmes" \
  --chapters "8,9,10" \
  --wait
```

**Option D : Construire votre documentation**
```bash
python -m cli.batch research \
  --topic "IA et création littéraire" \
  --subtopics "GPT,prix_littéraires,syndrome_imposteur" \
  --count 3
```

---

## 📞 Support

Questions ? Consultez :
- [Documentation Claude Batch API](https://platform.claude.com/docs/en/build-with-claude/batch-processing)
- [TRUBY_GUIDE.md](../TRUBY_GUIDE.md) pour l'approche narrative
- [AUDIT_REPORT.md](../AUDIT_REPORT.md) pour l'architecture du projet

**Nouveautés** :
- ✨ `draft-chapters` : Génération multi-chapitres
- ✨ `draft-variants` : Variations stylistiques
- ✨ `research` : Documentation automatique
- ✨ Intégration automatique du contexte Truby
- ✨ Compatible avec prompt caching (économies cumulées)

### Workflow B : Raffinement stylistique (méthode qualitative)

**Objectif** : Affiner les chapitres clés avec plusieurs variations.

#### Étape 1 : Identifier les chapitres pivots
Chapitres 1, 6, 10 (début, midpoint, révélation finale)

#### Étape 2 : Générer des variations
```bash
# Chapitre 1 (accroche)
python -m cli.batch draft-variants \
  --chapter "story/drafting/LeSilenceDesAlgorithmes/Chap01.md" \
  --styles "mystérieux,ironique,mélancolique"

# Chapitre 6 (midpoint)
python -m cli.batch draft-variants \
  --chapter "story/drafting/LeSilenceDesAlgorithmes/Chap06.md" \
  --styles "brutal,contemplatif,tension_dramatique"

# Chapitre 10 (révélation)
python -m cli.batch draft-variants \
  --chapter "story/drafting/LeSilenceDesAlgorithmes/Chap10.md" \
  --styles "poétique,sombre,libérateur"
```

#### Étape 3 : Comparer et choisir
```bash
# Ouvrir toutes les variations dans VS Code
code story/drafting/LeSilenceDesAlgorithmes/*variant*.md
```

**Résultat** : 3 chapitres × 3 variations = 9 versions à comparer pour choisir la meilleure.

---

### Workflow C : Itération rapide (méthode hybride)

**Objectif** : Premier draft rapide + raffinement des meilleurs passages.

#### Phase 1 : Génération massive (1 jour)
```bash
python -m cli.batch draft-chapters \
  --project "LeSilenceDesAlgorithmes" \
  --chapters "1,2,3,4,5,6,7,8,9,10"
```

#### Phase 2 : Lecture et sélection (2 jours)
- Lire les 10 chapitres
- Identifier les 3 meilleurs et les 3 à retravailler

#### Phase 3 : Variations ciblées (1 jour)
```bash
# Pour les 3 chapitres à retravailler
python -m cli.batch draft-variants \
  --chapter "story/drafting/.../ChapXX.md" \
  --styles "style_A,style_B,style_C"
```

**Résultat** : Roman complet avec mix de chapitres directs + chapitres affiné
## Références stylistiques
Annie Ernaux, Emmanuel Carrère, Virginie Despentes
```

Ce contexte sera automatiquement utilisé dans tous les batchs `draft-variants`.

---

## 🔍 Workflow recommandé

### 1. Exploration (matin)
```bash
# Lancer le batch avant le café
python -m cli.batch draft-variants \
  --chapter "story/drafting/Chap10.md" \
  --styles "mélancolique,brutal,poétique,minimaliste,lyrique"
  
# Batch ID: msgbatch_01ABC123
```

### 2. Travail sur autre chose (30-60 min)

Pendant que le batch tourne, continuez votre écriture sur un autre chapitre.

### 3. Vérification (après 1h)
```bash
python -m cli.batch status --batch-id msgbatch_01ABC123
# → ended ✅
```

### 4. Récupération et comparaison
```bash
python -m cli.batch download --batch-id msgbatch_01ABC123

# Comparer les 5 versions dans VS Code
code story/drafting/LeSilenceDesAlgorithmes/*.md
```

### 5. Choix final

Sélectionnez la meilleure version ou fusionnez des passages de plusieurs variations.

---

## 📊 Metadata et traçabilité

Chaque batch génère un fichier `{batch_id}_metadata.json` dans `story/drafting/batches/` :

```json
{
  "batch_id": "msgbatch_01ABC123",
  "type": "draft_variants",
  "created_at": "2026-01-20T14:30:00",
  "chapter_file": "story/drafting/.../20260118_213305_draft_response.md",
  "styles": ["mélancolique", "brutal", "poétique"],
  "status": "completed",
  "request_count": 3,
  "saved_files": 3,
  "errors": 0,
  "completed_at": "2026-01-20T15:15:00"
}
```

Utile pour retrouver l'historique de vos expérimentations.

---

## ⚠️ Limitations

- **Maximum 100,000 requêtes** par batch
- **Taille max 256 MB** par batch
- **Expiration après 24h** si non terminé
- **Résultats disponibles 29 jours** après création
- **Cache hit non garanti** (30-98% selon votre usage)

---

## 🆘 Dépannage

### Erreur : "Batch not ended yet"
Le batch n'a pas encore terminé. Attendez quelques minutes.

### Erreur : "ANTHROPIC_API_KEY manquante"
Vérifiez votre fichier `.env` à la racine du projet.

### Erreur : "Fichier introuvable"
Utilisez le chemin relatif depuis la racine du projet :
```bash
--chapter "story/drafting/LeSilenceDesAlgorithmes/fichier.md"
```

### Batch expire après 24h
Si votre batch est très volumineux, il peut expirer. Divisez-le en batches plus petits.

---

## 🚀 Prochaines étapes

1. **Testez** avec une petite variation (2-3 styles)
2. **Comparez** les résultats pour valider la qualité
3. **Scalez** pour des générations plus massives
4. **Combinez** avec le prompt caching pour maximiser les économies

---

## 📞 Support

Questions ? Consultez :
- [Documentation Claude Batch API](https://platform.claude.com/docs/en/build-with-claude/batch-processing)
- Fichier `TRUBY_GUIDE.md` pour l'approche narrative
- Fichier `AUDIT_REPORT.md` pour l'architecture du projet

Bon batch ! 🎉
