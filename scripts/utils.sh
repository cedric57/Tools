#!/bin/bash
# scripts/utils.sh - Fonctions utilitaires pour les scripts Shell

# Fonction de logging coloré
log_info() {
    echo "🔵 $1"
}

log_success() {
    echo "✅ $1"
}

log_warning() {
    echo "⚠️  $1"
}

log_error() {
    echo "❌ $1" >&2
}

# Vérifier si une commande existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Vérifier si un port est utilisé
is_port_used() {
    local port=$1
    if command_exists "lsof"; then
        lsof -i :"$port" >/dev/null 2>&1
    else
        netstat -tuln 2>/dev/null | grep -q ":$port "
    fi
}

# Attendre qu'un service soit disponible
wait_for_service() {
    local host=$1
    local port=$2
    local timeout=$3
    local counter=0

    while ! nc -z "$host" "$port" >/dev/null 2>&1; do
        sleep 1
        counter=$((counter + 1))
        if [ "$counter" -ge "$timeout" ]; then
            log_error "Timeout waiting for $host:$port"
            return 1
        fi
    done
    log_success "Service $host:$port is available"
    return 0
}
