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
            
            # Info sur l'utilisation du cache
            usage = response.usage
            cache_info = ""
            cache_creation = getattr(usage, 'cache_creation_input_tokens', 0) or 0
            cache_read = getattr(usage, 'cache_read_input_tokens', 0) or 0
            
            if cache_creation:
                cache_info = f" [Cache: {cache_creation} créés, {cache_read} lus]"
            elif cache_read:
                cache_info = f" [Cache: {cache_read} lus]"
            elif use_cache:
                # Cache était activé mais pas utilisé (contenu trop court)
                cache_info = f" [Cache: inactif (contenu < 1024 tokens)]"
            
            # Sauvegarder la réponse
            self._save_response(content, meta)
            
            return f"[claude] Réponse reçue ({len(content)} caractères){cache_info} — sauvegardée dans out/responses/"
            
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
        """Sauvegarde la réponse dans out/responses/"""
        out_dir = Path(__file__).resolve().parents[2] / "out" / "responses"
        out_dir.mkdir(parents=True, exist_ok=True)
        
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        target = meta.get("target", "prompt")
        fname = out_dir / f"{ts}_{target}_response.md"
        
        fname.write_text(content, encoding="utf-8")
