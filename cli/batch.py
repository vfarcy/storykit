#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
StoryKit Batch CLI — Batch processing pour Claude API
------------------------------------------------------

Génération en masse avec réduction de coût de 50% via Message Batches API.
À partir de janvier 2026, les batchs sont automatiquement scopés par livre (via storykit.config.yaml).

Commandes disponibles :

1) draft-variants : Générer plusieurs variations stylistiques d'un chapitre
   Exemple (depuis livre1-truby) :
     python -m cli.batch draft-variants \
       --chapter story/drafting/LeSilenceDesAlgorithmes/20260118_213305_draft_response.md \
       --styles "mélancolique,brutal,poétique,minimaliste" \
       --wait
   Sortie : livre1-truby/story/drafting/LeSilenceDesAlgorithmes/

2) research : Générer du contenu de recherche en masse
   Exemple :
     python -m cli.batch research \
       --topic "IA et littérature" \
       --subtopics "histoire,éthique,créativité,prix_littéraires" \
       --count 5
   Sortie : livre1-truby/story/research/

3) status : Vérifier le statut d'un batch
   Exemple :
     python -m cli.batch status --batch-id msgbatch_abc123

4) download : Télécharger les résultats d'un batch
   Exemple :
     python -m cli.batch download --batch-id msgbatch_abc123

Nécessite : anthropic (pip install anthropic)
"""

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path
# Charger .env explicitement
try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / '.env')
except ImportError:
    pass

try:
    import yaml
except ImportError:
    yaml = None

try:
    from cli.adapters.claude import ClaudeAdapter
except ImportError:
    print("Erreur : Impossible d'importer ClaudeAdapter")
    sys.exit(1)


def find_book_roots(project_root: Path) -> list[Path]:
    """Retourne les répertoires contenant storykit.config.yaml."""
    return sorted({p.parent for p in project_root.rglob("storykit.config.yaml")})


def get_current_book(
    project_root: Path,
    chapter_path: Path | None = None,
    book_roots: list[Path] | None = None
) -> Path | None:
    """
    Détecte le livre courant en cherchant storykit.config.yaml.
    Ordre de priorité :
      1) Chemin du chapitre (si fourni)
      2) CWD et ses parents
      3) Sous-dossiers du projet
    """
    book_roots = book_roots or find_book_roots(project_root)

    # 1) Depuis le chemin du chapitre
    if chapter_path:
        chapter_path = Path(chapter_path) if not isinstance(chapter_path, Path) else chapter_path
        current = chapter_path if chapter_path.is_absolute() else Path.cwd() / chapter_path
        current = current.parent if current.is_file() else current
        for parent in [current] + list(current.parents):
            if (parent / "storykit.config.yaml").exists():
                return parent

        # Essayer de mapper le chemin relatif sur chaque livre connu
        if not chapter_path.is_absolute():
            for book in book_roots:
                alt = book / chapter_path
                if alt.exists():
                    return book

    # 2) Depuis le CWD (utile quand on se place dans le livre)
    cwd = Path.cwd()
    for parent in [cwd] + list(cwd.parents):
        if (parent / "storykit.config.yaml").exists():
            return parent

    # 3) Parcours des sous-dossiers du repo (fallback)
    for book in book_roots:
        return book

    return None


class BatchService:
    """Service pour orchestrer les opérations batch"""
    
    def __init__(self, project_root: Path, chapter_path: Path | None = None):
        self.project_root = project_root
        self.adapter = ClaudeAdapter()
        self.book_roots = find_book_roots(project_root)
        
        # Détecte le livre courant et scopes les outputs au livre
        initial_book = get_current_book(project_root, chapter_path, self.book_roots)
        if initial_book:
            self._set_book(initial_book)
        elif self.book_roots:
            self._set_book(self.book_roots[0])
            print(f"⚠️ Aucun livre détecté, fallback vers {self.current_book.name}")
        else:
            # Fallback global si pas de livre détecté (pour compatibilité)
            self.current_book = None
            self.batch_dir = project_root / "story" / "drafting" / "batches"
            self.research_dir = project_root / "story" / "research"
            self.drafting_base = project_root / "story" / "drafting"
            self.batch_dir.mkdir(exist_ok=True, parents=True)
            self.research_dir.mkdir(exist_ok=True, parents=True)

    def _set_book(self, book_root: Path):
        self.current_book = book_root
        self.batch_dir = book_root / "story" / "drafting" / "batches"
        self.research_dir = book_root / "story" / "research"
        self.drafting_base = book_root / "story" / "drafting"
        self.batch_dir.mkdir(exist_ok=True, parents=True)
        self.research_dir.mkdir(exist_ok=True, parents=True)
    
    def draft_variants(
        self,
        chapter_path: Path,
        styles: list,
        wait: bool = False,
        system_context: str = None
    ) -> str:
        """
        Générer plusieurs variations stylistiques d'un chapitre.
        
        Args:
            chapter_path: Chemin vers le fichier du chapitre
            styles: Liste des tonalités (ex: ["mélancolique", "brutal"])
            wait: Attendre la fin du batch
            system_context: Contexte système (optionnel)
        
        Returns:
            batch_id
        """
        # Résoudre le chemin du chapitre
        chapter_path = Path(chapter_path) if not isinstance(chapter_path, Path) else chapter_path
        
        # Si le fichier n'existe pas en absolu, chercher dans les sous-dossiers du projet
        if not chapter_path.is_absolute():
            # Essayer le chemin absolu depuis le CWD d'abord
            abs_path = Path.cwd() / chapter_path
            if abs_path.exists():
                chapter_path = abs_path
            else:
                # Chercher dans les sous-dossiers du projet (livre1-truby, livre2-maigretlike, etc.)
                found = False
                for book_root in self.book_roots:
                    alt_path = book_root / chapter_path
                    if alt_path.exists():
                        chapter_path = alt_path
                        self._set_book(book_root)
                        found = True
                        break
        
        print(f"📖 Lecture du chapitre : {chapter_path.name}")
        
        if not chapter_path.exists():
            print(f"❌ Fichier introuvable : {chapter_path}")
            return None
        
        with open(chapter_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Charger le style guide si disponible
        if system_context is None:
            # Cherche d'abord dans le livre courant, sinon dans la racine
            style_file = None
            if self.current_book:
                style_file = self.current_book / "story" / "config" / "style.md"
            if not style_file or not style_file.exists():
                style_file = self.project_root / "story" / "config" / "style.md"
            
            if style_file.exists():
                with open(style_file, 'r', encoding='utf-8') as f:
                    system_context = f.read()
            else:
                system_context = """Tu es un écrivain littéraire français.
