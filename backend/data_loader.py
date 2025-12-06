""" 
Data Loader Script
Loads CSV data into Supabase database
Run this once to populate the database with initial data


import pandas as pd
import os
import sys

def load_data_to_supabase():
    

    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

    if not supabase_url or not supabase_key:
        print("Error: Supabase credentials not found in environment")
        sys.exit(1)

    supabase = create_client(supabase_url, supabase_key)
    print("Connected to Supabase")

    print("\n1. Loading Posts Data...")
    try:
        posts_df = pd.read_csv('big_posts_enriched.csv')
        print(f"   Found {len(posts_df)} posts")

        posts_data = []
        for _, row in posts_df.iterrows():
            posts_data.append({
                'post_id': str(row.get('post_id', '')),
                'token_id': str(row.get('token_id', '')).upper(),
                'text': str(row.get('text', '')),
                'post_type': str(row.get('type', 'organic')),
                'is_bot': bool(row.get('is_bot', 0) == 1),
                'sentiment_score': float(row.get('sentiment_score', 0)),
                'sentiment_label': str(row.get('sentiment_label', 'Neutral'))
            })

        batch_size = 100
        for i in range(0, len(posts_data), batch_size):
            batch = posts_data[i:i+batch_size]
            supabase.table('posts').upsert(batch).execute()
            print(f"   Loaded {min(i+batch_size, len(posts_data))}/{len(posts_data)} posts")

        print("   Posts data loaded successfully")
    except FileNotFoundError:
        print("   Warning: big_posts_enriched.csv not found, skipping")
    except Exception as e:
        print(f"   Error loading posts: {e}")

    print("\n2. Loading Token Risk Scores...")
    try:
        risk_df = pd.read_csv('final_risk_scores.csv')
        print(f"   Found {len(risk_df)} tokens")

        tokens_data = []
        for _, row in risk_df.iterrows():
            tokens_data.append({
                'token_id': str(row.get('token_id', '')).upper(),
                'risk_score': float(row.get('risk_score', 0)),
                'risk_label': str(row.get('label', 'SAFE')),
                'bot_ratio': float(row.get('bot_ratio', 0)),
                'avg_sentiment': float(row.get('avg_sentiment', 0)),
                'total_posts': int(row.get('total_posts', 0)),
                'suspicious_posts': int(row.get('suspicious_posts', 0)),
                'reason': str(row.get('reason', ''))
            })

        for token in tokens_data:
            supabase.table('tokens').upsert(token).execute()

        print(f"   Loaded {len(tokens_data)} tokens")
    except FileNotFoundError:
        print("   Warning: final_risk_scores.csv not found, skipping")
    except Exception as e:
        print(f"   Error loading tokens: {e}")

    print("\n3. Loading Narrative Risk Data...")
    try:
        narratives_df = pd.read_csv('final_narrative_risk.csv')
        print(f"   Found {len(narratives_df)} narratives")

        narratives_data = []
        for _, row in narratives_df.iterrows():
            narratives_data.append({
                'narrative_id': str(row.get('narrative_id', '')),
                'token_id': str(row.get('token_id', '')).upper(),
                'topic': str(row.get('topic', '')),
                'risk_level': str(row.get('risk_level', 'LOW')),
                'bot_percentage': float(row.get('bot_percentage', 0)),
                'avg_sentiment': float(row.get('avg_sentiment', 0)),
                'warning': str(row.get('warning', '')),
                'post_count': 0
            })

        for narrative in narratives_data:
            supabase.table('narratives').insert(narrative).execute()

        print(f"   Loaded {len(narratives_data)} narratives")
    except FileNotFoundError:
        print("   Warning: final_narrative_risk.csv not found, skipping")
    except Exception as e:
        print(f"   Error loading narratives: {e}")

    print("\n4. Loading Account Trust Data...")
    try:
        trust_df = pd.read_csv('final_account_trust.csv')
        print(f"   Found {len(trust_df)} accounts")

        accounts_data = []
        for _, row in trust_df.iterrows():
            accounts_data.append({
                'account_id': str(row.get('account_id', '')),
                'username': str(row.get('username', 'unknown')),
                'trust_score': float(row.get('trust_score', 50)),
                'trust_label': str(row.get('trust_label', 'NEUTRAL')),
                'bot_ratio': float(row.get('bot_ratio', 0)),
                'total_posts': int(row.get('total_posts', 0))
            })

        for account in accounts_data:
            supabase.table('accounts').upsert(account).execute()

        print(f"   Loaded {len(accounts_data)} accounts")
    except FileNotFoundError:
        print("   Warning: final_account_trust.csv not found, skipping")
    except Exception as e:
        print(f"   Error loading accounts: {e}")

    print("\n" + "="*50)
    print("DATA LOADING COMPLETE")
    print("="*50)

    stats_response = supabase.table('tokens').select('*', count='exact').execute()
    print(f"\nDatabase now contains:")
    print(f"  - {stats_response.count} tokens")

    posts_response = supabase.table('posts').select('*', count='exact').execute()
    print(f"  - {posts_response.count} posts")

    print("\nYou can now start the API server!")
    if __name__ == "__main__":
    load_data_to_supabase()
"""

