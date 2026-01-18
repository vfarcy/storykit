
# -*- coding: utf-8 -*-
"""
StoryKit CLI — assemble & validate
----------------------------------

Ce CLI propose deux commandes :

1) assemble : génère un prompt prêt à coller dans ton assistant IA
   Exemples :
     python -m cli.storykit assemble --target premise
     python -m cli.storykit assemble --target truby7
     python -m cli.storykit assemble --target truby22
     python -m cli.storykit assemble --target weave
     python -m cli.storykit assemble --target draft --chapter 1

2) validate : vérifie la validité et la cohérence des fichiers YAML/MD
   Exemples :
     python -m cli.storykit validate

Dépendances : pyyaml (yaml), rich (facultatif pour l’affichage)
"""


import argparse
import sys
import re
from pathlib import Path
from datetime import datetime

# Charger les variables d'environnement depuis .env à la racine du projet
try:
    import os
    from pathlib import Path
    from dotenv import load_dotenv
    # Force le chargement du .env à la racine du projet, même si le cwd est différent
    load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env", override=True)
except ImportError:
    pass  # python-dotenv non installé, ignorer

import yaml  # pip install pyyaml

# Affichage "riche" si dispo, sinon fallback simple
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
except Exception:  # pragma: no cover
    class Console:
        def print(self, *args, **kwargs):
            print(*args)

    class Panel:
        def __init__(self, text, **kwargs):
            self.text = text
        def __str__(self):
            return str(self.text)

    class Table:
        def __init__(self, title=None, box=None):
            self.title = title
            self.rows = []
        def add_column(self, name, justify=None, style=None):
            pass
        def add_row(self, *cells):
            self.rows.append(cells)

console = Console()

# Racines
ROOT = Path(__file__).resolve().parents[1]
STORY = ROOT / "story"
CONFIG = STORY / "config" / "storykit.config.yaml"
OUTDIR = ROOT / "out" / "prompts"

# ---------------------------
# Utilitaires de lecture
# ---------------------------

def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""

def read_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as e:
        # on remontera l’erreur côté validate
        return {"__YAML_ERROR__": str(e)}

def load_config() -> dict:
    return read_yaml(CONFIG)


def demote_headers(text: str, levels: int = 1) -> str:
    """Ajoute des '#' aux titres markdown existants pour les décaler."""
    if not text:
        return ""
    prefix = "#" * levels
    return re.sub(r"^(#+)", lambda m: prefix + m.group(1), text, flags=re.MULTILINE)


def estimate_tokens(text: str) -> int:
    """
    Estimation simple des tokens : environ 1 token par 4 caractères (moyenne pour le français).
    Pour une estimation précise, utiliser tiktoken ou la lib de l'API.
    """
    return len(text) // 4


def check_token_budget(payload: str, max_tokens: int, target: str) -> None:
    """
    Vérifie si le prompt dépassera le budget de tokens et affiche un avertissement.
    """
    estimated_input = estimate_tokens(payload)
    # On suppose que la réponse sera aussi longue que l'input (heuristique conservative)
    estimated_total = estimated_input + max_tokens
    
    if estimated_input > max_tokens * 0.8:  # Avertissement si input > 80% du budget
        msg = (
            f"Attention: Le prompt d'entrée ({estimated_input} tokens estimés) "
            f"approche la limite max_tokens ({max_tokens}). "
            f"La réponse risque d'être tronquée."
        )
        console.print(f"[yellow]{msg}[/yellow]")
    elif estimated_input > max_tokens:
        msg = (
            f"Erreur: Le prompt d'entrée ({estimated_input} tokens) "
            f"dépasse max_tokens ({max_tokens}). "
            f"L'API rejettera cette requête."
        )
        console.print(f"[red]{msg}[/red]")


# ---------------------------
# Assemble: construction de prompt
# ---------------------------