Tu maîtrises les styles d'écriture variés tout en gardant une cohérence narrative.
Adapte le rythme, le vocabulaire et la ponctuation selon la tonalité demandée."""
        
        # Charger le genre principal et la philosophie
        genre_file = None
        if self.current_book:
            genre_file = self.current_book / "story" / "genre" / "genre_choice.yaml"
        if not genre_file or not genre_file.exists():
            genre_file = self.project_root / "story" / "genre" / "genre_choice.yaml"
        genre_context = ""
        if genre_file.exists() and yaml:
            with open(genre_file, 'r', encoding='utf-8') as f:
                genre_data = yaml.safe_load(f)
                g = genre_data.get('genre', {})
                genre_context = f"GENRE PRINCIPAL : {g.get('primary','')}.\nBLENDS : {', '.join(g.get('blends', []))}\nPHILOSOPHIE : {g.get('philosophy','')}\nPROMESSE : {g.get('promise','')}\n"

        # Créer les requêtes batch
        requests = []
        chapter_name = chapter_path.stem.replace("_draft_response", "")

        for idx, style in enumerate(styles):
            # Nettoyer le style pour custom_id (ASCII seulement, pas d'accents)
            safe_style = (style
                .replace('é', 'e')
                .replace('è', 'e')
                .replace('ê', 'e')
                .replace('à', 'a')
                .replace('ù', 'u')
                .replace('ô', 'o')
                .replace('î', 'i')
                .replace('ç', 'c')
                .replace(' ', '_')
                .replace(',', '_'))
            
            prompt = f"""{genre_context}
Voici un chapitre de roman littéraire.

CONSIGNE : Réécris ce chapitre avec une tonalité **{style.upper()}**, tout en conservant :
- La structure narrative existante
- Les événements clés et leur enchaînement
- Les lieux et personnages
- La longueur approximative

Modifie uniquement le STYLE, le RYTHME et l'ATMOSPHÈRE pour refléter une écriture {style}.

CHAPITRE ORIGINAL :
{original_content}

