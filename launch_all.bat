@echo off
chcp 65001 > nul
title 🚀 TrendIA Fake News Detection System

echo.
echo ========================================
echo       🎯 TRENDIA - DÉTECTION FAKE NEWS
echo ========================================
echo.

REM 1. Vérifier PostgreSQL
echo [1/4] Vérification de PostgreSQL...
sc query postgresql-x64-18 | find "RUNNING" > nul
if %errorlevel% neq 0 (
    echo ❌ PostgreSQL n'est pas démarré
    echo Démarrage du service...
    net start postgresql-x64-18
    timeout /t 3
)

REM 2. Activer l'environnement virtuel
echo [2/4] Activation de l'environnement virtuel...
call .venv\Scripts\activate

REM 3. Créer les dossiers nécessaires
echo [3/4] Préparation des dossiers...
if not exist reports mkdir reports
if not exist logs mkdir logs

REM 4. Lancer les services
echo [4/4] Lancement des services...
echo.

echo 📡 SERVICES EN COURS DE DÉMARRAGE...
echo.

echo ┌─────────────────────────────────────┐
echo │  🤖 API Modèles ML (port 8001)     │
echo └─────────────────────────────────────┘
start cmd /k "cd /d %CD% && .venv\Scripts\activate && python model/run_ml_api.py"

timeout /t 5

echo ┌─────────────────────────────────────┐
echo │  🚀 API Principale (port 8000)     │
echo └─────────────────────────────────────┘
start cmd /k "cd /d %CD% && .venv\Scripts\activate && python run.py"

timeout /t 5

echo ┌─────────────────────────────────────┐
echo │  🔍 Agent Watchdog                 │
echo └─────────────────────────────────────┘
start cmd /k "cd /d %CD% && .venv\Scripts\activate && python agent/watchdog.py"

echo.
echo ✅ TOUS LES SERVICES SONT LANCÉS !
echo.
echo 🌐 ACCÈS AU SYSTÈME :
echo    Frontend Principal : http://localhost:8000
echo    Documentation      : http://localhost:8000/docs
echo    API Modèles ML     : http://localhost:8001
echo    Docs ML API        : http://localhost:8001/docs
echo.
echo 📊 POUR TESTER :
echo   1. Ouvrez http://localhost:8000/docs
echo   2. Testez /api/ml/detect
echo   3. Testez /api/ml/tokens/high-risk
echo.
pause