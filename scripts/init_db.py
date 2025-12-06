# scripts/init_db.py
import sys
import os
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.append(str(Path(__file__).parent.parent))

from app.core.database import engine, Base
from app.models import Account, Post, Narrative
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    """Initialise la base de données"""
    print("🗄️  Initialisation de la base de données...")
    
    try:
        # Créer toutes les tables
        Base.metadata.create_all(bind=engine)
        
        logger.info("✅ Tables créées avec succès!")
        
        # Vérifier
        from sqlalchemy import inspect
        inspector = inspect(engine)
        
        print("\n📋 Tables dans la base de données:")
        for table_name in inspector.get_table_names():
            columns = inspector.get_columns(table_name)
            print(f"  - {table_name} ({len(columns)} colonnes)")
            for col in columns[:3]:  # Afficher les 3 premières colonnes
                print(f"    * {col['name']} ({col['type']})")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur initialisation DB: {e}")
        return False

if __name__ == "__main__":
    init_database()