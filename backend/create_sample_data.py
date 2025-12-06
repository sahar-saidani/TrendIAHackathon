"""
Sample Data Generator
Creates test data to demonstrate TrendAI functionality
"""

""" from supabase import create_client
import os

def create_sample_data():

    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

    if not supabase_url or not supabase_key:
        print("Error: Supabase credentials not found")
        return

    supabase = create_client(supabase_url, supabase_key)
    print("Connected to Supabase\n")

    print("Creating sample tokens...")

    sample_tokens = [
        {
            'token_id': 'SAFEMOON',
            'name': 'SafeMoon',
            'risk_score': 85.5,
            'risk_label': 'PUMP & DUMP',
            'bot_ratio': 72.3,
            'avg_sentiment': 0.85,
            'total_posts': 1250,
            'suspicious_posts': 903,
            'reason': 'Coordinated High-Hype Bot Attack (72.3% bots).'
        },
        {
            'token_id': 'SCAMCOIN',
            'name': 'ScamCoin',
            'risk_score': 95.2,
            'risk_label': 'HIGH RISK',
            'bot_ratio': 88.1,
            'avg_sentiment': 0.92,
            'total_posts': 890,
            'suspicious_posts': 784,
            'reason': 'Critical levels of non-human activity detected.'
        },
        {
            'token_id': 'BTC',
            'name': 'Bitcoin',
            'risk_score': 12.5,
            'risk_label': 'SAFE',
            'bot_ratio': 12.5,
            'avg_sentiment': 0.15,
            'total_posts': 5000,
            'suspicious_posts': 625,
            'reason': 'Community sentiment appears organic.'
        },
        {
            'token_id': 'ETH',
            'name': 'Ethereum',
            'risk_score': 15.2,
            'risk_label': 'SAFE',
            'bot_ratio': 15.2,
            'avg_sentiment': 0.22,
            'total_posts': 4500,
            'suspicious_posts': 684,
            'reason': 'Community sentiment appears organic.'
        },
        {
            'token_id': 'SUSPICOUS',
            'name': 'SuspiciousToken',
            'risk_score': 45.8,
            'risk_label': 'SUSPICIOUS',
            'bot_ratio': 38.2,
            'avg_sentiment': 0.65,
            'total_posts': 750,
            'suspicious_posts': 287,
            'reason': 'Moderate manipulation signs observed (45.8%).'
        }
    ]

    for token in sample_tokens:
        try:
            supabase.table('tokens').upsert(token).execute()
            print(f"  Added {token['token_id']} - {token['risk_label']}")
        except Exception as e:
            print(f"  Error adding {token['token_id']}: {e}")

    print("\nCreating sample narratives...")

    sample_narratives = [
        {
            'narrative_id': 'N001',
            'token_id': 'SAFEMOON',
            'topic': 'Moon mission guaranteed returns',
            'risk_level': 'CRITICAL',
            'bot_percentage': 85.2,
            'avg_sentiment': 0.92,
            'warning': 'Artificial Hype / Bull Trap',
            'post_count': 450
        },
        {
            'narrative_id': 'N002',
            'token_id': 'SAFEMOON',
            'topic': 'Exchange listing rumors',
            'risk_level': 'HIGH',
            'bot_percentage': 68.5,
            'avg_sentiment': 0.88,
            'warning': 'Heavily Manipulated (Bot Army)',
            'post_count': 320
        },
        {
            'narrative_id': 'N003',
            'token_id': 'BTC',
            'topic': 'Technical analysis and market trends',
            'risk_level': 'LOW',
            'bot_percentage': 12.3,
            'avg_sentiment': 0.25,
            'warning': 'Organic conversation',
            'post_count': 1200
        }
    ]

    for narrative in sample_narratives:
        try:
            supabase.table('narratives').insert(narrative).execute()
            print(f"  Added narrative: {narrative['topic']}")
        except Exception as e:
            print(f"  Error adding narrative: {e}")

    print("\nCreating sample posts...")

    sample_posts = [
        {
            'post_id': 'P001',
            'token_id': 'SAFEMOON',
            'text': 'TO THE MOON!!! BUY NOW BEFORE ITS TOO LATE!!! 1000X GUARANTEED!!!',
            'post_type': 'bot',
            'is_bot': True,
            'sentiment_score': 0.95,
            'sentiment_label': 'Positive'
        },
        {
            'post_id': 'P002',
            'token_id': 'SAFEMOON',
            'text': 'HUGE ANNOUNCEMENT COMING! GET IN NOW! DONT MISS OUT!!!',
            'post_type': 'bot',
            'is_bot': True,
            'sentiment_score': 0.92,
            'sentiment_label': 'Positive'
        },
        {
            'post_id': 'P003',
            'token_id': 'BTC',
            'text': 'Interesting technical analysis on Bitcoin. Looking at the weekly chart, we might see support around 40k.',
            'post_type': 'organic',
            'is_bot': False,
            'sentiment_score': 0.15,
            'sentiment_label': 'Neutral'
        },
        {
            'post_id': 'P004',
            'token_id': 'ETH',
            'text': 'The upcoming Ethereum upgrade could improve transaction speeds significantly. Worth researching.',
            'post_type': 'organic',
            'is_bot': False,
            'sentiment_score': 0.35,
            'sentiment_label': 'Positive'
        },
        {
            'post_id': 'P005',
            'token_id': 'SCAMCOIN',
            'text': 'LAST CHANCE!!! PRICE EXPLOSION INCOMING!!! BUY BUY BUY!!!',
            'post_type': 'bot',
            'is_bot': True,
            'sentiment_score': 0.98,
            'sentiment_label': 'Positive'
        }
    ]

    for post in sample_posts:
        try:
            supabase.table('posts').upsert(post).execute()
            print(f"  Added post: {post['post_id']}")
        except Exception as e:
            print(f"  Error adding post: {e}")

    print("\n" + "="*50)
    print("SAMPLE DATA CREATED SUCCESSFULLY")
    print("="*50)
    print("\nYou can now:")
    print("1. Start the API: python backend/integrated_api.py")
    print("2. Start the frontend: npm run dev")
    print("3. Try analyzing tokens: SAFEMOON, BTC, ETH, SCAMCOIN")
    print("\nNote: These are demo tokens for testing purposes.")

if __name__ == "__main__":
    create_sample_data()
 """
 
 
