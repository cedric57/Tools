#!/bin/bash

echo "🚀 Démarrage du backend Tools avec uv..."

# Vérifier que uv est installé
if ! command -v uv &> /dev/null; then
    echo "❌ uv n'est pas installé. Installation..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# Synchroniser les dépendances
echo "📦 Synchronisation des dépendances..."
uv sync

# Lancer l'application
echo "🔥 Lancement de l'application..."
uv run uvicorn main:app --host 127.0.0.1 --port 8000 --reload
