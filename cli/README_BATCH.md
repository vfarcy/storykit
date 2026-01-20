# StoryKit Batch CLI 🚀

**Génération en masse avec réduction de coût de 50%** via l'API Message Batches de Claude.

## 📋 Prérequis

```bash
pip install anthropic
```

Assurez-vous que votre clé API Claude est configurée dans `.env` :
```
ANTHROPIC_API_KEY=sk-ant-...
```

---

## 🎯 Commandes disponibles

### 1. **draft-variants** — Variations stylistiques de chapitres

Générer plusieurs versions d'un chapitre avec des tonalités différentes.

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
  --wait
```

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

#### Exemple : Recherche sur un thème
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

### 3. **status** — Vérifier l'avancement d'un batch

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

### 4. **download** — Télécharger les résultats

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

### Cas 1 : Tester plusieurs tonalités pour un chapitre

**Problème** : Vous hésitez sur le style à adopter pour le Chapitre 10.

**Solution** :
```bash
python -m cli.batch draft-variants \
  --chapter "story/drafting/LeSilenceDesAlgorithmes/20260118_213305_draft_response.md" \
  --styles "mélancolique,minimaliste,lyrique,brutal,contemplatif" \
  --wait
```

Vous obtenez 5 versions complètes à comparer, **pour moitié prix**.

---

### Cas 2 : Recherche documentaire massive

**Problème** : Vous voulez documenter l'univers startup/tech parisien.

**Solution** :
```bash
python -m cli.batch research \
  --topic "Écosystème startup parisien 2020-2025" \
  --subtopics "incubateurs,financement,échecs_célèbres,culture_travail,IA_générative" \
  --count 10
```

Génère **50 fiches** (5 sous-thèmes × 10 variations) pour alimenter votre worldbuilding.

---

### Cas 3 : Génération de scènes alternatives

**Problème** : Une scène clé ne vous convainc pas, vous voulez explorer d'autres approches.

**Astuce** : Extraire la scène dans un fichier temporaire, puis :
```bash
python -m cli.batch draft-variants \
  --chapter "temp/scene_03_extract.md" \
  --styles "dialogué,descriptif,introspectif,action,symbolique" \
  --wait
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

| Action | Mode normal | Mode batch | Économie |
|--------|-------------|------------|----------|
| 1 chapitre (3k tokens) | $0.03 | $0.015 | 50% |
| 5 variations | $0.15 | **$0.075** | 50% |
| 20 fiches recherche | $0.30 | **$0.15** | 50% |
| 100 requêtes | $3.00 | **$1.50** | 50% |

### Compatibilité avec Prompt Caching

Si vos requêtes partagent le même `system_context`, le cache peut être utilisé :
- Cache hit : 90% de réduction sur les tokens cachés
- **Réductions cumulées** : jusqu'à 95% d'économie totale

---

## ⚙️ Configuration avancée

### Personnaliser le contexte système

Éditez `story/config/style.md` pour définir votre voix d'auteur :

```markdown
# Style Guide

Tu es un écrivain de fiction littéraire française contemporaine.

## Principes stylistiques
- Privilégier le montré au dit
- Dialogues naturalistes
- Descriptions sensorielles
- Pas de jugement moral explicite

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
