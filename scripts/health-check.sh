#!/bin/bash
# scripts/health-check.sh - Vérification santé des services

check_port() {
    if nc -z localhost "$1" 2>/dev/null; then
        echo "✅ Port $1: Service actif"
        return 0
    else
        echo "❌ Port $1: Service inactif"
        return 1
    fi
}

echo "🏥 Vérification de l'état des services..."

check_port 8000  # Backend
check_port 3000  # Marketing
check_port 3001  # App

echo "📊 Vérification terminée"