NOUVELLE VERSION ({style.upper()}) :
"""
            
            # Charger le modèle depuis la config YAML
            config_file = self.project_root / "story" / "config" / "storykit.config.yaml"
            model_name = "claude-sonnet-4-20250514"
            if config_file.exists() and yaml:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    model_name = config.get('ai', {}).get('model', model_name)
            requests.append({
                "custom_id": f"{chapter_name}_variant_{idx:02d}_{safe_style}",
                "params": {
                    "model": model_name,
                    "max_tokens": 256,  # Limité pour test
                    "temperature": 0.85,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "system": system_context
                }
            })
        
        print(f"🚀 Création du batch avec {len(requests)} variations...")
        result = self.adapter.create_batch(requests)
        
        if "error" in result:
            print(f"❌ Erreur : {result['error']}")
            return None
        
        batch_id = result["batch_id"]
        
        # Sauvegarder metadata
        metadata = {
            "batch_id": batch_id,
            "type": "draft_variants",
            "created_at": datetime.now().isoformat(),
            "chapter_file": str(chapter_path),
            "styles": styles,
            "status": "created",
            "request_count": len(requests)
        }
        if self.current_book:
            metadata["book_root"] = str(self.current_book.relative_to(self.project_root))
            metadata["book_name"] = self.current_book.name
        
        metadata_file = self.batch_dir / f"{batch_id}_metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Batch créé : {batch_id}")
        print(f"📊 {len(requests)} variations demandées : {', '.join(styles)}")
        print(f"⏱️  Temps estimé : 30-60 minutes")
        print(f"💰 Coût : ~50% moins cher qu'en mode normal")
        
        if wait:
            print(f"\n⏳ Attente de la fin du traitement...")
            self.poll_until_complete(batch_id)
            self.download_results(batch_id)
        else:
            print(f"\n💡 Pour vérifier le statut :")
            print(f"   python -m cli.batch status --batch-id {batch_id}")
            print(f"\n💡 Pour télécharger les résultats :")
            print(f"   python -m cli.batch download --batch-id {batch_id}")
        
        return batch_id
    
    def draft_chapters(
        self,
        chapters: list,
        project_name: str,
        wait: bool = False,
        system_context: str = None
    ) -> str:
        """
        Générer plusieurs chapitres différents en batch.
        
        Args:
            chapters: Liste de dicts avec 'number', 'title', 'outline'
            project_name: Nom du projet (ex: "LeSilenceDesAlgorithmes")
            wait: Attendre la fin du batch
            system_context: Contexte système (optionnel)
        
        Returns:
            batch_id
        """
        print(f"📚 Génération de {len(chapters)} chapitres pour : {project_name}")
        
        # Charger le style guide si disponible
        if system_context is None:
            style_file = self.project_root / "story" / "config" / "style.md"
            if style_file.exists():
                with open(style_file, 'r', encoding='utf-8') as f:
                    system_context = f.read()
            else:
                system_context = """Tu es un écrivain littéraire français.
Tu écris des romans contemporains avec une attention particulière au rythme, aux détails sensoriels et à la profondeur psychologique."""
        
        # Charger les artefacts Truby pour contexte enrichi
        truby_context = self._load_truby_context()
        scene_weave = self._load_scene_weave()
        
        # Charger le genre principal et la philosophie
        genre_file = self.project_root / "story" / "genre" / "genre_choice.yaml"
        genre_context = ""
        if genre_file.exists() and yaml:
            with open(genre_file, 'r', encoding='utf-8') as f:
                genre_data = yaml.safe_load(f)
                g = genre_data.get('genre', {})
                genre_context = f"GENRE PRINCIPAL : {g.get('primary','')}.\nBLENDS : {', '.join(g.get('blends', []))}\nPHILOSOPHIE : {g.get('philosophy','')}\nPROMESSE : {g.get('promise','')}\n"

        # Créer les requêtes batch
        requests = []

        for chapter in chapters:
            chapter_num = chapter['number']
            chapter_title = chapter.get('title', f'Chapitre {chapter_num}')
            outline = chapter.get('outline', '')
            scenes = chapter.get('scenes', [])
            
            # Construire le prompt pour ce chapitre
            prompt = f"""{genre_context}
Tu dois écrire le **Chapitre {chapter_num} : {chapter_title}** d'un roman littéraire.

## CONTEXTE DU ROMAN
{truby_context}

## PLAN GÉNÉRAL DES SCÈNES
{scene_weave}

## CHAPITRE {chapter_num} : {chapter_title}

### Synopsis
{outline}

### Scènes à inclure
{chr(10).join(f'- Scène {s["number"]}: {s["description"]}' for s in scenes)}

## CONSIGNES D'ÉCRITURE

