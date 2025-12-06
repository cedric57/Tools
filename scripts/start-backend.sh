#!/bin/bash
# scripts/start-backend.sh - Démarrage technique du backend

echo "🔧 Démarrage du backend FastAPI avec uv..."
cd backend || exit 1

# Vérifier que uv est installé
if ! command -v uv &> /dev/null; then
    echo "❌ uv n'est pas installé. Installation..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

echo "📦 Installation des dépendances..."
uv sync

echo "🚀 Lancement de FastAPI..."
uv run uvicorn main:app --host 127.0.0.1 --port 8000 --reload