def assemble_payload(target: str, chapter: int | None = None) -> str:
    # Charger le contenu nécessaire
    p = {
        "premise": read_text(STORY / "truby" / "premise.md"),
        "seven": read_text(STORY / "truby" / "seven_steps.yaml"),
        "twentytwo": read_text(STORY / "truby" / "twenty_two_steps.yaml"),
        "moral": read_text(STORY / "truby" / "moral_argument.md"),
        "web": read_text(STORY / "truby" / "character_web.yaml"),
        "world": read_text(STORY / "truby" / "story_world.md"),
        "symbols": read_text(STORY / "truby" / "symbol_web.yaml"),
        "genre": read_text(STORY / "genre" / "genre_choice.yaml"),
        "beats": read_text(STORY / "genre" / "genre_beats.yaml"),
        "weave": read_text(STORY / "outline" / "scene_weave.md"),
        "acts": read_text(STORY / "outline" / "act_map.yaml"),
        "tasks": read_text(STORY / "tasks" / "tasks.yaml"),
        "style": read_text(STORY / "config" / "style.md"),
    }

    # Construire le header de manière sûre (évite l’erreur d’“unterminated f-string”)
    header_lines = []
    header_lines.append("# CONTEXTE GÉNÉRAL\n")

    header_lines.append("## Prémisse\n")
    header_lines.append(demote_headers(p["premise"], 2) + "\n")

    # Inclure systématiquement le style/voix si présent
    if p["style"].strip():
        header_lines.append("## Style & Voix\n")
        header_lines.append(demote_headers(p["style"], 2) + "\n\n")

    if target in ("truby7", "truby22", "web", "genre", "weave", "draft"):
        header_lines.append("## 7 étapes\n```yaml\n")
        header_lines.append(p["seven"])
        header_lines.append("\n```\n\n")

        header_lines.append("## 22 étapes\n```yaml\n")
        header_lines.append(p["twentytwo"])
        header_lines.append("\n```\n\n")

        header_lines.append("## Argument moral\n")
        header_lines.append(demote_headers(p["moral"], 2) + "\n\n")

        header_lines.append("## Web de personnages\n```yaml\n")
        header_lines.append(p["web"])
        header_lines.append("\n```\n\n")

        header_lines.append("## Monde de l’histoire\n")
        header_lines.append(demote_headers(p["world"], 2) + "\n\n")

        header_lines.append("## Symboles\n```yaml\n")
        header_lines.append(p["symbols"])
        header_lines.append("\n```\n\n")

        header_lines.append("## Genre\n```yaml\n")
        header_lines.append(p["genre"])
        header_lines.append("\n```\n\n")

        header_lines.append("## Beats de genre\n```yaml\n")
        header_lines.append(p["beats"])
        header_lines.append("\n```\n\n")

        if p["weave"].strip():
            header_lines.append("## Scene Weave\n")
            header_lines.append(demote_headers(p["weave"], 2) + "\n\n")

    # Instructions selon la target
    instructions_lines = []
    instructions_lines.append("# INSTRUCTIONS\n")

    

        

    
    if target == "premise":
        instructions_lines += [
            "- Affiner la prémisse en 1 phrase claire et porteuse d’un enjeu.\n",
            "- Proposer 3 variantes de principe organisateur.\n",
            "- Sortie : Markdown avec sections 'Prémisse', 'Principe organisateur', 'Promesse'.\n",
        ]
    elif target == "truby7":
        instructions_lines += [
            "- Construire les 7 étapes (faiblesse/besoin → nouvel équilibre) à partir de la prémisse.\n",
            "- Rendre explicite le problème moral.\n",
            "- Respecter le style défini dans Style & Voix.\n",
            "- Sortie : YAML 'seven_steps'.\n",
        ]
    elif target == "truby22":
        instructions_lines += [
            "- Proposer une chaîne de 22 étapes cohérente avec les beats de genre.\n",
            "- Indiquer pour chaque étape la valeur en jeu.\n",
            "- Respecter le style défini dans Style & Voix.\n",
            "- Sortie : YAML 'twenty_two_steps' (avec notes).\n",
        ]
    elif target == "web":
        instructions_lines += [
            "- Construire un web de personnages contrasté (fonction, valeurs, désir).\n",
            "- Ajouter 2 antagonistes secondaires et 1 allié révélateur.\n",
            "- Respecter le style défini dans Style & Voix.\n",
            "- Sortie : YAML 'characters'.\n",
        ]
    elif target == "genre":
        instructions_lines += [
            "- Valider le choix de genre et décliner 6 beats obligatoires adaptés au projet.\n",
            "- Décrire la philosophie du genre en 2 phrases.\n",
            "- Respecter le style défini dans Style & Voix.\n",
            "- Sortie : YAML 'required_beats'.\n",
        ]
    elif target == "weave":
        instructions_lines += [
            "- Générer le scene-weave (liste de scènes) en respectant 22 étapes et beats.\n",
            "- Pour chaque scène : conflit, décision, valeur en jeu, beat de genre.\n",
            "- Respecter le style défini dans Style & Voix.\n",
            "- Sortie : tableau Markdown.\n",
        ]
    elif target == "draft":
        if chapter is None:
            chapter = 1
        instructions_lines += [
            f"- Rédiger le brouillon du Chapitre {chapter} en suivant le scene-weave correspondant.\n",
            "- Respecter la trajectoire morale et les valeurs en jeu.\n",
            "- Style : français clair, focalisation interne limitée.\n",
            "- Respecter le style défini dans Style & Voix.\n",
            "- Sortie : Markdown, sections = scènes, sans méta-commentaires.\n",
        ]
    else:
        instructions_lines.append("- Tâche générique : synthétiser et proposer des options.\n")

    payload = "".join(header_lines) + "\n" + "".join(instructions_lines)
    return payload


