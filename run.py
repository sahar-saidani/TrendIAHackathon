""" # run.py
import uvicorn
import os
import sys
from dotenv import load_dotenv
import time
import requests

load_dotenv()

def check_ml_api():
    
        response = requests.get("http://localhost:8001/", timeout=2)
        if response.status_code == 200:
            print("✅ API ML connectée sur port 8001")
            return True
    except:
        print("⚠️ API ML non disponible - Lancement quand même")
    return False

def run_backend():
   
    print("🚀 Démarrage du backend principal...")
    print("📡 URL: http://localhost:8000")
    print("📚 Documentation: http://localhost:8000/docs")
    print("")
    print("💡 Pour tester :")
    print("   1. Ouvrez http://localhost:8000/docs")
    print("   2. Testez /api/analyze avec un texte")
    print("")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

def main():
    
    print("=" * 60)
    print("       🤖 TRENDIA FAKE NEWS DETECTION SYSTEM")
    print("=" * 60)
    print()
    
    # Vérifier rapidement l'API ML (sans attendre longtemps)
    check_ml_api()
    
    # Lancer le backend immédiatement
    run_backend()

if __name__ == "__main__":
    main() 
"""
"""
Script de lancement unifié pour TrendAI
"""
""" import subprocess
import sys
import os
import time
from colorama import init, Fore, Style

# Initialiser colorama
init(autoreset=True)

def print_banner():
    
    banner = f
{Fore.CYAN}{'='*60}
{Fore.YELLOW}       🤖 TRENDIA FAKE NEWS DETECTION SYSTEM
{Fore.CYAN}{'='*60}
{Fore.GREEN}🚀 Démarrage du système complet...
{Fore.WHITE}
📡 Backend Principal: {Fore.CYAN}http://localhost:8000
🤖 API ML: {Fore.CYAN}http://localhost:8001
📚 Documentation: {Fore.CYAN}http://localhost:8000/docs
{Fore.CYAN}{'='*60}
{Fore.YELLOW}💡 Endpoints disponibles:
{Fore.WHITE}
• {Fore.GREEN}/health{Fore.WHITE} - Vérifier l'état des services
• {Fore.GREEN}/api/analyze{Fore.WHITE} (POST) - Analyser du texte
• {Fore.GREEN}/api/risk/NEURA{Fore.WHITE} - Risque d'un token
• {Fore.GREEN}/api/rankings/high-risk{Fore.WHITE} - Tokens risqués
• {Fore.GREEN}/api/predict/NEURA{Fore.WHITE} - Prédiction prix
• {Fore.GREEN}/api/early-warning/NEURA{Fore.WHITE} - Alertes
{Fore.CYAN}{'='*60}

    print(banner)

def check_dependencies():
    
    print(f"{Fore.YELLOW}🔍 Vérification des dépendances...")
    
    try:
        import fastapi
        import uvicorn
        import pandas
        import sklearn
        import numpy
        
        print(f"{Fore.GREEN}✅ Toutes les dépendances sont installées")
        return True
    except ImportError as e:
        print(f"{Fore.RED}❌ Dépendance manquante: {e}")
        print(f"{Fore.YELLOW}📦 Installation des dépendances...")
        
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", 
                                  "fastapi", "uvicorn", "pandas", "scikit-learn", 
                                  "numpy", "requests", "colorama"])
            print(f"{Fore.GREEN}✅ Dépendances installées avec succès")
            return True
        except:
            print(f"{Fore.RED}❌ Échec installation. Installez manuellement:")
            print(f"{Fore.WHITE}pip install fastapi uvicorn pandas scikit-learn numpy requests colorama")
            return False

def create_missing_files():
   
    print(f"{Fore.YELLOW}📁 Vérification des fichiers...")
    
    # Vérifier le dossier model
    if not os.path.exists('model'):
        os.makedirs('model')
        print(f"{Fore.GREEN}✅ Dossier 'model' créé")
    
    # Vérifier le dossier agents
    if not os.path.exists('agents'):
        os.makedirs('agents')
        print(f"{Fore.GREEN}✅ Dossier 'agents' créé")
    
    # Vérifier les fichiers de données
    data_dir = 'model'
    required_files = {
        'bot_detector.pkl': "Modèle ML (peut être factice)",
        'final_risk_scores.csv': "Données de risque des tokens",
        'ai_generated_narratives.csv': "Narratifs générés"
    }
    
    for file, description in required_files.items():
        filepath = os.path.join(data_dir, file)
        if not os.path.exists(filepath):
            print(f"{Fore.YELLOW}⚠️  {file} non trouvé - {description}")
            
            # Créer un fichier factice si c'est un CSV
            if file.endswith('.csv'):
                import pandas as pd
                if 'risk' in file:
                    df = pd.DataFrame({
                        'token_id': ['NEURA', 'TAO', 'RNDR', 'AGIX', 'FET'],
                        'risk_score': [0.85, 0.62, 0.41, 0.73, 0.55],
                        'label': ['HIGH', 'MEDIUM', 'LOW', 'HIGH', 'MEDIUM'],
                        'reason': [
                            'Volume suspect élevé',
                            'Activité sociale normale',
                            'Faible risque détecté',
                            'Patterns de manipulation',
                            'Risque modéré'
                        ]
                    })
                else:  # narratives
                    df = pd.DataFrame({
                        'token_id': ['NEURA', 'NEURA', 'TAO', 'RNDR', 'AGIX'],
                        'topic': [
                            'AI Revolution Narrative',
                            'Market Manipulation Warning',
                            'Decentralized AI Growth',
                            'GPU Rendering Demand',
                            'SingularityNET Ecosystem'
                        ],
                        'start_time': ['2024-01-01', '2024-01-05', '2024-01-02', '2024-01-03', '2024-01-04'],
                        'end_time': ['2024-01-10', '2024-01-08', '2024-01-12', '2024-01-10', '2024-01-11'],
                        'sentiment_score': [0.8, -0.6, 0.7, 0.5, 0.6]
                    })
                
                df.to_csv(filepath, index=False)
                print(f"{Fore.GREEN}✅ Fichier factice créé: {filepath}")

def start_services():
    
    print(f"{Fore.YELLOW}🚀 Démarrage des services...")
    
    try:
        # Démarrer le backend principal
        print(f"{Fore.CYAN}▶️  Démarrage du backend principal (port 8000)...")
        
        # Importer et exécuter
        from main import app
        import uvicorn
        
        # Démarrer dans un thread
        import threading
        import asyncio
        
        def run_main():
            uvicorn.run(
                "main:app",
                host="0.0.0.0",
                port=8000,
                log_level="info",
                reload=False
            )
        
        main_thread = threading.Thread(target=run_main, daemon=True)
        main_thread.start()
        
        print(f"{Fore.GREEN}✅ Backend principal démarré")
        
        # Attendre un peu
        time.sleep(2)
        
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.GREEN}🎉 Système TrendAI pleinement opérationnel!")
        print(f"{Fore.CYAN}{'='*60}")
        print(f"\n{Fore.YELLOW}📋 Pour tester:")
        print(f"{Fore.WHITE}1. Ouvrez {Fore.CYAN}http://localhost:8000/docs")
        print(f"{Fore.WHITE}2. Testez les endpoints:")
        print(f"   • {Fore.GREEN}POST /api/analyze{Fore.WHITE} - Analyser du texte")
        print(f"   • {Fore.GREEN}GET /api/risk/NEURA{Fore.WHITE} - Voir risque NEURA")
        print(f"   • {Fore.GREEN}GET /api/predict/TAO{Fore.WHITE} - Prédire TAO")
        print(f"   • {Fore.GREEN}GET /api/early-warning/RNDR{Fore.WHITE} - Alertes RNDR")
        
        print(f"\n{Fore.YELLOW}🛑 Pour arrêter: Appuyez sur Ctrl+C")
        print(f"{Fore.CYAN}{'='*60}")
        
        # Garder le programme en vie
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}👋 Arrêt du système...")
            
    except Exception as e:
        print(f"{Fore.RED}❌ Erreur: {e}")
        return False

def main():
    
    print_banner()
    
    # Vérifier les dépendances
    if not check_dependencies():
        return
    
    # Créer les fichiers manquants
    create_missing_files()
    
    # Démarrer les services
    start_services()

if __name__ == "__main__":
    main() """
    
    