1. **Longueur** : 2500-3500 mots
2. **Structure** : Découper en 8-12 sections numérotées (I, II, III...)
3. **Style** : Littéraire contemporain, introspection psychologique
4. **Narration** : Troisième personne, focalisation interne (Léo)
5. **Rythme** : Alterner entre action, dialogue, introspection
6. **Détails** : Sensorialité (lieux, objets, atmosphères)

## TON
- Mélancolie sous-jacente
- Tension dramatique progressive
- Ironie distanciée sur le milieu littéraire

Écris maintenant le chapitre complet.
"""
            
            # Nettoyer le chapter_num pour custom_id
            safe_title = (chapter_title
                .replace(' ', '_')
                .replace("'", '')
                .replace('é', 'e')
                .replace('è', 'e')
                .replace('ê', 'e')
                .replace('à', 'a')
                .replace('ù', 'u')
                .replace('ô', 'o')
                .replace('î', 'i')
                .replace('ç', 'c')[:30])  # Limiter la longueur
            
            # Charger le modèle depuis la config YAML
            config_file = self.project_root / "story" / "config" / "storykit.config.yaml"
            model_name = "claude-sonnet-4-20250514"
            if config_file.exists() and yaml:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    model_name = config.get('ai', {}).get('model', model_name)
            requests.append({
                "custom_id": f"chapter_{chapter_num:02d}_{safe_title}",
                "params": {
                    "model": model_name,
                    "max_tokens": 8000,
                    "temperature": 0.85,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "system": system_context
                }
            })
        
        print(f"🚀 Création du batch avec {len(requests)} chapitres...")
        result = self.adapter.create_batch(requests)
        
        if "error" in result:
            print(f"❌ Erreur : {result['error']}")
            return None
        
        batch_id = result["batch_id"]
        
        # Sauvegarder metadata
        metadata = {
            "batch_id": batch_id,
            "type": "draft_chapters",
            "created_at": datetime.now().isoformat(),
            "project_name": project_name,
            "chapters": [{"number": ch['number'], "title": ch.get('title', '')} for ch in chapters],
            "status": "created",
            "request_count": len(requests)
        }
        if self.current_book:
            metadata["book_root"] = str(self.current_book.relative_to(self.project_root))
            metadata["book_name"] = self.current_book.name
        
        metadata_file = self.batch_dir / f"{batch_id}_metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Batch créé : {batch_id}")
        print(f"📊 {len(requests)} chapitres demandés")
        print(f"⏱️  Temps estimé : 45-90 minutes")
        print(f"💰 Coût estimé : ~${len(requests) * 0.025} (vs ${len(requests) * 0.05} en mode normal)")
        
        if wait:
            print(f"\n⏳ Attente de la fin du traitement...")
            self.poll_until_complete(batch_id)
            self.download_results(batch_id)
        else:
            print(f"\n💡 Pour télécharger les résultats :")
            print(f"   python -m cli.batch download --batch-id {batch_id}")
        
        return batch_id
    
    def _load_truby_context(self) -> str:
        """Charger les artefacts Truby pour enrichir le contexte"""
        truby_dir = self.project_root / "story" / "truby"
        
        context_parts = []
        
        # Prémisse
        premise_file = truby_dir / "premise.md"
        if premise_file.exists():
            with open(premise_file, 'r', encoding='utf-8') as f:
                context_parts.append(f"### Prémisse\n{f.read()}\n")
        
        # Personnages
        char_file = truby_dir / "character_web.yaml"
        if char_file.exists():
            with open(char_file, 'r', encoding='utf-8') as f:
                import yaml
                chars = yaml.safe_load(f)
                if chars and 'characters' in chars:
                    context_parts.append("### Personnages principaux")
                    for char in chars['characters'][:3]:  # Limiter aux 3 premiers
                        context_parts.append(f"- **{char.get('name', 'N/A')}** : {char.get('role', 'N/A')}")
                    context_parts.append("")
        
        return "\n".join(context_parts) if context_parts else "Roman littéraire contemporain."
    
    def _load_scene_weave(self) -> str:
        """Charger le plan des scènes"""
        scene_file = self.project_root / "story" / "outline" / "scene_weave.md"
        if scene_file.exists():
            with open(scene_file, 'r', encoding='utf-8') as f:
                return f.read()
        return ""
    
    def research(
        self,
        topic: str,
        subtopics: list,
        count: int = 5,
        wait: bool = False
    ) -> str:
        """
        Générer du contenu de recherche en masse.
        
        Args:
            topic: Thème principal
            subtopics: Sous-thèmes à explorer
            count: Nombre de variations par sous-thème
            wait: Attendre la fin du batch
        
        Returns:
            batch_id
        """
        print(f"🔬 Génération de recherche sur : {topic}")
        print(f"📚 Sous-thèmes : {', '.join(subtopics)}")
        
        system_context = f"""Tu es un chercheur littéraire et culturel expert.