class DryRunAdapter:
    def send(self, payload: str, meta: dict) -> str:
        OUTDIR.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = OUTDIR / f"{ts}_{meta.get('target','prompt')}.md"
        fname.write_text(payload, encoding="utf-8")
        return f"[dry-run] prompt écrit: {fname}"


ADAPTERS = {
    "dry-run": DryRunAdapter,
}

# Charger les adaptateurs réels si disponibles
try:
    from cli.adapters.claude import ClaudeAdapter
    ADAPTERS["claude"] = ClaudeAdapter
except (ImportError, ValueError):
    pass  # Module anthropic ou clé API manquante

try:
    from cli.adapters.copilot import CopilotAdapter
    ADAPTERS["copilot"] = CopilotAdapter
    ADAPTERS["openai"] = CopilotAdapter  # alias
except (ImportError, ValueError):
    pass  # Module openai ou clé API manquante

try:
    from cli.adapters.gemini import GeminiAdapter
    ADAPTERS["gemini"] = GeminiAdapter
except (ImportError, ValueError):
    pass  # Module google.generativeai ou clé API manquante


# ---------------------------
# Validate: contrôles YAML/MD
# ---------------------------

class ValidationError(Exception):
    pass

def _read_yaml_or_error(path: Path, issues: list[str]) -> dict:
    data = read_yaml(path)
    err = data.get("__YAML_ERROR__")
    if err:
        issues.append(f"[yaml] Erreur YAML dans {path}: {err}")
        return {}
    return data

