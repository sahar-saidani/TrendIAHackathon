""" import os
from dotenv import load_dotenv

load_dotenv()

# Example: postgresql://postgres:postgres@localhost:5432/trendai
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/trendai"
)

# other configs
APP_NAME = os.getenv("APP_NAME", "TrendAI Watchdog Backend")
"""
import os
from dotenv import load_dotenv
from pathlib import Path

# Charger les variables d'environnement
load_dotenv()

# Chemins
BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_DIR = BASE_DIR / "model"

# Configuration de la base de données
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/trendai"
)

# Fichiers ML
ML_MODEL_PATH = MODEL_DIR / "bot_detector.pkl"
RISK_SCORES_PATH = MODEL_DIR / "final_risk_scores.csv"
NARRATIVES_PATH = MODEL_DIR / "ai_generated_narratives.csv"

# Configuration de l'application
APP_NAME = os.getenv("APP_NAME", "TrendAI Watchdog Backend")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# Vérifier l'existence des fichiers ML
def check_ml_files():
    """Vérifie que les fichiers ML nécessaires existent"""
    missing_files = []
    
    if not ML_MODEL_PATH.exists():
        missing_files.append("bot_detector.pkl")
    
    if not RISK_SCORES_PATH.exists():
        missing_files.append("final_risk_scores.csv")
    
    if not NARRATIVES_PATH.exists():
        missing_files.append("ai_generated_narratives.csv")
    
    if missing_files:
        print(f"⚠️ Fichiers ML manquants: {missing_files}")
        print(f"   Chemin modèle: {MODEL_DIR}")
    
    return len(missing_files) == 0

# Vérifier au démarrage
ML_FILES_OK = check_ml_files()