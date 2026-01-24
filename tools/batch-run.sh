#!/bin/bash
# Helper pour exécuter des commandes batch depuis n'importe quel répertoire
# Fonctionne depuis la racine du repo, peu importe le répertoire courant
# Usage: ../batch-run.sh list --limit 10
#        ../batch-run.sh draft-variants --chapter story/drafting/ChapX.md --styles minimaliste
#        ../batch-run.sh status msgbatch_XXXXX
#        ../batch-run.sh download msgbatch_XXXXX

# Forcer l'encodage UTF-8
export PYTHONIOENCODING=utf-8

# Déterminer le répertoire root du projet (parent de tools/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Vérifier que le repo est valide
if [ ! -f "$REPO_ROOT/livre1-truby/storykit.config.yaml" ]; then
    echo "✗ ERREUR : Impossible de trouver le répertoire du projet StoryKit"
    echo "   Assurez-vous d'être dans le repository story-repo-polar"
    echo "   Chemin attendu : $REPO_ROOT"
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

# Exécuter la commande
cd "$REPO_ROOT"
python -m cli.batch "$@"
