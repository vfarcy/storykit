
from pathlib import Path
import re
import yaml

class ValidationError(Exception):
    pass

def _read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""

def _read_yaml(p: Path):
    if not p.exists():
        raise ValidationError(f"Fichier manquant: {p}")
    try:
        return yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as e:
        raise ValidationError(f"YAML invalide dans {p} : {e}")

def validate_seven_steps(root: Path, issues: list[str]):
    p = root / "story/truby/seven_steps.yaml"
    data = _read_yaml(p)
    s = data.get("seven_steps", {})
    required_str = [
        ("weakness_need.internal", s.get("weakness_need", {}).get("internal")),
        ("desire", s.get("desire")),
        ("opponent.name", s.get("opponent", {}).get("name")),
    ]
    for key, val in required_str:
        if not isinstance(val, str) or not val.strip():
            issues.append(f"[seven_steps] Champ requis absent/vide: {key}")

def validate_genre(root: Path, issues: list[str]):
    p_choice = root / "story/genre/genre_choice.yaml"
    p_beats  = root / "story/genre/genre_beats.yaml"
    choice = _read_yaml(p_choice).get("genre", {})
    beats  = _read_yaml(p_beats).get("required_beats", [])

    primary = choice.get("primary")
    allowed = {"detective","romance","horror","action","thriller","mystery","fantasy","sci-fi","crime"}
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

def _parse_scene_weave_table(text: str):
    """
    Renvoie une liste de dicts avec au moins les clés:
      index, fonction, lieu, conflit, decision, valeur, beat
    Hypothèse: table Markdown avec en-têtes standard.
    """
    rows = []
    lines = [ln.rstrip() for ln in text.splitlines() if ln.strip()]
    # Cherche la ligne d'en-tête et sépare à '|'
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
        # normalisation colonnes utiles
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

def validate_scene_weave(root: Path, valid_beats: set[str], issues: list[str]):
    p = root / "story/outline/scene_weave.md"
    text = _read_text(p)
    rows = _parse_scene_weave_table(text)
    if not rows:
        issues.append("[scene_weave] Table introuvable ou vide.")
        return
    # Vérifie au moins 1 scène “pivot”
    pivots = {"first revelation","midpoint","battle","self-revelation"}
    has_pivot = any(any(pv in r["fonction"].lower() for pv in pivots) for r in rows)
    if not has_pivot:
        issues.append("[scene_weave] Aucun pivot (First Revelation/Midpoint/Battle/Self-Revelation) détecté.")

    # Vérifie référence de beat
    for r in rows:
        beat = r["beat"]
        if beat and beat not in valid_beats:
            issues.append(f"[scene_weave] Beat inconnu sur la scène #{r['index']}: {beat}")

def validate_all(repository_root: Path) -> list[str]:
    issues: list[str] = []
    valid_beats = validate_genre(repository_root, issues)
    validate_seven_steps(repository_root, issues)
    validate_scene_weave(repository_root, valid_beats, issues)
    # Tu peux ajouter ici d’autres validations (moral_argument, character_web, etc.)
    return issues
