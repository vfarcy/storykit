"""
Adaptateur Claude (Anthropic API)
Installer : pip install anthropic
Config : ajouter ANTHROPIC_API_KEY dans .env ou variable d'environnement

Prompt Caching activé par défaut pour réduire les coûts :
- Les blocs de contexte (artefacts Truby, beats, style) sont mis en cache
- Cache valide ~5 min, réduction ~90% du coût sur tokens cachés
- Désactiver via meta["use_cache"] = False si besoin
"""
import os
from datetime import datetime
from pathlib import Path

try:
    import anthropic
except ImportError:
    anthropic = None


class ClaudeAdapter:
    def __init__(self):
        if anthropic is None:
            raise ImportError(
                "Le module 'anthropic' n'est pas installé. "
                "Installez-le avec: pip install anthropic"
            )
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY manquante. "
                "Définissez-la dans .env ou comme variable d'environnement."
            )
        self.client = anthropic.Anthropic(api_key=api_key)

    def send(self, payload: str, meta: dict) -> str:
        """
        Envoie le prompt à Claude et retourne la réponse.
        Sauvegarde aussi la réponse dans out/responses/.
        
        Utilise Prompt Caching par défaut pour réduire les coûts :
        - Sépare le contexte (cachable) de la requête (variable)
        - Marqueurs cache_control sur les blocs de contexte
        """
        model = meta.get("model") or "claude-3-5-sonnet-20241022"
        max_tokens = meta.get("max_tokens", 4096)
        use_cache = meta.get("use_cache", True)  # Activé par défaut

        try:
            # Construire les messages avec ou sans cache
            if use_cache:
                system_text, user_message = self._build_cached_messages(payload)
                
                # Si pas assez de contenu pour le cache, fallback sans cache
                if not system_text:
                    response = self.client.messages.create(
                        model=model,
                        max_tokens=max_tokens,
                        messages=[{"role": "user", "content": user_message}]
                    )
                else:
                    # Cache activé : utiliser system avec cache_control
                    response = self.client.messages.create(
                        model=model,
                        max_tokens=max_tokens,
                        system=[
                            {
                                "type": "text",
                                "text": system_text,
                                "cache_control": {"type": "ephemeral"}
                            }
                        ],
                        messages=[{"role": "user", "content": user_message}]
                    )
            else:
                response = self.client.messages.create(
                    model=model,
                    max_tokens=max_tokens,
                    messages=[{"role": "user", "content": payload}]
                )
            
            # Extraire le texte de la réponse (filtrer les blocs non-texte)
            content = self._extract_text(response.content)
            
            # Info détaillée sur l'utilisation des tokens
            usage = response.usage
            input_tokens = getattr(usage, 'input_tokens', 0) or 0
            output_tokens = getattr(usage, 'output_tokens', 0) or 0
            cache_creation = getattr(usage, 'cache_creation_input_tokens', 0) or 0
            cache_read = getattr(usage, 'cache_read_input_tokens', 0) or 0
            
            # Construire le message d'info
            token_info = f"Input: {input_tokens:,} | Output: {output_tokens:,}"
            
            cache_info = ""
            if cache_creation:
                cache_info = f" | Cache: {cache_creation:,} créés, {cache_read:,} lus"
            elif cache_read:
                cache_info = f" | Cache: {cache_read:,} lus"
            elif use_cache:
                cache_info = f" | Cache: inactif (< 1024 tok)"
            
            total_cost_tokens = input_tokens + output_tokens + (cache_creation // 10) + (cache_read // 10)
            
            # Sauvegarder la réponse
            self._save_response(content, meta)
            
            return f"[claude] Réponse reçue ({len(content)} caractères) — {token_info}{cache_info} — Total ~{total_cost_tokens:,} tokens"
            
        except Exception as e:
            # Capte anthropic.APIError et autres exceptions
            error_type = type(e).__name__
            return f"[claude] Erreur ({error_type}): {e}"
    
    def _build_cached_messages(self, payload: str):
        """
        Sépare le prompt en contexte (cachable) et requête (variable).
        
        Retourne (system_text: str, user_message: str)
        - system_text : contexte à mettre en cache (peut être vide si trop court)
        - user_message : instructions finales
        """
        # Chercher la section "INSTRUCTIONS" ou similaire qui marque la fin du contexte
        instructions_markers = [
            "# INSTRUCTIONS",
            "# Instructions",
            "# TÂCHE",
            "# Tâche", 
            "# MISSION",
            "# Mission"
        ]
        
        split_pos = -1
        for marker in instructions_markers:
            pos = payload.rfind(marker)
            if pos != -1:
                split_pos = pos
                break
        
        if split_pos == -1:
            # Pas de séparation claire, mettre tout le contexte en cache sauf les 2 derniers paragraphes
            paragraphs = payload.split('\n\n')
            if len(paragraphs) < 3:
                return "", payload  # Trop court pour le cache
            
            context = '\n\n'.join(paragraphs[:-2])
            request = '\n\n'.join(paragraphs[-2:])
        else:
            # Séparer au niveau du marker d'instructions
            context = payload[:split_pos].strip()
            request = payload[split_pos:].strip()
        
        return context, request
    
    def _extract_text(self, content_blocks):
        """
        Extrait le texte des blocs de contenu, en ignorant les blocs non-texte
        (ThinkingBlock, ToolUseBlock, etc.).
        """
        if not content_blocks:
            return ""
        
        text_parts = []
        for block in content_blocks:
            # Vérifier si le bloc a un attribut 'text'
            if hasattr(block, 'text'):
                text_parts.append(block.text)
        
        return "".join(text_parts)
    
    def _split_prompt(self, payload: str):
        """
        Divise le prompt en sections logiques pour optimiser le cache.
        
        Cherche des marqueurs comme :
        - "---" (séparateur Markdown)
        - Titres de niveau 1 (# Titre)
        - Sections identifiables (Prémisse, Style, Artefacts, etc.)
        """
        sections = []
        current = []
        
        for line in payload.split('\n'):
            # Détecter les séparateurs
            if line.strip() in ['---', '═══']:
                if current:
                    sections.append('\n'.join(current))
                    current = []
            # Détecter les titres de niveau 1 (sauf le premier)
            elif line.startswith('# ') and sections:
                if current:
                    sections.append('\n'.join(current))
                    current = [line]
            else:
                current.append(line)
        
        # Ajouter la dernière section
        if current:
            sections.append('\n'.join(current))
        
        return sections if sections else [payload]

    def _save_response(self, content: str, meta: dict):
        """Sauvegarde la réponse dans out/responses/ du livre en cours"""
        # Utiliser le chemin fourni par meta, ou fallback au repo root
        out_base = meta.get("out_dir") or str(Path(__file__).resolve().parents[2] / "out" / "prompts")
        out_dir = Path(out_base).parent.parent / "responses"  # passer de prompts/ à responses/
        out_dir.mkdir(parents=True, exist_ok=True)
        
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        target = meta.get("target", "prompt")
        fname = out_dir / f"{ts}_{target}_response.md"
        
        fname.write_text(content, encoding="utf-8")
    
    # ========== BATCH PROCESSING ==========
    
    def create_batch(self, requests: list) -> dict:
        """
        Crée un batch job avec plusieurs requêtes.
        
        Args:
            requests: Liste de dicts avec format:
                {
                    "custom_id": str,
                    "params": {
                        "model": str,
                        "max_tokens": int,
                        "messages": list,
                        "system": str (optionnel)
                    }
                }
        
        Returns:
            dict avec batch_id, status, etc.
        """
        if len(requests) > 100000:
            raise ValueError("Maximum 100,000 requests per batch")
        
        try:
            batch = self.client.messages.batches.create(requests=requests)
            
            return {
                "batch_id": batch.id,
                "status": batch.processing_status,
                "created_at": batch.created_at,
                "expires_at": batch.expires_at,
                "request_count": len(requests)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_batch_status(self, batch_id: str) -> dict:
        """
        Récupère le statut d'un batch.
        
        Returns:
            dict avec status, progress, etc.
        """
        try:
            batch = self.client.messages.batches.retrieve(batch_id)
            
            counts = batch.request_counts
            total = (counts.processing + counts.succeeded + 
                    counts.errored + counts.canceled + counts.expired)
            
            result = {
                "batch_id": batch.id,
                "status": batch.processing_status,
                "progress": {
                    "total": total,
                    "succeeded": counts.succeeded,
                    "processing": counts.processing,
                    "errored": counts.errored,
                    "canceled": counts.canceled,
                    "expired": counts.expired
                },
                "created_at": batch.created_at,
                "expires_at": batch.expires_at
            }
            
            if batch.processing_status == "ended":
                result["results_url"] = batch.results_url
                result["ended_at"] = batch.ended_at
            
            return result
        except Exception as e:
            return {"error": str(e)}
    
    def download_batch_results(self, batch_id: str) -> list:
        """
        Télécharge les résultats d'un batch terminé.
        
        Returns:
            Liste de dicts avec custom_id et résultats
        """
        try:
            batch = self.client.messages.batches.retrieve(batch_id)
            
            if batch.processing_status != "ended":
                return {"error": f"Batch not ended yet (status: {batch.processing_status})"}
            
            results = []
            for result in self.client.messages.batches.results(batch_id):
                item = {
                    "custom_id": result.custom_id,
                    "result_type": result.result.type
                }
                
                if result.result.type == "succeeded":
                    item["content"] = self._extract_text(result.result.message.content)
                    item["usage"] = {
                        "input_tokens": result.result.message.usage.input_tokens,
                        "output_tokens": result.result.message.usage.output_tokens
                    }
                elif result.result.type == "errored":
                    item["error"] = {
                        "type": result.result.error.type,
                        "message": result.result.error.message
                    }
                
                results.append(item)
            
            return results
        except Exception as e:
            return {"error": str(e)}
