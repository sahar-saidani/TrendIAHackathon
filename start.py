"""
Script simplifié pour démarrer TrendAI
"""
import os
import sys
import subprocess
import time

def main():
    print("="*60)
    print("       🤖 TRENDIA FAKE NEWS DETECTION SYSTEM")
    print("="*60)
    
    # Vérifier et installer les dépendances
    print("\n📦 Vérification des dépendances...")
    requirements = [
        "fastapi", "uvicorn", "pandas", "scikit-learn", 
        "numpy", "requests", "colorama", "schedule"
    ]
    
    for req in requirements:
        try:
            __import__(req)
            print(f"✅ {req}")
        except ImportError:
            print(f"⬇️ Installation de {req}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", req])
    
    # Créer la structure
    print("\n🔧 Configuration de la structure...")
    for folder in ['model', 'agents']:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"✅ Dossier créé: {folder}")
    
    # Créer le fichier agent s'il n'existe pas
    agent_file = 'agents/prediction_agent.py'
    if not os.path.exists(agent_file):
        agent_code = '''"""
Agent de prédiction pour TrendAI
"""
import numpy as np
import random
from datetime import datetime

def get_price_prediction(token_id, horizon="24h"):
    """Prédiction de prix simplifiée"""
    token = token_id.upper()
    return_percent = round(np.random.uniform(-10, 10), 2)
    
    return {
        "token": token,
        "horizon": horizon,
        "predicted_return": return_percent,
        "direction": "UP" if return_percent > 0 else "DOWN",
        "confidence": round(random.uniform(0.5, 0.9), 2),
        "timestamp": datetime.now().isoformat()
    }

def get_early_warning_signals(token_id):
    """Alertes simplifiées"""
    return {
        "token": token_id.upper(),
        "signals": [{
            "type": "test_signal",
            "description": "Système opérationnel"
        }],
        "risk_level": "LOW"
    }
'''
        with open(agent_file, 'w') as f:
            f.write(agent_code)
        print(f"✅ Fichier agent créé: {agent_file}")
    
    # Créer __init__.py pour agents
    init_file = 'agents/__init__.py'
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            f.write('''from .prediction_agent import get_price_prediction, get_early_warning_signals
__all__ = ['get_price_prediction', 'get_early_warning_signals']''')
        print(f"✅ Fichier __init__.py créé")
    
    # Créer des données factices dans model/
    data_files = {
        'final_risk_scores.csv': '''token_id,risk_score,label,reason
NEURA,0.85,HIGH,Volume suspect
TAO,0.62,MEDIUM,Risque modéré
RNDR,0.41,LOW,Faible risque''',
        'ai_generated_narratives.csv': '''token_id,topic
NEURA,AI Narrative
TAO,Decentralized AI'''
    }
    
    for filename, content in data_files.items():
        filepath = os.path.join('model', filename)
        if not os.path.exists(filepath):
            with open(filepath, 'w') as f:
                f.write(content)
            print(f"✅ Fichier créé: {filepath}")
    
    # Démarrer l'application
    print("\n🚀 Démarrage de TrendAI...")
    print("🌐 Accédez à: http://localhost:8000/docs")
    print("⏳ Démarrage en cours...")
    
    # Importer et lancer
    import uvicorn
    from main import app
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )

if __name__ == "__main__":
    main()