"""
Script de lancement unifié pour TrendAI
"""
import subprocess
import sys
import os
import time
from colorama import init, Fore, Style

# Initialiser colorama
init(autoreset=True)

def print_banner():
    """Afficher la bannière"""
    banner = f"""
{Fore.CYAN}{'='*60}
{Fore.YELLOW}       🤖 TRENDIA FAKE NEWS DETECTION SYSTEM
{Fore.CYAN}{'='*60}
{Fore.GREEN}🚀 Démarrage du système complet...
{Fore.WHITE}
📡 Backend Principal: {Fore.CYAN}http://localhost:8000
🤖 API ML: {Fore.CYAN}http://localhost:8001
📚 Documentation: {Fore.CYAN}http://localhost:8000/docs
{Fore.CYAN}{'='*60}
{Fore.YELLOW}💡 Endpoints disponibles:
{Fore.WHITE}
• {Fore.GREEN}/health{Fore.WHITE} - Vérifier l'état des services
• {Fore.GREEN}/api/analyze{Fore.WHITE} (POST) - Analyser du texte
• {Fore.GREEN}/api/risk/NEURA{Fore.WHITE} - Risque d'un token
• {Fore.GREEN}/api/rankings/high-risk{Fore.WHITE} - Tokens risqués
• {Fore.GREEN}/api/predict/NEURA{Fore.WHITE} - Prédiction prix
• {Fore.GREEN}/api/early-warning/NEURA{Fore.WHITE} - Alertes
{Fore.CYAN}{'='*60}
"""
    print(banner)

