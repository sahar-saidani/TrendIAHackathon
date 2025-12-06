# scripts/create_missing_files.py
import pickle
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def create_ml_model():
    """Crée un modèle ML entraîné pour détecter les bots"""
    print("🤖 Création du modèle de détection de bots...")
    
    # Générer des données d'entraînement simulées
    np.random.seed(42)
    n_samples = 1000
    
    # Features simulées pour des comptes
    # [followers_ratio, tweet_frequency, account_age, verified, engagement]
    X = np.random.randn(n_samples, 5)
    
    # Labels : 1 pour bot, 0 pour humain (20% de bots)
    y = np.zeros(n_samples)
    bot_indices = np.random.choice(n_samples, size=int(n_samples * 0.2), replace=False)
    y[bot_indices] = 1
    
    # Ajouter des patterns pour les bots
    # Les bots ont généralement plus de followers ratio et tweet plus fréquemment
    X[bot_indices, 0] += 1.5  # followers_ratio plus élevé
    X[bot_indices, 1] += 0.8  # tweet_frequency plus élevée
    X[bot_indices, 3] = 0     # moins vérifiés
    
    # Entraîner le modèle
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        class_weight='balanced'
    )
    
    model.fit(X_train, y_train)
    
    # Évaluer
    accuracy = model.score(X_test, y_test)
    print(f"✅ Modèle entraîné - Accuracy: {accuracy:.2%}")
    
    return model

def create_all_files():
    """Crée tous les fichiers nécessaires"""
    model_dir = "model"
    os.makedirs(model_dir, exist_ok=True)
    
    print(f"📁 Création des fichiers dans: {model_dir}")
    
    # 1. Créer bot_detector.pkl
    print("🤖 Création bot_detector.pkl...")
    model = create_ml_model()
    
    with open(os.path.join(model_dir, 'bot_detector.pkl'), 'wb') as f:
        pickle.dump(model, f)
    
    # 2. Créer les autres fichiers CSV
    create_csv_files(model_dir)
    
    print("\n✅ Tous les fichiers ont été créés!")
    print(f"\n📋 Fichiers dans {model_dir}:")
    for file in os.listdir(model_dir):
        file_path = os.path.join(model_dir, file)
        size = os.path.getsize(file_path) / 1024  # Taille en KB
        print(f"  - {file} ({size:.1f} KB)")

def create_csv_files(model_dir):
    """Crée les fichiers CSV de données"""
    
    # 2. final_risk_scores.csv
    print("📊 Création final_risk_scores.csv...")
    risk_data = []
    for i in range(1, 1001):
        risk_score = np.random.beta(2, 5)  # Distribution biaisée vers les faibles risques
        is_bot = risk_score > 0.7  # Si risque > 70%, considéré comme bot
        
        risk_data.append({
            'account_id': i,
            'username': f'user_{i:04d}',
            'risk_score': round(risk_score, 4),
            'bot_probability': round(risk_score, 4),
            'is_bot': is_bot,
            'last_analyzed': (datetime.now() - timedelta(days=np.random.randint(0, 30))).strftime('%Y-%m-%d %H:%M:%S'),
            'risk_category': 'high' if risk_score > 0.7 else 'medium' if risk_score > 0.3 else 'low'
        })
    
    pd.DataFrame(risk_data).to_csv(os.path.join(model_dir, 'final_risk_scores.csv'), index=False)
    
    # 3. ai_generated_narratives.csv
    print("📝 Création ai_generated_narratives.csv...")
    narratives = [
        {"name": "Election Interference", "keywords": "fraud,vote,rigged,election"},
        {"name": "Health Misinformation", "keywords": "vaccine,danger,side effects,big pharma"},
        {"name": "Financial Scams", "keywords": "crypto,free money,investment,get rich"},
        {"name": "Political Propaganda", "keywords": "conspiracy,deep state,elite,control"},
        {"name": "Climate Denial", "keywords": "hoax,climate change,weather,normal"},
        {"name": "Social Unrest", "keywords": "protest,riot,government,revolution"}
    ]
    
    narrative_data = []
    for i, narrative in enumerate(narratives, 1):
        confidence = np.random.uniform(0.75, 0.95)
        post_count = np.random.randint(500, 5000)
        
        narrative_data.append({
            'narrative_id': i,
            'name': narrative['name'],
            'keywords': narrative['keywords'],
            'description': f'AI detected narrative about {narrative["name"].lower()}',
            'confidence_score': round(confidence, 4),
            'detected_at': (datetime.now() - timedelta(days=np.random.randint(1, 60))).strftime('%Y-%m-%d'),
            'post_count': post_count,
            'account_count': post_count // 50,
            'risk_level': 'high' if confidence > 0.9 else 'medium',
            'trending_score': round(np.random.uniform(0.3, 0.9), 4)
        })
    
    pd.DataFrame(narrative_data).to_csv(os.path.join(model_dir, 'ai_generated_narratives.csv'), index=False)
    
    # 4. big_accounts.csv
    print("👥 Création big_accounts.csv...")
    accounts_data = []
    for i in range(1, 1001):
        is_bot = np.random.random() < 0.15  # 15% de bots
        is_verified = np.random.random() < 0.1  # 10% vérifiés
        
        if is_bot:
            followers = np.random.randint(0, 5000)
            following = np.random.randint(500, 10000)
            tweets = np.random.randint(1000, 50000)
        else:
            followers = np.random.randint(0, 10000)
            following = np.random.randint(0, 2000)
            tweets = np.random.randint(0, 10000)
        
        accounts_data.append({
            'id': i,
            'username': f'user_{i:04d}',
            'display_name': f'User {i}',
            'email': f'user{i}@example.com',
            'followers_count': followers,
            'following_count': following,
            'tweet_count': tweets,
            'verified': is_verified,
            'account_age_days': np.random.randint(1, 365*3),
            'location': np.random.choice(['Paris', 'London', 'New York', 'Tokyo', 'Berlin', 'Madrid', '', '', ''], p=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2, 0.2, 0.1]),
            'is_bot': is_bot,
            'created_at': (datetime.now() - timedelta(days=np.random.randint(1, 365*3))).strftime('%Y-%m-%d %H:%M:%S')
        })
    
    pd.DataFrame(accounts_data).to_csv(os.path.join(model_dir, 'big_accounts.csv'), index=False)
    
    # 5. big_posts.csv (pour compléter)
    print("💬 Création big_posts.csv...")
    posts_data = []
    for i in range(1, 5001):
        account_id = np.random.randint(1, 1001)
        narrative_id = np.random.choice([1, 2, 3, 4, 5, 6, None], p=[0.1, 0.1, 0.1, 0.1, 0.05, 0.05, 0.5])
        
        posts_data.append({
            'post_id': i,
            'account_id': account_id,
            'content': f'Sample post content {i} about current events and discussions.',
            'created_at': (datetime.now() - timedelta(hours=np.random.randint(0, 720))).strftime('%Y-%m-%d %H:%M:%S'),
            'likes_count': np.random.randint(0, 1000),
            'retweets_count': np.random.randint(0, 500),
            'replies_count': np.random.randint(0, 100),
            'sentiment_score': round(np.random.uniform(-1, 1), 4),
            'narrative_id': narrative_id,
            'language': np.random.choice(['en', 'fr', 'es'], p=[0.7, 0.2, 0.1])
        })
    
    pd.DataFrame(posts_data).to_csv(os.path.join(model_dir, 'big_posts.csv'), index=False)

if __name__ == "__main__":
    create_all_files()