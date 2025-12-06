#!/bin/bash
# start-dev.sh - Script racine principal

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Vérifier si utils.sh existe avant de le sourcer
if [ -f "${SCRIPT_DIR}/scripts/utils.sh" ]; then
    # shellcheck source=scripts/utils.sh
    source "${SCRIPT_DIR}/scripts/utils.sh"
fi

echo "🚀 Démarrage de l'application complète..."
echo ""

# Vérifier les prérequis
if ! "${SCRIPT_DIR}/scripts/check-prerequisites.sh"; then
    exit 1
fi

# Menu principal
while true; do
    echo "--- Menu Principal ---"
    echo "1) Démarrer tous les services"
    echo "2) Démarrer backend seulement"
    echo "3) Démarrer frontend seulement"
    echo "4) Vérifier l'état des services"
    echo "5) Arrêter tous les services"
    echo "q) Quitter"
    echo "---------------------"
    read -r -p "Choisissez une option: " choice

    case "$choice" in
        1)
            "${SCRIPT_DIR}/scripts/start-backend.sh" &
            BACKEND_PID=$!
            "${SCRIPT_DIR}/scripts/start-frontend.sh" &
            FRONTEND_PID=$!
            echo "✅ Services démarrés (Backend: $BACKEND_PID, Frontend: $FRONTEND_PID)"
            ;;
        2)
            "${SCRIPT_DIR}/scripts/start-backend.sh"
            ;;
        3)
            "${SCRIPT_DIR}/scripts/start-frontend.sh"
            ;;
        4)
            "${SCRIPT_DIR}/scripts/health-check.sh"
            ;;
        5)
            "${SCRIPT_DIR}/scripts/stop-services.sh"
            ;;
        q|Q)
            echo "👋 Au revoir!"
            exit 0
            ;;
        *)
            echo "❌ Option invalide"
            ;;
    esac
    echo ""
done
