# scripts/import_data.py
import sys
import os
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import numpy as np

# Ajouter le répertoire parent au path
sys.path.append(str(Path(__file__).parent.parent))

from app.core.database import SessionLocal
from app.models.account import Account
from app.models.post import Post
from app.models.narrative import Narrative
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def import_csv_data():
    """Importe les données depuis les fichiers CSV"""
    db = SessionLocal()
    
    try:
        model_dir = "model"
        
        # 1. Importer les comptes
        accounts_csv = os.path.join(model_dir, "big_accounts.csv")
        if os.path.exists(accounts_csv):
            logger.info(f"📥 Importation des comptes depuis {accounts_csv}")
            
            df_accounts = pd.read_csv(accounts_csv)
            
            for _, row in df_accounts.iterrows():
                account = Account(
                    username=row.get('username', f"user_{_}"),
                    display_name=row.get('display_name', ''),
                    email=row.get('email', f"user{_}@example.com"),
                    followers_count=int(row.get('followers_count', 0)),
                    following_count=int(row.get('following_count', 0)),
                    tweet_count=int(row.get('tweet_count', 0)),
                    is_verified=bool(row.get('verified', False)),
                    is_bot=bool(row.get('is_bot', False)),
                    created_at=datetime.strptime(row.get('created_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M:%S') if 'created_at' in row and pd.notna(row['created_at']) else datetime.now() - timedelta(days=int(row.get('account_age_days', 365))),
                    location=row.get('location', '')
                )
                db.add(account)
            
            db.commit()
            logger.info(f"✅ {len(df_accounts)} comptes importés")
        
        # 2. Importer les posts
        posts_csv = os.path.join(model_dir, "big_posts.csv")
        if os.path.exists(posts_csv):
            logger.info(f"📥 Importation des posts depuis {posts_csv}")
            
            df_posts = pd.read_csv(posts_csv)
            accounts_in_db = {acc.username: acc.id for acc in db.query(Account).all()}
            
            posts_imported = 0
            for _, row in df_posts.iterrows():
                # Trouver l'ID du compte correspondant
                username = f"user_{row['account_id']:04d}" if 'account_id' in row else None
                account_id = accounts_in_db.get(username)
                
                if account_id:
                    post = Post(
                        account_id=account_id,
                        content=row.get('content', ''),
                        likes_count=int(row.get('likes_count', 0)),
                        retweets_count=int(row.get('retweets_count', 0)),
                        replies_count=int(row.get('replies_count', 0)),
                        created_at=datetime.strptime(row['created_at'], '%Y-%m-%d %H:%M:%S') if 'created_at' in row and pd.notna(row['created_at']) else datetime.now() - timedelta(hours=np.random.randint(0, 720)),
                        sentiment_score=float(row.get('sentiment_score', 0)),
                        language=row.get('language', 'en')
                    )
                    db.add(post)
                    posts_imported += 1
            
            db.commit()
            logger.info(f"✅ {posts_imported} posts importés")
        
        # 3. Importer les narratives
        narratives_csv = os.path.join(model_dir, "ai_generated_narratives.csv")
        if os.path.exists(narratives_csv):
            logger.info(f"📥 Importation des narratives depuis {narratives_csv}")
            
            df_narratives = pd.read_csv(narratives_csv)
            
            for _, row in df_narratives.iterrows():
                narrative = Narrative(
                    name=row.get('name', ''),
                    description=row.get('description', ''),
                    keywords=row.get('keywords', ''),
                    post_count=int(row.get('post_count', 0)),
                    account_count=int(row.get('account_count', 0)),
                    confidence_score=float(row.get('confidence_score', 0)),
                    risk_level=row.get('risk_level', 'low'),
                    detected_at=datetime.strptime(row['detected_at'], '%Y-%m-%d') if 'detected_at' in row and pd.notna(row['detected_at']) else datetime.now() - timedelta(days=np.random.randint(1, 60))
                )
                db.add(narrative)
            
            db.commit()
            logger.info(f"✅ {len(df_narratives)} narratives importées")
        
        # Afficher les statistiques finales
        total_accounts = db.query(Account).count()
        total_posts = db.query(Post).count()
        total_narratives = db.query(Narrative).count()
        
        logger.info("\n📊 STATISTIQUES FINALES:")
        logger.info(f"   Comptes: {total_accounts}")
        logger.info(f"   Posts: {total_posts}")
        logger.info(f"   Narratives: {total_narratives}")
        
    except Exception as e:
        logger.error(f"❌ Erreur import données: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import_csv_data()