"""
Data Loader Script
Loads CSV data into Local Postgres database
Run this once to populate the database with initial data
"""

""" import pandas as pd
from sqlalchemy import create_engine, func, Column, Float, Integer, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
import os
import sys

# Models for the tables (duplicated for standalone script)
Base = declarative_base()

class Post(Base):
    __tablename__ = 'posts'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    post_id = Column(String, nullable=False)
    token_id = Column(String, nullable=False)
    text = Column(String, nullable=False)
    post_type = Column(String, default='organic')
    is_bot = Column(Boolean, default=False)
    sentiment_score = Column(Float, default=0)
    sentiment_label = Column(String, default='Neutral')
    created_at = Column(DateTime, server_default=func.now())

class Token(Base):
    __tablename__ = 'tokens'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token_id = Column(String, unique=True, nullable=False)
    name = Column(String)
    risk_score = Column(Float, default=0)
    risk_label = Column(String, default='SAFE')
    bot_ratio = Column(Float, default=0)
    avg_sentiment = Column(Float, default=0)
    total_posts = Column(Integer, default=0)
    suspicious_posts = Column(Integer, default=0)
    reason = Column(String, default='')
    last_analyzed = Column(DateTime, server_default=func.now())

class Narrative(Base):
    __tablename__ = 'narratives'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    narrative_id = Column(String, nullable=False)
    token_id = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    risk_level = Column(String, default='LOW')
    bot_percentage = Column(Float, default=0)
    avg_sentiment = Column(Float, default=0)
    warning = Column(String, default='')
    post_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())

class Account(Base):
    __tablename__ = 'accounts'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=False)
    trust_score = Column(Float, default=50)
    trust_label = Column(String, default='NEUTRAL')
    bot_ratio = Column(Float, default=0)
    total_posts = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())

# Chaîne de connexion
DATABASE_URL = "postgresql://postgres:votre_mot_de_passe@localhost:5432/trendai"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def load_data_to_postgres():
   
    db: Session = SessionLocal()
    try:
        print("\n1. Loading Posts Data...")
        try:
            posts_df = pd.read_csv('big_posts_enriched.csv')
            print(f"   Found {len(posts_df)} posts")

            batch_size = 100
            for i in range(0, len(posts_df), batch_size):
                batch = posts_df.iloc[i:i+batch_size]
                for _, row in batch.iterrows():
                    post = Post(
                        post_id=str(row.get('post_id', '')),
                        token_id=str(row.get('token_id', '')).upper(),
                        text=str(row.get('text', '')),
                        post_type=str(row.get('type', 'organic')),
                        is_bot=bool(row.get('is_bot', 0) == 1),
                        sentiment_score=float(row.get('sentiment_score', 0)),
                        sentiment_label=str(row.get('sentiment_label', 'Neutral'))
                    )
                    db.merge(post)
                db.commit()
                print(f"   Loaded {min(i+batch_size, len(posts_df))}/{len(posts_df)} posts")

            print("   Posts data loaded successfully")
        except FileNotFoundError:
            print("   Warning: big_posts_enriched.csv not found, skipping")
        except Exception as e:
            print(f"   Error loading posts: {e}")

        print("\n2. Loading Token Risk Scores...")
        try:
            risk_df = pd.read_csv('final_risk_scores.csv')
            print(f"   Found {len(risk_df)} tokens")

            for _, row in risk_df.iterrows():
                token = Token(
                    token_id=str(row.get('token_id', '')).upper(),
                    risk_score=float(row.get('risk_score', 0)),
                    risk_label=str(row.get('label', 'SAFE')),
                    bot_ratio=float(row.get('bot_ratio', 0)),
                    avg_sentiment=float(row.get('avg_sentiment', 0)),
                    total_posts=int(row.get('total_posts', 0)),
                    suspicious_posts=int(row.get('suspicious_posts', 0)),
                    reason=str(row.get('reason', ''))
                )
                db.merge(token)
            db.commit()
            print("   Tokens data loaded successfully")
        except FileNotFoundError:
            print("   Warning: final_risk_scores.csv not found, skipping")
        except Exception as e:
            print(f"   Error loading tokens: {e}")

        print("\n3. Loading Narrative Risk Data...")
        try:
            narratives_df = pd.read_csv('final_narrative_risk.csv')
            print(f"   Found {len(narratives_df)} narratives")

            for _, row in narratives_df.iterrows():
                narrative = Narrative(
                    narrative_id=str(row.get('narrative_id', '')),
                    token_id=str(row.get('token_id', '')).upper(),
                    topic=str(row.get('topic', '')),
                    risk_level=str(row.get('risk_level', 'LOW')),
                    bot_percentage=float(row.get('bot_percentage', 0)),
                    avg_sentiment=float(row.get('avg_sentiment', 0)),
                    warning=str(row.get('warning', '')),
                    post_count=0
                )
                db.merge(narrative)
            db.commit()
            print("   Narratives data loaded successfully")
        except FileNotFoundError:
            print("   Warning: final_narrative_risk.csv not found, skipping")
        except Exception as e:
            print(f"   Error loading narratives: {e}")

        print("\n4. Loading Account Trust Data...")
        try:
            trust_df = pd.read_csv('final_account_trust.csv')
            print(f"   Found {len(trust_df)} accounts")

            for _, row in trust_df.iterrows():
                account = Account(
                    account_id=str(row.get('account_id', '')),
                    username=str(row.get('username', 'unknown')),
                    trust_score=float(row.get('trust_score', 50)),
                    trust_label=str(row.get('trust_label', 'NEUTRAL')),
                    bot_ratio=float(row.get('bot_ratio', 0)),
                    total_posts=int(row.get('total_posts', 0))
                )
                db.merge(account)
            db.commit()
            print("   Accounts data loaded successfully")
        except FileNotFoundError:
            print("   Warning: final_account_trust.csv not found, skipping")
        except Exception as e:
            print(f"   Error loading accounts: {e}")

        print("\n" + "="*50)
        print("DATA LOADING COMPLETE")
        print("="*50)

        # Stats pour vérification
        total_tokens = db.query(func.count(Token.id)).scalar() or 0
        total_posts = db.query(func.count(Post.id)).scalar() or 0
        print(f"\nDatabase now contains:")
        print(f"  - {total_tokens} tokens")
        print(f"  - {total_posts} posts")

    except Exception as e:
        db.rollback()
        print(f"Global error: {e}")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    load_data_to_postgres() """
    