"""
Sample Data Generator
Creates test data to demonstrate TrendAI functionality
"""

from sqlalchemy import create_engine, func, Column, Float, Integer, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
import os

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

# Chaîne de connexion
DATABASE_URL = "postgresql://postgres:votre_mot_de_passe@localhost:5432/trendai"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_sample_data():
    """Create sample data for demonstration"""
    db = SessionLocal()
    try:
        print("Connected to Local Postgres\n")

        print("Creating sample tokens...")

        sample_tokens = [
            {
                'token_id': 'SAFEMOON',
                'name': 'SafeMoon',
                'risk_score': 85.5,
                'risk_label': 'PUMP & DUMP',
                'bot_ratio': 72.3,
                'avg_sentiment': 0.85,
                'total_posts': 1250,
                'suspicious_posts': 903,
                'reason': 'Coordinated High-Hype Bot Attack (72.3% bots).'
            },
            {
                'token_id': 'SCAMCOIN',
                'name': 'ScamCoin',
                'risk_score': 95.2,
                'risk_label': 'HIGH RISK',
                'bot_ratio': 88.1,
                'avg_sentiment': 0.92,
                'total_posts': 890,
                'suspicious_posts': 784,
                'reason': 'Critical levels of non-human activity detected.'
            },
            {
                'token_id': 'BTC',
                'name': 'Bitcoin',
                'risk_score': 12.5,
                'risk_label': 'SAFE',
                'bot_ratio': 12.5,
                'avg_sentiment': 0.15,
                'total_posts': 5000,
                'suspicious_posts': 625,
                'reason': 'Community sentiment appears organic.'
            },
            {
                'token_id': 'ETH',
                'name': 'Ethereum',
                'risk_score': 15.2,
                'risk_label': 'SAFE',
                'bot_ratio': 15.2,
                'avg_sentiment': 0.22,
                'total_posts': 4500,
                'suspicious_posts': 684,
                'reason': 'Community sentiment appears organic.'
            },
            {
                'token_id': 'SUSPICOUS',
                'name': 'SuspiciousToken',
                'risk_score': 45.8,
                'risk_label': 'SUSPICIOUS',
                'bot_ratio': 45.8,
                'avg_sentiment': 0.45,
                'total_posts': 1000,
                'suspicious_posts': 458,
                'reason': 'Moderate manipulation signs observed.'
            }
        ]

        for token_data in sample_tokens:
            token = Token(**token_data)
            db.merge(token)
            print(f"  Added token: {token_data['token_id']}")

        print("\nCreating sample posts...")

        sample_posts = [
            {
                'post_id': 'P001',
                'token_id': 'SAFEMOON',
                'text': 'BUY SAFEMOON BEFORE ITS TOO LATE!!! 1000X GUARANTEED!!!',
                'post_type': 'bot',
                'is_bot': True,
                'sentiment_score': 0.95,
                'sentiment_label': 'Positive'
            },
            {
                'post_id': 'P002',
                'token_id': 'SAFEMOON',
                'text': 'HUGE ANNOUNCEMENT COMING! GET IN NOW! DONT MISS OUT!!!',
                'post_type': 'bot',
                'is_bot': True,
                'sentiment_score': 0.92,
                'sentiment_label': 'Positive'
            },
            {
                'post_id': 'P003',
                'token_id': 'BTC',
                'text': 'Interesting technical analysis on Bitcoin. Looking at the weekly chart, we might see support around 40k.',
                'post_type': 'organic',
                'is_bot': False,
                'sentiment_score': 0.15,
                'sentiment_label': 'Neutral'
            },
            {
                'post_id': 'P004',
                'token_id': 'ETH',
                'text': 'The upcoming Ethereum upgrade could improve transaction speeds significantly. Worth researching.',
                'post_type': 'organic',
                'is_bot': False,
                'sentiment_score': 0.35,
                'sentiment_label': 'Positive'
            },
            {
                'post_id': 'P005',
                'token_id': 'SCAMCOIN',
                'text': 'LAST CHANCE!!! PRICE EXPLOSION INCOMING!!! BUY BUY BUY!!!',
                'post_type': 'bot',
                'is_bot': True,
                'sentiment_score': 0.98,
                'sentiment_label': 'Positive'
            }
        ]

        for post_data in sample_posts:
            post = Post(**post_data)
            db.merge(post)
            print(f"  Added post: {post_data['post_id']}")

        db.commit()
        print("\n" + "="*50)
        print("SAMPLE DATA CREATED SUCCESSFULLY")
        print("="*50)
        print("\nYou can now:")
        print("1. Start the API: python backend/integrated_api.py")
        print("2. Start the frontend: npm run dev")
        print("3. Try analyzing tokens: SAFEMOON, BTC, ETH, SCAMCOIN")
        print("\nNote: These are demo tokens for testing purposes.")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()