@echo off
echo 🚀 Démarrage du backend Tools avec uv...

REM Synchroniser les dépendances
echo 📦 Synchronisation des dépendances...
uv sync

REM Lancer l'application
echo 🔥 Lancement de l'application...
uv run uvicorn main:app --host 127.0.0.1 --port 8000 --reload