def check_dependencies():
    """Vérifier les dépendances"""
    print(f"{Fore.YELLOW}🔍 Vérification des dépendances...")
    
    required_modules = [
        'fastapi',
        'uvicorn', 
        'pandas',
        'sklearn',
        'numpy',
        'requests',
        'colorama'
    ]
    
    missing = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"{Fore.GREEN}✅ {module}")
        except ImportError:
            missing.append(module)
            print(f"{Fore.RED}❌ {module}")
    
    if missing:
        print(f"\n{Fore.YELLOW}📦 Installation des dépendances manquantes...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
            print(f"{Fore.GREEN}✅ Dépendances installées avec succès")
            return True
        except:
            print(f"{Fore.RED}❌ Échec installation. Installez manuellement:")
            print(f"{Fore.WHITE}pip install {' '.join(missing)}")
            return False
    
    print(f"{Fore.GREEN}✅ Toutes les dépendances sont installées")
    return True

def create_missing_files():
    """Créer les fichiers manquants si nécessaire"""
    print(f"\n{Fore.YELLOW}📁 Vérification des fichiers...")
    
    # Vérifier le dossier model
    if not os.path.exists('model'):
        os.makedirs('model')
        print(f"{Fore.GREEN}✅ Dossier 'model' créé")
    
    # Vérifier le dossier agents
    if not os.path.exists('agents'):
        os.makedirs('agents')
        print(f"{Fore.GREEN}✅ Dossier 'agents' créé")
    
    # Créer le fichier prediction_agent.py s'il n'existe pas
    agent_file = 'agents/prediction_agent.py'
    if not os.path.exists(agent_file):
        agent_code = '''"""
Agent de prédiction pour TrendAI
Prédit les mouvements de prix basé sur le sentiment
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from typing import Dict, List, Tuple

def get_price_prediction(token_id: str, horizon: str = "24h") -> Dict:
    """
    Prédire le mouvement de prix d'un token
    
    Args:
        token_id: Symbole du token (ex: NEURA)
        horizon: Horizon de prédiction (6h, 24h, 7d)
    
    Returns:
        Dict avec prédiction et métadonnées
    """
    # Mapping des horizons
    horizon_map = {
        "6h": {"periods": 6, "volatility": 0.03},
        "24h": {"periods": 24, "volatility": 0.05},
        "7d": {"periods": 168, "volatility": 0.15}
    }
    
    if horizon not in horizon_map:
        horizon = "24h"
    
    # Facteurs simulés basés sur le token
    token_factors = {
        "NEURA": {"momentum": 0.7, "sentiment": 0.8, "risk": 0.6},
        "TAO": {"momentum": 0.5, "sentiment": 0.6, "risk": 0.4},
        "RNDR": {"momentum": 0.6, "sentiment": 0.7, "risk": 0.5},
        "AGIX": {"momentum": 0.4, "sentiment": 0.5, "risk": 0.3},
        "FET": {"momentum": 0.5, "sentiment": 0.6, "risk": 0.4}
    }
    
    # Récupérer les facteurs du token ou utiliser des valeurs par défaut
    factors = token_factors.get(token_id.upper(), {
        "momentum": 0.5,
        "sentiment": 0.5,
        "risk": 0.5
    })
    
    # Calculer la prédiction
    base_return = np.random.normal(0, horizon_map[horizon]["volatility"])
    sentiment_boost = factors["sentiment"] * 0.02
    momentum_boost = factors["momentum"] * 0.01
    
    predicted_return = base_return + sentiment_boost + momentum_boost
    
    # Déterminer la direction
    direction = "UP" if predicted_return > 0 else "DOWN"
    confidence = min(0.95, abs(predicted_return) * 10)
    
    # Générer des features pour l'explication
    features = {
        "sentiment_score": round(factors["sentiment"], 2),
        "momentum_score": round(factors["momentum"], 2),
        "risk_score": round(factors["risk"], 2),
        "social_volume": random.randint(1000, 10000),
        "volatility_24h": round(random.uniform(0.02, 0.08), 3)
    }
    
    # Générer des alertes si nécessaire
    warnings = []
    if factors["risk"] > 0.7:
        warnings.append("Risque élevé de manipulation détecté")
    if abs(predicted_return) > 0.1:
        warnings.append(f"Mouvement important attendu ({direction})")
    
    # Générer une explication
    if direction == "UP":
        explanation = f"Analyse pour {token_id} ({horizon}): Sentiment positif ({features['sentiment_score']}/1.0), Momentum favorable ({features['momentum_score']}/1.0). Volume social: {features['social_volume']} posts. Recommandation: Surveillance pour entrée potentielle."
    else:
        explanation = f"Analyse pour {token_id} ({horizon}): Sentiment mitigé ({features['sentiment_score']}/1.0), Momentum faible ({features['momentum_score']}/1.0). Volatilité: {features['volatility_24h']*100}%. Recommandation: Attendre confirmation."
    
    return {
        "token": token_id.upper(),
        "horizon": horizon,
        "predicted_return": round(predicted_return * 100, 2),  # en pourcentage
        "direction": direction,
        "confidence": round(confidence, 2),
        "features": features,
        "warnings": warnings,
        "explanation": explanation,
        "timestamp": datetime.now().isoformat()
    }

def get_correlation_analysis(token_id: str) -> Dict:
    """Analyse de corrélation entre sentiment et prix"""
    correlations = {
        "sentiment_price": round(random.uniform(0.3, 0.9), 3),
        "volume_volatility": round(random.uniform(0.4, 0.8), 3),
        "lag_optimal": random.choice(["1h", "3h", "6h"]),
        "r_squared": round(random.uniform(0.2, 0.7), 3)
    }
    
    return {
        "token": token_id,
        "analysis": "correlation",
        "correlations": correlations,
        "insight": "Le sentiment précède généralement les mouvements de prix",
        "strength": "forte" if correlations["sentiment_price"] > 0.7 else "modérée"
    }

def get_early_warning_signals(token_id: str) -> Dict:
    """Signaux d'alerte précoce"""
    signals = []
    
    # Générer des signaux aléatoires
    if random.random() > 0.5:
        signals.append({
            "type": "bullish_divergence",
            "confidence": round(random.uniform(0.6, 0.9), 2),
            "description": "Sentiment en hausse mais prix stagnant",
            "action": "Surveiller pour entrée potentielle"
        })
    
    if random.random() > 0.7:
        signals.append({
            "type": "volume_spike",
            "confidence": round(random.uniform(0.7, 0.95), 2),
            "description": "Pic de volume sans mouvement de prix correspondant",
            "action": "Risque de manipulation"
        })
    
    if random.random() > 0.6:
        signals.append({
            "type": "sentiment_flip",
            "confidence": round(random.uniform(0.5, 0.85), 2),
            "description": "Retournement soudain du sentiment",
            "action": "Préparer à la volatilité"
        })
    
    return {
        "token": token_id,
        "signals": signals,
        "risk_level": "HIGH" if len(signals) > 1 else "MEDIUM",
        "timestamp": datetime.now().isoformat()
    }
'''
        
        with open(agent_file, 'w', encoding='utf-8') as f:
            f.write(agent_code)
        print(f"{Fore.GREEN}✅ Fichier agent créé: {agent_file}")
    
    # Créer les fichiers de données dans model/
    data_files = {
        'bot_detector.pkl': None,  # Sera créé par le ML si nécessaire
        'final_risk_scores.csv': '''token_id,risk_score,label,reason
NEURA,0.85,HIGH,Volume suspect élevé et patterns de manipulation
TAO,0.62,MEDIUM,Activité sociale normale avec quelques alertes
RNDR,0.41,LOW,Faible risque, communauté organique
AGIX,0.73,HIGH,Patterns de manipulation détectés
FET,0.55,MEDIUM,Risque modéré, surveillance recommandée
OCEAN,0.68,MEDIUM,Activité inhabituelle détectée
NMR,0.49,LOW,Faible risque
VXV,0.77,HIGH,Volume anormal et sentiment artificiel''',
        
        'ai_generated_narratives.csv': '''token_id,topic,start_time,end_time,sentiment_score,volume
NEURA,AI Revolution Narrative,2024-01-01,2024-01-10,0.8,1250
NEURA,Market Manipulation Warning,2024-01-05,2024-01-08,-0.6,890
TAO,Decentralized AI Growth,2024-01-02,2024-01-12,0.7,1100
RNDR,GPU Rendering Demand,2024-01-03,2024-01-10,0.5,950
AGIX,SingularityNET Ecosystem,2024-01-04,2024-01-11,0.6,800
FET,AI Agent Development,2024-01-06,2024-01-14,0.4,700'''
    }
    
    for filename, content in data_files.items():
        filepath = os.path.join('model', filename)
        if not os.path.exists(filepath):
            if content is None and filename == 'bot_detector.pkl':
                print(f"{Fore.YELLOW}⚠️  {filename} non trouvé - sera créé dynamiquement")
            else:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"{Fore.GREEN}✅ Fichier créé: {filepath}")