import pandas as pd
from sqlalchemy import create_engine, func, Column, Float, Integer, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
import os
import sys

# ========================================
# CONFIG
# ========================================
DATABASE_URL = "postgresql://postgres:admin123@localhost:5432/trendai"  # Change ton mot de passe ici
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ========================================
# MODÈLES (identiques à integrated_api.py)
# ========================================
class Post(Base):
    __tablename__ = 'posts'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    post_id = Column(String, nullable=False)
    token_id = Column(String, nullable=False)
    text = Column(String, nullable=False)
    post_type = Column(String, default='organic')
    is_bot = Column(Boolean, default=False)
    sentiment_score = Column(Float, default=0)
    sentiment_label = Column(String, default='Neutral')
    created_at = Column(DateTime, server_default=func.now())

class Token(Base):
    __tablename__ = 'tokens'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token_id = Column(String, unique=True, nullable=False)
    name = Column(String)  # ← Obligatoire
    risk_score = Column(Float, default=0)
    risk_label = Column(String, default='SAFE')
    bot_ratio = Column(Float, default=0)
    avg_sentiment = Column(Float, default=0)
    total_posts = Column(Integer, default=0)
    suspicious_posts = Column(Integer, default=0)
    reason = Column(String, default='')

class Narrative(Base):
    __tablename__ = 'narratives'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    narrative_id = Column(String, nullable=False)
    token_id = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    risk_level = Column(String, default='LOW')
    bot_percentage = Column(Float, default=0)
    avg_sentiment = Column(Float, default=0)
    warning = Column(String, default='')
    post_count = Column(Integer, default=0)