def validate_seven_steps(issues: list[str]) -> None:
    p = STORY / "truby" / "seven_steps.yaml"
    data = _read_yaml_or_error(p, issues).get("seven_steps", {})

    # weakness_need peut être une chaîne ou un objet avec 'internal'
    wn = data.get("weakness_need")
    if isinstance(wn, dict):
        wn_internal = wn.get("internal")
        if not (isinstance(wn_internal, str) and wn_internal.strip()):
            issues.append("[seven_steps] Champ requis absent/vide: weakness_need.internal")
    elif isinstance(wn, str):
        if not wn.strip():
            issues.append("[seven_steps] Champ requis absent/vide: weakness_need (string)")
    else:
        issues.append("[seven_steps] weakness_need manquant ou de type invalide (attendu str ou mapping)")

    # desire doit être une chaîne non vide
    desire = data.get("desire")
    if not (isinstance(desire, str) and desire.strip()):
        issues.append("[seven_steps] Champ requis absent/vide: desire")

    # opponent peut être une chaîne ou un objet avec 'name'
    op = data.get("opponent")
    if isinstance(op, dict):
        op_name = op.get("name")
        if not (isinstance(op_name, str) and op_name.strip()):
            issues.append("[seven_steps] Champ requis absent/vide: opponent.name")
    elif isinstance(op, str):
        if not op.strip():
            issues.append("[seven_steps] Champ requis absent/vide: opponent (string)")
    else:
        issues.append("[seven_steps] opponent manquant ou de type invalide (attendu str ou mapping)")

def validate_genre(issues: list[str]) -> set[str]:
    p_choice = STORY / "genre" / "genre_choice.yaml"
    p_beats  = STORY / "genre" / "genre_beats.yaml"

    choice = _read_yaml_or_error(p_choice, issues).get("genre", {})
    beats  = _read_yaml_or_error(p_beats, issues).get("required_beats", [])

    primary = choice.get("primary")
    allowed = {"drama","detective","romance","horror","action","thriller","mystery","fantasy","sci-fi","crime"}
    if not isinstance(primary, str) or primary not in allowed:
        issues.append(f"[genre_choice] 'primary' invalide ou absent: {primary} (attendu ∈ {sorted(allowed)})")

    seen = set()
    id_re = re.compile(r"^g\d{2}$")
    for i, beat in enumerate(beats, 1):
        bid = beat.get("id")
        name = beat.get("name")
        status = beat.get("status", "planned")
        if not (isinstance(bid, str) and id_re.match(bid)):
            issues.append(f"[genre_beats] id invalide à l’item {i}: {bid} (format gNN)")
        if bid in seen:
            issues.append(f"[genre_beats] id dupliqué: {bid}")
        seen.add(bid)
        if not isinstance(name, str) or not name.strip():
            issues.append(f"[genre_beats] name manquant à l’item {i}")
        if status not in {"planned","locked","done"}:
            issues.append(f"[genre_beats] status invalide pour {bid}: {status}")

    return seen  # renvoie l’ensemble des ids valides (g01, g02, ...)

def _parse_scene_weave_table(text: str) -> list[dict]:
    """
    Renvoie une liste de dicts avec au moins les clés:
      index, fonction, lieu, conflit, decision, valeur, beat
    Hypothèse: table Markdown avec en-têtes standard.
    """
    rows = []
    lines = [ln.rstrip() for ln in text.splitlines() if ln.strip()]
    data_lines = [ln for ln in lines if ln.startswith("|")]
    if len(data_lines) < 3:
        return rows  # pas de table exploitable
    # Ignore la ligne de séparateurs (|---|)
    content = [ln for ln in data_lines if not ln.startswith("|---")]
    header = [h.strip().lower() for h in content[0].strip("|").split("|")]
    for ln in content[1:]:
        cols = [c.strip() for c in ln.strip("|").split("|")]
        if len(cols) != len(header):
            # ligne invalide, on ignore
            continue
        row = dict(zip(header, cols))
        rows.append({
            "index": row.get("#") or row.get("n") or row.get("no") or "",
            "fonction": row.get("fonction truby",""),
            "lieu": row.get("lieu",""),
            "conflit": row.get("conflit",""),
            "decision": row.get("décision","") or row.get("decision",""),
            "valeur": row.get("valeur en jeu",""),
            "beat": row.get("beat de genre","") or row.get("beat",""),
        })
    return rows