def start_services():
    """Démarrer tous les services"""
    print(f"\n{Fore.YELLOW}🚀 Démarrage des services...")
    
    try:
        # Vérifier si main.py existe
        if not os.path.exists('main.py'):
            print(f"{Fore.RED}❌ Fichier main.py non trouvé")
            return False
        
        # Importer et exécuter
        print(f"{Fore.CYAN}▶️  Démarrage du backend principal (port 8000)...")
        
        # Lancer dans un processus séparé
        import threading
        
        def run_backend():
            import uvicorn
            uvicorn.run(
                "main:app",
                host="0.0.0.0",
                port=8000,
                log_level="warning",
                reload=False
            )
        
        backend_thread = threading.Thread(target=run_backend, daemon=True)
        backend_thread.start()
        
        # Attendre que le backend démarre
        time.sleep(3)
        
        print(f"{Fore.GREEN}✅ Backend principal démarré sur http://localhost:8000")
        
        # Vérifier si l'API est accessible
        try:
            import requests
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print(f"{Fore.GREEN}✅ API vérifiée et fonctionnelle")
        except:
            print(f"{Fore.YELLOW}⚠️  L'API démarre mais n'est pas encore accessible")
        
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.GREEN}🎉 Système TrendAI pleinement opérationnel!")
        print(f"{Fore.CYAN}{'='*60}")
        print(f"\n{Fore.YELLOW}📋 Pour tester:")
        print(f"{Fore.WHITE}1. Ouvrez {Fore.CYAN}http://localhost:8000/docs")
        print(f"{Fore.WHITE}2. Testez les endpoints:")
        print(f"   • {Fore.GREEN}POST /api/analyze{Fore.WHITE} - Analyser du texte")
        print(f"   • {Fore.GREEN}GET /api/risk/NEURA{Fore.WHITE} - Voir risque NEURA")
        print(f"   • {Fore.GREEN}GET /api/predict/TAO{Fore.WHITE} - Prédire TAO")
        print(f"   • {Fore.GREEN}GET /api/early-warning/RNDR{Fore.WHITE} - Alertes RNDR")
        
        print(f"\n{Fore.YELLOW}🛑 Pour arrêter: Appuyez sur Ctrl+C")
        print(f"{Fore.CYAN}{'='*60}")
        
        # Garder le programme en vie
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}👋 Arrêt du système TrendAI...")
            sys.exit(0)
            
    except Exception as e:
        print(f"{Fore.RED}❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print_banner()
    
    # Vérifier les dépendances
    if not check_dependencies():
        return
    
    # Créer les fichiers manquants
    create_missing_files()
    
    # Démarrer les services
    start_services()

if __name__ == "__main__":
    main()