""" import pandas as pd
import pickle
import re

# --- CONFIGURATION ---
POSTS_FILE = './data/big_posts.csv'
MODEL_FILE = 'bot_detector.pkl'  # The model you trained in Step 1
OUTPUT_FILE = 'final_risk_scores.csv'

# --- 1. LOAD RESOURCES ---
print("Loading data and model...")
try:
    df = pd.read_csv(POSTS_FILE)
    with open(MODEL_FILE, 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    print("Error: Could not find 'big_posts.csv' or 'bot_detector.pkl'.")
    print("Please run the previous scripts first!")
    exit()

# Helper to clean text (must match training step)
def clean_text(text):
    if not isinstance(text, str): return ""
    return re.sub(r'[^\w\s]', '', text.lower())

# --- 2. RUN AI PREDICTIONS ---
print(f"Analyzing {len(df)} posts... this might take a minute.")

# Prepare text for the model
df['clean_text'] = df['text'].apply(clean_text)

# Predict organic(0) vs suspicious(1) for ALL posts
# (The pipeline inside the pkl handles vectorization)
df['ai_pred'] = model.predict(df['clean_text']) 

# --- 3. CALCULATE RISK PER TOKEN ---
print("Calculating risk scores...")

risk_results = []
unique_tokens = df['token_id'].unique()

for token in unique_tokens:
    # Get all posts for this token
    token_posts = df[df['token_id'] == token]
    total = len(token_posts)
    
    if total == 0: continue

    # Count suspicious posts identified by AI
    suspicious_count = token_posts['ai_pred'].sum()
    
    # Formula: Risk = (Suspicious / Total) * 100
    risk_score = (suspicious_count / total) * 100
    
    # Determine Label
    if risk_score > 75:
        label = "HIGH RISK"
        reason = f"Critical levels of bot activity detected ({risk_score:.1f}%)."
    elif risk_score > 35:
        label = "SUSPICIOUS"
        reason = f"Moderate manipulation signs observed ({risk_score:.1f}%)."
    else:
        label = "SAFE"
        reason = "Community sentiment appears organic."

    risk_results.append({
        'token_id': token,
        'risk_score': round(risk_score, 2),
        'label': label,
        'total_posts': total,
        'suspicious_posts': suspicious_count,
        'reason': reason
    })

# --- 4. EXPORT ---
risk_df = pd.DataFrame(risk_results)
risk_df = risk_df.sort_values('risk_score', ascending=False)

print("\n--- FINAL RISK REPORT ---")
print(risk_df.head(10))

risk_df.to_csv(OUTPUT_FILE, index=False)
print(f"\nSaved detailed risk analysis to {OUTPUT_FILE}") """

"""
Moteur de risque amélioré avec détection de patterns spécifiques
"""
import pandas as pd
import numpy as np
from datetime import datetime
import re
from collections import Counter