def validate_scene_weave(valid_beats: set[str], issues: list[str]) -> None:
    p = STORY / "outline" / "scene_weave.md"
    text = read_text(p)
    rows = _parse_scene_weave_table(text)
    if not rows:
        issues.append("[scene_weave] Table introuvable ou vide.")
        return
    # Vérifie au moins 1 scène “pivot”
    pivots = {"first revelation", "midpoint", "battle", "self-revelation"}
    has_pivot = any(any(pv in r["fonction"].lower() for pv in pivots) for r in rows)
    if not has_pivot:
        issues.append("[scene_weave] Aucun pivot (First Revelation/Midpoint/Battle/Self-Revelation) détecté.")

    # Vérifie référence de beat
    for r in rows:
        beat = r["beat"]
        if beat and beat not in valid_beats:
            issues.append(f"[scene_weave] Beat inconnu sur la scène #{r['index']}: {beat}")

def validate_style(issues: list[str], autofix: bool, optional_autofix: str) -> None:
    """Assure que story/config/style.md contient Ton, Voix, Rythme.
    Si vide ou rubriques manquantes, insère automatiquement un squelette et informe l'utilisateur.
    optional_autofix contrôle l'insertion de sections facultatives: 'none', 'forbidden', 'examples', 'both'.
    """
    p = STORY / "config" / "style.md"
    text = read_text(p)

    # Détection des rubriques existantes
    found = set()
    heading_re = re.compile(r"^\s*#{1,6}\s*(Ton|Voix|Rythme)\b", re.IGNORECASE | re.MULTILINE)
    for m in heading_re.finditer(text):
        found.add(m.group(1).lower())
    label_re = re.compile(r"^\s*(Ton|Voix|Rythme)\s*:\s*", re.IGNORECASE | re.MULTILINE)
    for m in label_re.finditer(text):
        found.add(m.group(1).lower())

    required = {"ton","voix","rythme"}

    # Si fichier vide, écrire le squelette complet
    if not text.strip():
        skeleton = (
            "# Ton\n"
            "Ex.: Intime, sobre, ironie mesurée ; éviter le pathos, jargon.\n\n"
            "# Voix\n"
            "Ex.: Focalisation interne limitée ; vocabulaire concret ; métaphores discrètes.\n\n"
            "# Rythme\n"
            "Ex.: Phrases 12–18 mots ; alternance court/long ; paragraphes 3–5 phrases.\n"
        )
        if autofix:
            p.write_text(skeleton, encoding="utf-8")
            console.print(Panel(f"Squelette inséré automatiquement dans {p}: Ton, Voix, Rythme", title="Auto-fix style.md"))
            return
        else:
            issues.append("[style] Fichier style.md vide (auto-fix désactivé).")
            return

    # Sinon, ajouter uniquement les rubriques manquantes en fin de fichier
    missing = sorted(required - found)
    if missing:
        additions = []
        for key in missing:
            if key == "ton":
                additions.append("\n\n# Ton\nEx.: Intime, sobre, ironie mesurée ; éviter le pathos, jargon.")
            elif key == "voix":
                additions.append("\n\n# Voix\nEx.: Focalisation interne limitée ; vocabulaire concret ; métaphores discrètes.")
            elif key == "rythme":
                additions.append("\n\n# Rythme\nEx.: Phrases 12–18 mots ; alternance court/long ; paragraphes 3–5 phrases.")
        if autofix:
            new_text = text + "".join(additions)
            p.write_text(new_text, encoding="utf-8")
            console.print(Panel(f"Rubriques ajoutées automatiquement dans {p}: {', '.join(missing)}", title="Auto-fix style.md"))
            # Pas d'ajout dans issues car corrigé automatiquement
        else:
            issues.append(f"[style] Rubriques manquantes: {', '.join(sorted(missing))} (auto-fix désactivé)")

    # Sections optionnelles selon optional_autofix
    if autofix and optional_autofix in ("forbidden", "both"):
        if "# Interdits" not in text and "## Interdits" not in text:
            forbidden_section = "\n\n# Interdits stylistiques\nAdverbes vagues (très, vraiment) ; clichés ; hyperboles gratuites ; passifs en chaîne.\n"
            text = read_text(p)  # re-read au cas où modifié
            p.write_text(text + forbidden_section, encoding="utf-8")
            console.print(Panel(f"Section 'Interdits' ajoutée dans {p}", title="Auto-fix style.md (optional)"))

    if autofix and optional_autofix in ("examples", "both"):
        if "# Exemples" not in text and "## Exemples" not in text:
            examples_section = "\n\n# Exemples\nConforme: 'Il observa sans dramatiser.'  \nNon conforme: 'C'était incroyable !!!'\n"
            text = read_text(p)  # re-read
            p.write_text(text + examples_section, encoding="utf-8")
            console.print(Panel(f"Section 'Exemples' ajoutée dans {p}", title="Auto-fix style.md (optional)"))

