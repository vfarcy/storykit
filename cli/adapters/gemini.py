"""
Adaptateur Google Gemini
Installer : pip install google-generativeai
Config : ajouter GOOGLE_API_KEY dans .env ou variable d'environnement
"""
import os
from datetime import datetime
from pathlib import Path

try:
    import google.genai as genai
except ImportError:
    genai = None


class GeminiAdapter:
    def __init__(self):
        if genai is None:
            raise ImportError(
                "Le module 'google-generativeai' n'est pas installé. "
                "Installez-le avec: pip install google-generativeai"
            )
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError(
                "GOOGLE_API_KEY manquante. "
                "Définissez-la dans .env ou comme variable d'environnement."
            )
        # Plus besoin de genai.configure avec google-genai >= 1.0
        self.api_key = api_key
        # Initialisation du client Gemini
        self.client = genai.Client(api_key=api_key)
        
    def send(self, payload: str, meta: dict) -> str:
        """
        Envoie le prompt à Gemini et retourne la réponse.
        Sélectionne automatiquement le modèle optimal selon la tâche, sauf override explicite.
        """
        # Sélection automatique selon la tâche (target)
        target = meta.get("target", "")
        user_model = meta.get("model")
        # Table de correspondance tâche → modèle
        task_model_map = {
            "premise": "gemini-2.5-flash",
            "genre": "gemini-2.5-flash",
            "truby7": "gemini-2.5-flash",
            "truby22": "gemini-2.5-pro",
            "weave": "gemini-2.5-pro",
            "draft": "gemini-2.5-pro",
        }
        # Si override explicite, priorité à l'utilisateur
        if user_model:
            model_name = user_model
        else:
            model_name = task_model_map.get(target, "gemini-2.5-flash")
        max_tokens = meta.get("max_tokens", 4096)
        try:
            from google.genai import types
            config = types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=max_tokens
            )
            response = self.client.models.generate_content(
                model=model_name,
                contents=payload,
                config=config
            )
            content = getattr(response, 'text', None) or str(response)
            self._save_response(content, meta)
            return f"[gemini] Modèle utilisé : {model_name} — Réponse reçue ({len(content)} caractères) — sauvegardée dans out/responses/"
        except Exception as e:
            return f"[gemini] Erreur: {e}"

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
