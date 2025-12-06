# start-dev.ps1
Write-Host "🚀 Démarrage de l'application complète..." -ForegroundColor Blue
Write-Host "📍 Backend: FastAPI sur http://localhost:8000" -ForegroundColor Gray
Write-Host "📍 Marketing (Astro): http://localhost:3000" -ForegroundColor Gray
Write-Host "📍 App (Next.js): http://localhost:3001" -ForegroundColor Gray
Write-Host "Press 'q' pour arrêter tous les services" -ForegroundColor Cyan
Write-Host ""

# Vérifier les répertoires
$directories = @("backend", "frontend/marketing", "frontend/app")
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        Write-Host "❌ Répertoire $dir introuvable!" -ForegroundColor Red
        exit 1
    }
}

# Démarrer les services
$jobs = @()

Write-Host "📦 Démarrage du Backend FastAPI..." -ForegroundColor Magenta
$backendJob = Start-Job -Name "Backend" -ScriptBlock {
    Set-Location "backend"
    uvicorn main:app --reload --port 8000
}
$jobs += $backendJob

Write-Host "📦 Démarrage du Marketing Astro..." -ForegroundColor Cyan
$marketingJob = Start-Job -Name "Marketing" -ScriptBlock {
    Set-Location "frontend/marketing"
    npm run dev
}
$jobs += $marketingJob

Write-Host "📦 Démarrage de l'App Next.js..." -ForegroundColor Green
$appJob = Start-Job -Name "App" -ScriptBlock {
    Set-Location "frontend/app"
    npm run dev
}
$jobs += $appJob

Write-Host "`n✅ Tous les services sont en cours de démarrage..." -ForegroundColor Green

# Menu interactif
do {
    Write-Host "--- Menu de contrôle ---" -ForegroundColor Yellow
    Write-Host "1) Voir les logs du Backend"
    Write-Host "2) Voir les logs du Marketing"
    Write-Host "3) Voir les logs de l'App"
    Write-Host "4) Voir l'état des services"
    Write-Host "q) Arrêter tous les services"
    Write-Host "------------------------"
    $choice = Read-Host "Choisissez une option"

    switch ($choice) {
        "1" {
            Write-Host "📋 Logs du Backend:" -ForegroundColor Magenta
            Receive-Job -Job $backendJob -Keep
        }
        "2" {
            Write-Host "📋 Logs du Marketing:" -ForegroundColor Cyan
            Receive-Job -Job $marketingJob -Keep
        }
        "3" {
            Write-Host "📋 Logs de l'App:" -ForegroundColor Green
            Receive-Job -Job $appJob -Keep
        }
        "4" {
            Write-Host "📊 État des services:" -ForegroundColor Yellow
            Get-Job | Format-Table Name, State, HasMoreData -AutoSize
        }
        "q" { break }
        default { Write-Host "Option invalide" -ForegroundColor Red }
    }
    Write-Host ""
} until ($choice -eq 'q')

# Nettoyage
Write-Host "🛑 Arrêt des services..." -ForegroundColor Yellow
Get-Job | Stop-Job
Get-Job | Remove-Job
Write-Host "✅ Tous les services sont arrêtés." -ForegroundColor Green