class PatternDetector:
    """Détecteur de patterns de manipulation"""
    
    def __init__(self):
        self.patterns = {
            'duplicate_content': {
                'threshold': 0.85,
                'min_occurrences': 3
            },
            'coordinated_timing': {
                'time_window_minutes': 5,
                'min_posts': 10
            },
            'bot_accounts': {
                'username_patterns': [
                    r'crypto.*\d{2,}',
                    r'whale.*\d+',
                    r'moon.*\d{4}',
                    r'trader.*\d+',
                    r'alpha.*\d+',
                    r'investor.*\d+',
                    r'hodl.*\d+'
                ]
            }
        }
    
    def detect_duplicates(self, posts_df):
        """Détecter les contenus dupliqués"""
        if len(posts_df) < 3:
            return []
        
        texts = posts_df['text'].tolist()
        duplicates = []
        
        for i in range(len(texts)):
            for j in range(i+1, len(texts)):
                similarity = self._text_similarity(texts[i], texts[j])
                if similarity > self.patterns['duplicate_content']['threshold']:
                    duplicates.append({
                        'text1': texts[i],
                        'text2': texts[j],
                        'similarity': similarity,
                        'accounts': [
                            posts_df.iloc[i]['username'],
                            posts_df.iloc[j]['username']
                        ]
                    })
        
        return duplicates
    
    def detect_coordinated_posting(self, posts_df):
        """Détecter la coordination temporelle"""
        if len(posts_df) < self.patterns['coordinated_timing']['min_posts']:
            return False
        
        posts_df = posts_df.sort_values('timestamp')
        timestamps = pd.to_datetime(posts_df['timestamp'])
        
        # Calculer les intervalles
        intervals = np.diff(timestamps.values.astype(np.int64) // 10**9)  # en secondes
        
        # Chercher des bursts d'activité
        window_seconds = self.patterns['coordinated_timing']['time_window_minutes'] * 60
        burst_count = 0
        current_burst = 0
        
        for interval in intervals:
            if interval < window_seconds:
                current_burst += 1
                if current_burst >= self.patterns['coordinated_timing']['min_posts']:
                    burst_count += 1
            else:
                current_burst = 0
        
        return burst_count > 0
    
    def detect_bot_accounts(self, posts_df):
        """Identifier les comptes bot"""
        usernames = posts_df['username'].unique()
        bot_accounts = []
        
        for username in usernames:
            if self._is_bot_username(username):
                user_posts = posts_df[posts_df['username'] == username]
                bot_accounts.append({
                    'username': username,
                    'post_count': len(user_posts),
                    'avg_likes': user_posts['likes'].mean(),
                    'duplicate_rate': self._calculate_duplicate_rate(user_posts)
                })
        
        return bot_accounts
    
    def _is_bot_username(self, username):
        """Vérifier si un username correspond aux patterns bot"""
        username_lower = username.lower()
        for pattern in self.patterns['bot_accounts']['username_patterns']:
            if re.search(pattern, username_lower):
                return True
        return False
    
    def _calculate_duplicate_rate(self, user_posts):
        """Calculer le taux de duplication pour un utilisateur"""
        if len(user_posts) < 2:
            return 0
        
        texts = user_posts['text'].tolist()
        unique_texts = set(texts)
        
        return 1 - (len(unique_texts) / len(texts))
    
    def _text_similarity(self, text1, text2):
        """Calculer la similarité entre deux textes"""
        # Simple similarité de Jaccard
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0

class TrustScorer:
    """Calculateur de score de confiance"""
    
    def __init__(self):
        self.weights = {
            'account_age': 0.15,
            'post_history': 0.20,
            'engagement_quality': 0.25,
            'content_authenticity': 0.30,
            'pattern_risk': 0.10
        }
    
    def calculate_post_score(self, post_data):
        """Calculer le score pour un post individuel"""
        score = 100
        
        # 1. Longueur du texte
        if len(post_data['text']) < 20:
            score -= 20
        
        # 2. Emotes excessifs
        emote_count = len(re.findall(r'[🚀🎉🔥💎🍀]+', post_data['text']))
        if emote_count > 3:
            score -= 15
        
        # 3. Langage d'urgence
        urgency_words = ['urgent', 'now', 'hurry', 'last chance', 'don\'t miss']
        if any(word in post_data['text'].lower() for word in urgency_words):
            score -= 10
        
        # 4. Références non vérifiées
        unverified_refs = ['breaking', 'insider', 'confirmed', 'exclusive']
        if any(ref in post_data['text'].lower() for ref in unverified_refs):
            score -= 15
        
        # 5. Engagement organique
        if post_data.get('likes', 0) > 20:
            score += 10
        
        return max(0, min(100, score))
    
    def calculate_account_score(self, account_data):
        """Calculer le score pour un compte"""
        score = 100
        
        # 1. Historique de posts
        if account_data.get('post_count', 0) < 5:
            score -= 20
        elif account_data.get('post_count', 0) > 1000:
            score -= 10  # Possible spam account
        
        # 2. Taux d'engagement moyen
        avg_likes = account_data.get('avg_likes', 0)
        if avg_likes < 1:
            score -= 15
        
        # 3. Taux de duplication
        duplicate_rate = account_data.get('duplicate_rate', 0)
        if duplicate_rate > 0.5:
            score -= 25
        
        # 4. Pattern du username
        if self._is_suspicious_username(account_data.get('username', '')):
            score -= 20
        
        return max(0, min(100, score))
    
    def _is_suspicious_username(self, username):
        """Vérifier si le username est suspect"""
        suspicious_patterns = [
            r'\d{4}$',  # Finit par 4 chiffres
            r'crypto.*\d{2}',
            r'whale.*\d',
            r'trader.*\d'
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, username.lower()):
                return True
        return False

# Intégration avec l'API existante
def enhance_risk_analysis(token_id, posts_data):
    """Améliorer l'analyse de risque avec les nouveaux patterns"""
    
    detector = PatternDetector()
    scorer = TrustScorer()
    
    # Convertir en DataFrame
    df = pd.DataFrame(posts_data)
    
    # Détecter les patterns
    duplicates = detector.detect_duplicates(df)
    coordinated = detector.detect_coordinated_posting(df)
    bot_accounts = detector.detect_bot_accounts(df)
    
    # Calculer les scores
    post_scores = [scorer.calculate_post_score(row) for _, row in df.iterrows()]
    avg_post_score = np.mean(post_scores) if post_scores else 50
    
    account_scores = [scorer.calculate_account_score(acc) for acc in bot_accounts]
    avg_account_score = np.mean(account_scores) if account_scores else 50
    
    # Calculer le risque global
    risk_factors = {
        'duplicate_rate': min(1.0, len(duplicates) / max(1, len(df))),
        'coordinated_posting': 1.0 if coordinated else 0.0,
        'bot_account_ratio': len(bot_accounts) / max(1, len(df['username'].unique())),
        'low_trust_posts': sum(1 for score in post_scores if score < 30) / max(1, len(post_scores))
    }
    
    risk_score = (
        risk_factors['duplicate_rate'] * 40 +
        risk_factors['coordinated_posting'] * 30 +
        risk_factors['bot_account_ratio'] * 20 +
        risk_factors['low_trust_posts'] * 10
    )
    
    # Déterminer le label de risque
    if risk_score >= 80:
        risk_label = "HIGH RISK"
    elif risk_score >= 60:
        risk_label = "SUSPICIOUS"
    else:
        risk_label = "SAFE"
    
    return {
        'risk_score': int(risk_score),
        'risk_label': risk_label,
        'metrics': {
            'duplicate_posts': f"{(risk_factors['duplicate_rate']*100):.1f}%",
            'bot_accounts': len(bot_accounts),
            'coordinated_activity': coordinated,
            'avg_post_trust': f"{avg_post_score:.1f}/100",
            'avg_account_trust': f"{avg_account_score:.1f}/100"
        },
        'patterns_detected': {
            'duplicates_count': len(duplicates),
            'bot_accounts_details': bot_accounts[:5],  # Top 5 seulement
            'coordinated_windows': 1 if coordinated else 0
        }
    }