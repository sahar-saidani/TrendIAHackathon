import pandas as pd
from datetime import datetime
import numpy as np

# --- CONFIGURATION ---
ACCOUNTS_FILE = './data/big_accounts.csv'
POSTS_FILE = 'big_posts_enriched.csv' # Needs the file with 'is_bot' from previous steps
OUTPUT_FILE = 'final_account_trust.csv'

print("Loading data for Trust Analysis...")
try:
    accounts_df = pd.read_csv(ACCOUNTS_FILE)
    posts_df = pd.read_csv(POSTS_FILE)
except FileNotFoundError:
    print("❌ Missing data files. Please run previous AI steps first.")
    exit()

# --- 1. CALCULATE BEHAVIORAL METRICS ---
print("Analyzing user behavior...")

# Group posts by account to see their AI stats
user_stats = posts_df.groupby('account_id').agg({
    'is_bot': 'mean',          # % of posts flagged as bot (0.0 to 1.0)
    'sentiment_score': 'std'   # Sentiment volatility (Bots often repeat same sentiment)
}).reset_index()

user_stats.rename(columns={'is_bot': 'bot_ratio', 'sentiment_score': 'volatility'}, inplace=True)

# Merge back into accounts
df = pd.merge(accounts_df, user_stats, on='account_id', how='left')
df['bot_ratio'] = df['bot_ratio'].fillna(0) # Default to 0 if no posts
df['volatility'] = df['volatility'].fillna(0.5) # Default normal volatility

# --- 2. THE TRUST ALGORITHM ---
def calculate_trust(row):
    score = 50 # Start neutral
    
    # FACTOR A: Account Age (Older = More Trust)
    # Assuming format YYYY-MM-DD
    try:
        created = datetime.strptime(row['created_at'], '%Y-%m-%d')
        age_days = (datetime.now() - created).days
        if age_days > 1000: score += 20
        elif age_days > 365: score += 10
        elif age_days < 30: score -= 10 # Brand new account
    except:
        pass
        
    # FACTOR B: Bot Behavior (The AI Verdict)
    # If AI said > 50% of their posts are bots, massive penalty
    if row['bot_ratio'] > 0.8: score -= 50
    elif row['bot_ratio'] > 0.5: score -= 30
    elif row['bot_ratio'] < 0.1: score += 10 # consistently organic
    
    # FACTOR C: Spammer Indicators
    if row['posts_per_day'] > 50: score -= 20 # Humanly impossible
    if row['posts_per_day'] < 5: score += 5   # Normal activity
    
    # Clamp score 0-100
    return max(0, min(100, score))

print("Calculating Trust Scores...")
df['trust_score'] = df.apply(calculate_trust, axis=1)

# --- 3. ASSIGN LABELS ---
def get_label(score):
    if score > 75: return "Reliable"
    if score < 30: return "Bot/Malicious"
    return "Neutral"

df['trust_label'] = df['trust_score'].apply(get_label)

# --- EXPORT ---
output = df[['account_id', 'username', 'trust_score', 'trust_label', 'bot_ratio', 'posts_per_day']]
output.to_csv(OUTPUT_FILE, index=False)

print("\n--- TOP TRUSTED USERS ---")
print(output.sort_values('trust_score', ascending=False).head(5))
print("\n--- IDENTIFIED BOTS ---")
print(output.sort_values('trust_score', ascending=True).head(5))
print(f"\nSaved account trust scores to {OUTPUT_FILE}")