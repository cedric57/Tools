#!/bin/bash
# scripts/start-frontend.sh - Démarrage technique des fronts

echo "🔧 Démarrage des applications frontend..."

# Fonction pour démarrer un frontend
start_frontend() {
    local name=$1
    local dir=$2
    local port=$3

    echo "📦 Démarrage de $name..."
    cd "$dir" || return 1

    # Vérifier si node_modules existe
    if [ ! -d "node_modules" ]; then
        echo "📦 Installation des dépendances pour $name..."
        npm install
    fi

    # Démarrer en arrière-plan
    npm run dev &
    local pid=$!
    echo "$name démarré sur le port $port (PID: $pid)"
    cd - > /dev/null || return
}

start_frontend "Marketing (Astro)" "frontend/marketing" "3000"
start_frontend "App (Next.js)" "frontend/app" "3001"

echo "✅ Frontends démarrés"
wait
