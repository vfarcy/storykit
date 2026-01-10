"""
Adaptateur OpenAI / GitHub Copilot
Installer : pip install openai
Config : ajouter OPENAI_API_KEY dans .env ou variable d'environnement
"""
import os
from datetime import datetime
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


class CopilotAdapter:
    def __init__(self):
        if OpenAI is None:
            raise ImportError(
                "Le module 'openai' n'est pas installé. "
                "Installez-le avec: pip install openai"
            )
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY manquante. "
                "Définissez-la dans .env ou comme variable d'environnement."
            )
        self.client = OpenAI(api_key=api_key)

    def send(self, payload: str, meta: dict) -> str:
        """
        Envoie le prompt à OpenAI et retourne la réponse.
        Sauvegarde aussi la réponse dans out/responses/.
        """
        model = meta.get("model") or "gpt-4o"
        max_tokens = meta.get("max_tokens", 4096)

        try:
            response = self.client.chat.completions.create(
                model=model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": payload}]
            )
            
            content = response.choices[0].message.content if response.choices else ""
            
            self._save_response(content, meta)
            
            return f"[openai] Réponse reçue ({len(content)} caractères) — sauvegardée dans out/responses/"
            
        except Exception as e:
            return f"[openai] Erreur: {e}"

    def _save_response(self, content: str, meta: dict):
        """Sauvegarde la réponse dans out/responses/"""
        out_dir = Path(__file__).resolve().parents[2] / "out" / "responses"
        out_dir.mkdir(parents=True, exist_ok=True)
        
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        target = meta.get("target", "prompt")
        fname = out_dir / f"{ts}_{target}_response.md"
        
        fname.write_text(content, encoding="utf-8")
