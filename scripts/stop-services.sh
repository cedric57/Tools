#!/bin/bash
# scripts/stop-services.sh - Arrêt des services

echo "🛑 Arrêt des services..."

# Arrêter les processus backend
pkill -f "uvicorn main:app" && echo "✅ Backend arrêté"

# Arrêter les processus frontend
pkill -f "npm run dev" && echo "✅ Frontends arrêtés"

echo "✅ Tous les services sont arrêtés"
