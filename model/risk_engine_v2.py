import pandas as pd
import pickle
import re

# --- CONFIGURATION ---
POSTS_FILE = 'big_posts_enriched.csv' # Use the file with sentiment!
MODEL_FILE = 'bot_detector.pkl'
OUTPUT_FILE = 'final_risk_scores.csv'

# --- LOAD RESOURCES ---
print("Loading enriched data...")
try:
    df = pd.read_csv(POSTS_FILE)
    with open(MODEL_FILE, 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    print("❌ Error: Missing files. Run 'ai_sentiment.py' first!")
    exit()

def clean_text(text):
    if not isinstance(text, str): return ""
    return re.sub(r'[^\w\s]', '', text.lower())

# --- RUN BOT CLASSIFIER ---
print("Re-verifying bot detection...")
df['clean_text'] = df['text'].apply(clean_text)
df['is_bot'] = model.predict(df['clean_text'])

# --- ADVANCED RISK LOGIC ---
print("Calculating Advanced Risk Metrics...")

risk_results = []
unique_tokens = df['token_id'].unique()

for token in unique_tokens:
    token_df = df[df['token_id'] == token]
    total = len(token_df)
    if total == 0: continue

    # 1. Metrics
    bot_count = token_df['is_bot'].sum()
    bot_ratio = (bot_count / total) * 100
    avg_sentiment = token_df['sentiment_score'].mean() # -1 to 1
    
    # 2. Heuristic Logic (The "AI" Reasoning)
    risk_score = 0
    label = "SAFE"
    reason = "Normal organic activity."

    # BASE RISK (Bot Activity)
    risk_score += bot_ratio  # If 50% bots, risk is at least 50

    # AMPLIFIER: Pump & Dump (Bots + Super Positive)
    if bot_ratio > 30 and avg_sentiment > 0.5:
        risk_score += 20
        label = "PUMP & DUMP"
        reason = f"⚠️ Coordinated High-Hype Bot Attack ({bot_ratio:.1f}% bots)."

    # AMPLIFIER: FUD Attack (Bots + Super Negative)
    elif bot_ratio > 30 and avg_sentiment < -0.5:
        risk_score += 20
        label = "FUD ATTACK"
        reason = f"⚠️ Targeted Negative Bot Campaign ({bot_ratio:.1f}% bots)."
        
    # AMPLIFIER: Suspicious Volume
    elif bot_ratio > 50:
        label = "HIGH RISK"
        reason = "Critical levels of non-human activity detected."
    
    elif bot_ratio > 20:
        label = "SUSPICIOUS"
        reason = "Moderate bot activity observed."

    # Cap Score at 100
    risk_score = min(risk_score, 100)

    risk_results.append({
        'token_id': token,
        'risk_score': round(risk_score, 2),
        'label': label,
        'bot_ratio': round(bot_ratio, 1),
        'avg_sentiment': round(avg_sentiment, 2),
        'reason': reason
    })

# --- EXPORT ---
risk_df = pd.DataFrame(risk_results).sort_values('risk_score', ascending=False)
print(risk_df.head(10))
risk_df.to_csv(OUTPUT_FILE, index=False)
print("✅ Advanced Risk Analysis Saved.")