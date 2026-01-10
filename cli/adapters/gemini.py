"""
Adaptateur Google Gemini
Installer : pip install google-generativeai
Config : ajouter GOOGLE_API_KEY dans .env ou variable d'environnement
"""
import os
from datetime import datetime
from pathlib import Path

try:
    import google.generativeai as genai
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
        genai.configure(api_key=api_key)
        
    def send(self, payload: str, meta: dict) -> str:
        """
        Envoie le prompt à Gemini et retourne la réponse.
        Sauvegarde aussi la réponse dans out/responses/.
        """
        model_name = meta.get("model") or "gemini-1.5-pro"
        max_tokens = meta.get("max_tokens", 4096)
        
        try:
            model = genai.GenerativeModel(model_name)
            
            # Configuration de génération
            generation_config = genai.types.GenerationConfig(
                max_output_tokens=max_tokens,
                temperature=0.7,
            )
            
            response = model.generate_content(
                payload,
                generation_config=generation_config
            )
            
            content = response.text if hasattr(response, 'text') else str(response)
            
            self._save_response(content, meta)
            
            return f"[gemini] Réponse reçue ({len(content)} caractères) — sauvegardée dans out/responses/"
            
        except Exception as e:
            return f"[gemini] Erreur: {e}"

    def _save_response(self, content: str, meta: dict):
        """Sauvegarde la réponse dans out/responses/"""
        out_dir = Path(__file__).resolve().parents[2] / "out" / "responses"
        out_dir.mkdir(parents=True, exist_ok=True)
        
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        target = meta.get("target", "prompt")
        fname = out_dir / f"{ts}_{target}_response.md"
        
        fname.write_text(content, encoding="utf-8")