class Account(Base):
    __tablename__ = 'accounts'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=False)
    trust_score = Column(Float, default=50)
    trust_label = Column(String, default='NEUTRAL')
    bot_ratio = Column(Float, default=0)
    total_posts = Column(Integer, default=0)

# ========================================
# CHARGEMENT DES DONNÉES
# ========================================
def load_data_to_postgres():
    db = SessionLocal()
    try:
        print("Démarrage du chargement des données...")

        # 1. TOKENS (CORRIGÉ : on force token_id en majuscule + name)
        try:
            df = pd.read_csv('final_risk_scores.csv')
            print(f"Chargement de {len(df)} tokens...")
            for _, row in df.iterrows():
                token = Token(
                    token_id=str(row['token_id']).upper(),  # ← FORCÉ EN MAJUSCULE
                    name=str(row['token_id']).upper(),       # ← name = token_id si pas de colonne name
                    risk_score=float(row.get('risk_score', 0)),
                    risk_label=str(row.get('label', 'SAFE')),
                    bot_ratio=float(row.get('bot_ratio', 0)),
                    avg_sentiment=float(row.get('avg_sentiment', 0)),
                    total_posts=int(row.get('total_posts', 0)),
                    suspicious_posts=int(row.get('suspicious_posts', 0)),
                    reason=str(row.get('reason', ''))
                )
                db.merge(token)
            db.commit()
            print("Tokens chargés avec succès")
        except Exception as e:
            print(f"Erreur tokens : {e}")

        # 2. POSTS
        try:
            df = pd.read_csv('big_posts_enriched.csv')
            print(f"Chargement de {len(df)} posts...")
            for _, row in df.iterrows():
                post = Post(
                    post_id=str(row.get('post_id', '')),
                    token_id=str(row.get('token_id', '')).upper(),
                    text=str(row.get('text', '')),
                    post_type=str(row.get('type', 'organic')),
                    is_bot=bool(row.get('is_bot', 0) == 1),
                    sentiment_score=float(row.get('sentiment_score', 0)),
                    sentiment_label=str(row.get('sentiment_label', 'Neutral'))
                )
                db.merge(post)
            db.commit()
            print("Posts chargés")
        except Exception as e:
            print(f"Erreur posts : {e}")

        # 3. NARRATIVES
        try:
            df = pd.read_csv('final_narrative_risk.csv')
            print(f"Chargement de {len(df)} narratives...")
            for _, row in df.iterrows():
                nar = Narrative(
                    narrative_id=str(row.get('narrative_id', '')),
                    token_id=str(row.get('token_id', '')).upper(),
                    topic=str(row.get('topic', '')),
                    risk_level=str(row.get('risk_level', 'LOW')),
                    bot_percentage=float(row.get('bot_percentage', 0)),
                    avg_sentiment=float(row.get('avg_sentiment', 0)),
                    warning=str(row.get('warning', '')),
                    post_count=0
                )
                db.merge(nar)
            db.commit()
            print("Narratives chargées")
        except Exception as e:
            print(f"Erreur narratives : {e}")

        # 4. ACCOUNTS (optionnel)
        try:
            df = pd.read_csv('final_account_trust.csv')
            for _, row in df.iterrows():
                acc = Account(
                    account_id=str(row.get('account_id', '')),
                    username=str(row.get('username', 'unknown')),
                    trust_score=float(row.get('trust_score', 50)),
                    trust_label=str(row.get('trust_label', 'NEUTRAL')),
                    bot_ratio=float(row.get('bot_ratio', 0)),
                    total_posts=int(row.get('total_posts', 0))
                )
                db.merge(acc)
            db.commit()
            print("Accounts chargés")
        except Exception as e:
            print("Erreur accounts (ignoré)")

        print("\n" + "="*60)
        print("TOUTES LES DONNÉES SONT CHARGÉES DANS POSTGRESQL !")
        print("="*60)
        print("Tu peux maintenant faire : curl http://localhost:8000/analyze/token/NEURA")

    except Exception as e:
        db.rollback()
        print(f"ERREUR FATALE : {e}")
    finally:
        db.close()

if __name__ == "__main__":
    load_data_to_postgres()