Tu fournis des analyses détaillées, documentées et nuancées sur le thème : {topic}.
Privilégie les faits, les références historiques et les exemples concrets."""
        
        # Charger le genre principal et la philosophie
        genre_file = self.project_root / "story" / "genre" / "genre_choice.yaml"
        genre_context = ""
        if genre_file.exists() and yaml:
            with open(genre_file, 'r', encoding='utf-8') as f:
                genre_data = yaml.safe_load(f)
                g = genre_data.get('genre', {})
                genre_context = f"GENRE PRINCIPAL : {g.get('primary','')}.\nBLENDS : {', '.join(g.get('blends', []))}\nPHILOSOPHIE : {g.get('philosophy','')}\nPROMESSE : {g.get('promise','')}\n"

        requests = []

        for subtopic in subtopics:
            for i in range(count):
                # Varier les angles d'approche
                angles = [
                    "Histoire et evolution",
                    "Enjeux contemporains",
                    "Exemples marquants",
                    "Perspectives critiques",
                    "Implications creatives"
                ]
                angle = angles[i % len(angles)]
                
                prompt = f"""{genre_context}
Sujet : {topic} — {subtopic}
Angle : {angle}

Rédige une fiche de recherche détaillée (500-800 mots) qui explore cet aspect.

Structure attendue :
1. Contexte et définitions clés
2. Développement avec exemples concrets
3. Enjeux ou tensions identifiés
4. Pistes de réflexion pour un roman

