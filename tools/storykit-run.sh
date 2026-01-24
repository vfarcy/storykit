#!/bin/bash
# Helper pour exécuter des commandes StoryKit depuis n'importe quel répertoire
# Doit être lancé depuis un livre (livre1-truby, livre2-monsoon, etc.)
# Usage: ../storykit-run.sh validate
#        ../storykit-run.sh assemble --target premise
#        ../storykit-run.sh assemble --target truby7

# Forcer l'encodage UTF-8
export PYTHONIOENCODING=utf-8

# Déterminer le répertoire root du projet (parent de tools/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Détecter le livre en cours en cherchant storykit.config.yaml
function find_current_book() {
    local current="$(pwd)"
    
    while [ "$current" != "/" ]; do
        if [ -f "$current/storykit.config.yaml" ]; then
            echo "$current"
            return 0
        fi
        current="$(dirname "$current")"
    done
    
    return 1
}

BOOK_PATH=$(find_current_book)

if [ -z "$BOOK_PATH" ]; then
    echo "✗ ERREUR : Impossible de détecter le livre en cours"
    echo "   Le fichier storykit.config.yaml n'a pas été trouvé"
    echo ""
    echo "   Pour utiliser StoryKit, naviguez vers un livre :"
    echo "   - cd livre1-truby"
    echo "   - cd livre2-monsoon"
    echo "   - ou un autre dossier contenant storykit.config.yaml"
    echo ""
    echo "   Puis relancez : ../storykit-run.sh validate"
    exit 1
fi

# Activer l'environnement virtuel
if [ -d "$REPO_ROOT/.venv" ]; then
    source "$REPO_ROOT/.venv/bin/activate"
elif [ -d "$REPO_ROOT/.venvWORK" ]; then
    source "$REPO_ROOT/.venvWORK/bin/activate"
else
    echo "✗ ERREUR : Aucun environnement virtuel trouvé"
    echo "   Créez-le avec : python -m venv .venv"
    exit 1
fi

# Ajouter la racine du repo au PYTHONPATH pour trouver le module cli
# On reste dans le répertoire courant pour que les chemins relatifs fonctionnent
export PYTHONPATH="$REPO_ROOT:$PYTHONPATH"
python -m cli.storykit "$@"
