"""
Adaptateur Claude (Anthropic API)
Installer : pip install anthropic
Config : ajouter ANTHROPIC_API_KEY dans .env ou variable d'environnement
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
        """
        model = meta.get("model") or "claude-3-5-sonnet-20241022"
        max_tokens = meta.get("max_tokens", 4096)

        try:
            response = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": payload}]
            )
            
            # Extraire le texte de la réponse
            content = response.content[0].text if response.content else ""
            
            # Sauvegarder la réponse
            self._save_response(content, meta)
            
            return f"[claude] Réponse reçue ({len(content)} caractères) — sauvegardée dans out/responses/"
            
        except anthropic.APIError as e:
            return f"[claude] Erreur API: {e}"
        except Exception as e:
            return f"[claude] Erreur inattendue: {e}"

    def _save_response(self, content: str, meta: dict):
        """Sauvegarde la réponse dans out/responses/"""
        out_dir = Path(__file__).resolve().parents[2] / "out" / "responses"
        out_dir.mkdir(parents=True, exist_ok=True)
        
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        target = meta.get("target", "prompt")
        fname = out_dir / f"{ts}_{target}_response.md"
        
        fname.write_text(content, encoding="utf-8")
