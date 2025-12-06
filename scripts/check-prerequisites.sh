#!/bin/bash
# scripts/check-prerequisites.sh - Vérification des prérequis

echo "🔍 Vérification des prérequis..."

check_command() {
    if command -v "$1" >/dev/null 2>&1; then
        echo "✅ $1 trouvé"
        return 0
    else
        echo "❌ $1 non trouvé"
        return 1
    fi
}

check_directory() {
    if [ -d "$1" ]; then
        echo "✅ Répertoire $1 trouvé"
        return 0
    else
        echo "❌ Répertoire $1 introuvable"
        return 1
    fi
}

# Vérifier les commandes
check_command "node" || exit 1
check_command "npm" || exit 1
check_command "python3" || exit 1

# Vérifier les répertoires
check_directory "frontend/marketing" || exit 1
check_directory "frontend/app" || exit 1
check_directory "backend" || exit 1

echo "✅ Tous les prérequis sont satisfaits!"
exit 0