Sois précis, factuel et inspirant pour un écrivain de fiction littéraire."""
                
                # Nettoyer les caractères pour custom_id (ASCII uniquement)
                safe_subtopic = (subtopic
                    .replace('é', 'e')
                    .replace('è', 'e')
                    .replace('ê', 'e')
                    .replace('à', 'a')
                    .replace('ù', 'u')
                    .replace('ô', 'o')
                    .replace('î', 'i')
                    .replace('ç', 'c')
                    .replace(' ', '_')
                    .replace(',', '_'))
                safe_angle = angle.replace(' ', '_')
                
                custom_id = f"research_{safe_subtopic}_{i:02d}_{safe_angle}"
                
                # Charger le modèle depuis la config YAML
                config_file = self.project_root / "story" / "config" / "storykit.config.yaml"
                model_name = "claude-sonnet-4-20250514"
                if config_file.exists() and yaml:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        config = yaml.safe_load(f)
                        model_name = config.get('ai', {}).get('model', model_name)
                requests.append({
                    "custom_id": custom_id,
                    "params": {
                        "model": model_name,
                        "max_tokens": 2048,
                        "temperature": 0.7,
                        "messages": [
                            {"role": "user", "content": prompt}
                        ],
                        "system": system_context
                    }
                })
        
        print(f"🚀 Création du batch avec {len(requests)} fiches de recherche...")
        result = self.adapter.create_batch(requests)
        
        if "error" in result:
            print(f"❌ Erreur : {result['error']}")
            return None
        
        batch_id = result["batch_id"]
        
        # Sauvegarder metadata
        metadata = {
            "batch_id": batch_id,
            "type": "research",
            "created_at": datetime.now().isoformat(),
            "topic": topic,
            "subtopics": subtopics,
            "count_per_subtopic": count,
            "status": "created",
            "request_count": len(requests)
        }
        if self.current_book:
            metadata["book_root"] = str(self.current_book.relative_to(self.project_root))
            metadata["book_name"] = self.current_book.name
        
        metadata_file = self.batch_dir / f"{batch_id}_metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Batch créé : {batch_id}")
        print(f"📊 {len(requests)} fiches demandées")
        print(f"⏱️  Temps estimé : 30-60 minutes")
        
        if wait:
            print(f"\n⏳ Attente de la fin du traitement...")
            self.poll_until_complete(batch_id)
            self.download_results(batch_id)
        else:
            print(f"\n💡 Pour télécharger les résultats :")
            print(f"   python -m cli.batch download --batch-id {batch_id}")
        
        return batch_id
    
    def status(self, batch_id: str):
        """Afficher le statut d'un batch"""
        result = self.adapter.get_batch_status(batch_id)
        
        if "error" in result:
            print(f"❌ Erreur : {result['error']}")
            return
        
        print(f"\n📦 Batch : {batch_id}")
        print(f"📊 Statut : {result['status']}")
        print(f"📅 Créé le : {result['created_at']}")
        print(f"⏰ Expire le : {result['expires_at']}")
        
        progress = result['progress']
        total = progress['total']
        succeeded = progress['succeeded']
        
        print(f"\n🎯 Progression :")
        print(f"   ✅ Réussis : {succeeded}/{total}")
        print(f"   ⏳ En cours : {progress['processing']}")
        print(f"   ❌ Erreurs : {progress['errored']}")
        print(f"   ⚠️  Annulés : {progress['canceled']}")
        print(f"   ⏱️  Expirés : {progress['expired']}")
        
        if result['status'] == 'ended':
            print(f"\n✅ Batch terminé !")
            print(f"   Terminé le : {result.get('ended_at', 'N/A')}")
            print(f"\n💡 Télécharger les résultats :")
            print(f"   batch download --batch-id {batch_id}")
    
    def list_batches(self, limit: int = 10):
        """Lister tous les batchs récents"""
        print(f"📋 Liste des {limit} derniers batchs\n")
        
        try:
            batches = list(self.adapter.client.messages.batches.list(limit=limit))
            
            if not batches:
                print("Aucun batch trouvé.")
                return
            
            for batch in batches:
                # Charger metadata si disponible
                metadata_file = self._find_metadata_file(batch.id)
                batch_type = "unknown"
                description = ""
                downloaded = False
                saved_count = 0
                
                if metadata_file and metadata_file.exists():
                    with open(metadata_file, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                        batch_type = metadata.get('type', 'unknown')
                        
                        # Vérifier si téléchargé
                        if 'saved_files' in metadata:
                            downloaded = True
                            saved_count = metadata.get('saved_files', 0)
                        
                        if batch_type == 'draft_variants':
                            styles = metadata.get('styles', [])
                            description = f"Variations: {', '.join(styles[:3])}"
                        elif batch_type == 'draft_chapters':
                            chapters = metadata.get('chapters', [])
                            ch_nums = [str(ch.get('number', '?')) for ch in chapters]
                            description = f"Chapitres: {', '.join(ch_nums)}"
                        elif batch_type == 'research':
                            topic = metadata.get('topic', 'N/A')
                            description = f"Topic: {topic[:40]}"
                
                # Statut avec emoji
                status_emoji = {
                    'in_progress': '⏳',
                    'ended': '✅',
                    'canceling': '⚠️',
                    'canceled': '❌'
                }.get(batch.processing_status, '❓')
                
                # Calculer progression
                counts = batch.request_counts
                total = (counts.processing + counts.succeeded + 
                        counts.errored + counts.canceled + counts.expired)
                progress_pct = (counts.succeeded / total * 100) if total > 0 else 0
                
                print(f"{status_emoji} {batch.id}")
                print(f"   Type: {batch_type}")
                if description:
                    print(f"   {description}")
                print(f"   Statut: {batch.processing_status} ({progress_pct:.0f}% complété)")
                print(f"   Créé: {batch.created_at}")
                
                # Indicateur de téléchargement
                if downloaded:
                    print(f"   📥 Téléchargé : {saved_count} fichiers")
                elif batch.processing_status == 'ended':
                    print(f"   ⚠️  Non téléchargé")
                
                # Suggestions d'action
                if batch.processing_status == 'in_progress':
                    print(f"   💡 batch status --batch-id {batch.id}")
                elif batch.processing_status == 'ended' and not downloaded:
                    print(f"   💡 batch download --batch-id {batch.id}")
                
                print()
        
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des batchs : {e}")
    
    def poll_until_complete(self, batch_id: str, interval: int = 60):
        """Attendre que le batch soit terminé"""
        while True:
            result = self.adapter.get_batch_status(batch_id)
            
            if "error" in result:
                print(f"❌ Erreur : {result['error']}")
                break
            
            progress = result['progress']
            print(f"   Progress: {progress['succeeded']}/{progress['total']} completed", end='\r')
            
            if result['status'] == 'ended':
                print(f"\n✅ Batch terminé !")
                break
            
            time.sleep(interval)
    
    def _find_metadata_file(self, batch_id: str) -> Path | None:
        candidates = []
        if self.current_book:
            candidates.append(self.batch_dir / f"{batch_id}_metadata.json")
        for book in self.book_roots:
            candidates.append(book / "story" / "drafting" / "batches" / f"{batch_id}_metadata.json")
        candidates.append(self.project_root / "story" / "drafting" / "batches" / f"{batch_id}_metadata.json")

        seen = set()
        for path in candidates:
            if path in seen:
                continue
            seen.add(path)
            if path.exists():
                return path
        return None

    def download_results(self, batch_id: str):
        """Télécharger et sauvegarder les résultats"""
        # Charger metadata
        metadata_file = self._find_metadata_file(batch_id)
        if metadata_file and metadata_file.exists():
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)

            # Recalibrer le livre si possible
            book_root = metadata.get("book_root")
            if book_root:
                candidate = (self.project_root / book_root).resolve()
            else:
                # Métadonnées trouvées dans .../story/drafting/batches/<id>_metadata.json
                candidate = metadata_file.parent.parent.parent
            if candidate.exists():
                self._set_book(candidate)
        else:
            metadata = {"type": "unknown"}
            metadata_file = self.batch_dir / f"{batch_id}_metadata.json"
        
        print(f"\n📥 Téléchargement des résultats...")
        results = self.adapter.download_batch_results(batch_id)
        
        if isinstance(results, dict) and "error" in results:
            print(f"❌ Erreur : {results['error']}")
            return
        
        print(f"📦 {len(results)} résultats récupérés")
        
        # Créer le dossier de résultats
        results_dir = self.batch_dir / f"{batch_id}_results"
        results_dir.mkdir(exist_ok=True)
        
        saved_files = []
        errors = []
        
        for result in results:
            custom_id = result['custom_id']
            
            if result['result_type'] == 'succeeded':
                content = result['content']
                
                # Déterminer le répertoire de destination
                if metadata['type'] == 'draft_variants':
                    # Sauvegarder dans drafting
                    project_name = Path(metadata['chapter_file']).parent.name
                    output_dir = self.drafting_base / project_name
                    output_dir.mkdir(exist_ok=True, parents=True)
                    
                    # Extraire le style du custom_id
                    style = custom_id.split('_')[-1]
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{timestamp}_draft_variant_{style}.md"
                    
                elif metadata['type'] == 'research':
                    # Sauvegarder dans research
                    output_dir = self.research_dir
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{timestamp}_{custom_id}.md"
                
                elif metadata['type'] == 'draft_chapters':
                    # Sauvegarder dans drafting
                    project_name = metadata['project_name']
                    output_dir = self.drafting_base / project_name
                    output_dir.mkdir(exist_ok=True, parents=True)
                    
                    # Extraire le numéro de chapitre du custom_id
                    chapter_num = custom_id.split('_')[1]
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"Chap{chapter_num}_{timestamp}_draft.md"
                    
                else:
                    # Par défaut dans batch_dir
                    output_dir = results_dir
                    filename = f"{custom_id}.md"
                
                filepath = output_dir / filename
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                saved_files.append(filepath)
                print(f"✅ {filename}")
                
            else:
                errors.append({
                    "custom_id": custom_id,
                    "error": result.get('error', 'Unknown error')
                })
                print(f"❌ {custom_id}: {result.get('error', {}).get('message', 'Unknown error')}")
        
        # Résumé
        print(f"\n📊 Résumé :")
        print(f"   ✅ Fichiers sauvegardés : {len(saved_files)}")
        print(f"   ❌ Erreurs : {len(errors)}")
        
        if metadata['type'] == 'draft_variants':
            target_dir = self.drafting_base / Path(metadata['chapter_file']).parent.name
            try:
                print(f"\n📁 Fichiers dans : {target_dir.relative_to(self.project_root)}/")
            except ValueError:
                print(f"\n📁 Fichiers dans : {target_dir}/")
        elif metadata['type'] == 'research':
            try:
                print(f"\n📁 Fichiers dans : {self.research_dir.relative_to(self.project_root)}/")
            except ValueError:
                print(f"\n📁 Fichiers dans : {self.research_dir}/")
        
        # Mettre à jour metadata
        metadata['status'] = 'completed'
        metadata['completed_at'] = datetime.now().isoformat()
        metadata['saved_files'] = len(saved_files)
        metadata['errors'] = len(errors)
        
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(
        description="StoryKit Batch CLI - Batch processing pour Claude API",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commandes disponibles')
    
    # draft-variants
    variants_parser = subparsers.add_parser(
        'draft-variants',
        help='Générer plusieurs variations stylistiques d\'un chapitre'
    )
    variants_parser.add_argument(
        '--chapter',
        required=True,
        help='Chemin vers le fichier du chapitre'
    )
    variants_parser.add_argument(
        '--styles',
        required=True,
        help='Styles séparés par des virgules (ex: "mélancolique,brutal,poétique")'
    )
    variants_parser.add_argument(
        '--wait',
        action='store_true',
        help='Attendre la fin du traitement'
    )
    
    # draft-chapters
    chapters_parser = subparsers.add_parser(
        'draft-chapters',
        help='Générer plusieurs chapitres différents en batch'
    )
    chapters_parser.add_argument(
        '--project',
        required=True,
        help='Nom du projet (ex: LeSilenceDesAlgorithmes)'
    )
    chapters_parser.add_argument(
        '--chapters',
        required=True,
        help='Numéros de chapitres séparés par des virgules (ex: "8,9,10")'
    )
    chapters_parser.add_argument(
        '--wait',
        action='store_true',
        help='Attendre la fin du traitement'
    )
    
    # research
    research_parser = subparsers.add_parser(
        'research',
        help='Générer du contenu de recherche en masse'
    )
    research_parser.add_argument(
        '--topic',
        required=True,
        help='Thème principal'
    )
    research_parser.add_argument(
        '--subtopics',
        required=True,
        help='Sous-thèmes séparés par des virgules'
    )
    research_parser.add_argument(
        '--count',
        type=int,
        default=5,
        help='Nombre de variations par sous-thème (défaut: 5)'
    )
    research_parser.add_argument(
        '--wait',
        action='store_true',
        help='Attendre la fin du traitement'
    )
    
    # status
    status_parser = subparsers.add_parser(
        'status',
        help='Vérifier le statut d\'un batch'
    )
    status_parser.add_argument(
        '--batch-id',
        required=True,
        help='ID du batch'
    )
    
    # download
    download_parser = subparsers.add_parser(
        'download',
        help='Télécharger les résultats d\'un batch'
    )
    download_parser.add_argument(
        '--batch-id',
        required=True,
        help='ID du batch'
    )
    
    # list
    list_parser = subparsers.add_parser(
        'list',
        help='Lister tous les batchs récents'
    )
    list_parser.add_argument(
        '--limit',
        type=int,
        default=10,
        help='Nombre de batchs à afficher (défaut: 10)'
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialiser le service
    project_root = Path(__file__).resolve().parents[1]
    
    # Passer le chapter_path pour une meilleure détection du livre
    chapter_path = None
    if args.command == 'draft-variants' and hasattr(args, 'chapter'):
        chapter_path = Path(args.chapter)
    elif args.command == 'draft-chapters' and hasattr(args, 'chapters'):
        # Pour draft-chapters, on ne peut pas passer UN chapitre, donc pas de path
        chapter_path = None
    
    service = BatchService(project_root, chapter_path)
    
    # Exécuter la commande
    if args.command == 'draft-variants':
        chapter_path = Path(args.chapter)
        styles = [s.strip() for s in args.styles.split(',')]
        service.draft_variants(chapter_path, styles, wait=args.wait)
    
    elif args.command == 'draft-chapters':
        # Charger le scene_weave pour extraire les chapitres
        scene_weave_file = project_root / "story" / "outline" / "scene_weave.md"
        
        if not scene_weave_file.exists():
            print("❌ Fichier scene_weave.md introuvable")
            return
        
        # Parser les numéros demandés
        chapter_nums = [int(n.strip()) for n in args.chapters.split(',')]
        
        # Construire les chapitres à partir du scene_weave
        chapters = []
        for num in chapter_nums:
            # Pour l'instant, structure simple - peut être enrichie
            chapters.append({
                "number": num,
                "title": f"Chapitre {num}",
                "outline": f"Consulter scene_weave.md, scènes liées au chapitre {num}",
                "scenes": []
            })
        
        service.draft_chapters(chapters, args.project, wait=args.wait)
    
    elif args.command == 'research':
        subtopics = [s.strip() for s in args.subtopics.split(',')]
        service.research(args.topic, subtopics, count=args.count, wait=args.wait)
    
    elif args.command == 'status':
        service.status(args.batch_id)
    
    elif args.command == 'download':
        service.download_results(args.batch_id)
    
    elif args.command == 'list':
        service.list_batches(limit=args.limit)


if __name__ == "__main__":
    main()
