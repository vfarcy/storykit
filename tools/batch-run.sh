#!/bin/bash
# Helper pour exécuter des commandes batch depuis n'importe quel répertoire
# Usage: ../batch-run.sh list --limit 10
#        ../batch-run.sh draft-variants --chapter story/drafting/ChapX.md --styles minimaliste

# Forcer l'encodage UTF-8
export PYTHONIOENCODING=utf-8

# Déterminer le répertoire root du projet (parent de tools/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Activer l'environnement virtuel
if [ -d "$REPO_ROOT/.venv" ]; then
    source "$REPO_ROOT/.venv/bin/activate"
elif [ -d "$REPO_ROOT/.venvWORK" ]; then
    source "$REPO_ROOT/.venvWORK/bin/activate"
else
    echo "⚠️  Aucun environnement virtuel trouvé dans $REPO_ROOT"
    echo "   Créez-le avec: python -m venv .venv"
    exit 1
fi

# Exécuter la commande
cd "$REPO_ROOT"
python -m cli.batch "$@"