def validate_all(autofix_style: bool, optional_autofix: str) -> list[str]:
    issues: list[str] = []
    valid_beats = validate_genre(issues)
    validate_seven_steps(issues)
    validate_scene_weave(valid_beats, issues)
    validate_style(issues, autofix_style, optional_autofix)
    # Ajouter ici d’autres validations si nécessaire (moral_argument, character_web, etc.)
    return issues


# ---------------------------
# Main
# ---------------------------

def main(argv=None):
    argv = argv or sys.argv[1:]
    parser = argparse.ArgumentParser(prog="storykit", description="CLI StoryKit (assemble & validate)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # assemble
    assemble = sub.add_parser("assemble", help="Assembler un prompt prêt pour IA")
    assemble.add_argument("--target", required=True,
                          choices=["premise","truby7","truby22","web","genre","weave","draft"])
    assemble.add_argument("--chapter", type=int, help="Numéro de chapitre pour --target draft")

    # validate
    validate = sub.add_parser("validate", help="Valider les YAML/MD et la cohérence du projet")
    validate.add_argument("--no-autofix-style", action="store_true", help="Désactiver l'auto-fix de style.md (Ton/Voix/Rythme)")

    args = parser.parse_args(argv)

    if args.cmd == "validate":
        cfg = load_config()
        autofix_cfg = cfg.get("style", {}).get("autofix", True)
        autofix_style = False if getattr(args, "no_autofix_style", False) else autofix_cfg
        optional_autofix = cfg.get("style", {}).get("optional_autofix", "none")
        issues = validate_all(autofix_style, optional_autofix)
        if issues:
            # Affichage lisible
            table = Table(title="Problèmes détectés")
            table.add_column("N°", justify="right", style="bold red")
            table.add_column("Message", justify="left")
            for i, it in enumerate(issues, start=1):
                table.add_row(str(i), it)
            console.print(table)
            # Code retour ≠ 0 pour CI
            raise SystemExit(1)
        console.print(Panel("✅ Validation OK — aucun problème détecté.", title="Validation"))
        return

    # assemble
    cfg = load_config()
    ai_cfg = cfg.get("ai", {})
    provider = ai_cfg.get("provider", "dry-run")
    model = ai_cfg.get("model")
    max_tokens = ai_cfg.get("max_tokens", 4000)
    AdapterCls = ADAPTERS.get(provider, DryRunAdapter)
    adapter = AdapterCls()

    payload = assemble_payload(args.target, chapter=args.chapter)
    
    # Vérifier le budget de tokens avant d'envoyer
    check_token_budget(payload, max_tokens, args.target)
    
    meta = {
        "target": args.target,
        "provider": provider,
        "model": model,
        "max_tokens": max_tokens,
    }
    result = adapter.send(payload, meta)
    console.print(Panel(f"{result}", title="Assemble"))


if __name__ == "__main__":
    main()
