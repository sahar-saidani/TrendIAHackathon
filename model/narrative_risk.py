import pandas as pd

# --- CONFIGURATION ---
NARRATIVES_FILE = 'ai_generated_narratives.csv'
POSTS_FILE = 'big_posts_enriched.csv' # Needs 'is_bot' and 'sentiment_score'
OUTPUT_FILE = 'final_narrative_risk.csv'

print("Loading narrative data...")
try:
    narratives_df = pd.read_csv(NARRATIVES_FILE)
    posts_df = pd.read_csv(POSTS_FILE)
except FileNotFoundError:
    print("❌ Missing files.")
    exit()

# Set index for fast lookup
posts_df.set_index('post_id', inplace=True)

print("Analyzing Narrative Health...")

narrative_risks = []

for index, row in narratives_df.iterrows():
    # 1. Parse Post IDs in this narrative
    # stored as "p001,p002,p003"
    post_ids = str(row['posts']).split(',')
    
    # 2. Get the actual post data
    # Filter only IDs that exist in our posts file
    valid_ids = [pid for pid in post_ids if pid in posts_df.index]
    cluster_data = posts_df.loc[valid_ids]
    
    if len(cluster_data) == 0:
        continue
        
    # 3. Calculate Risk Metrics
    bot_volume = cluster_data['is_bot'].sum()
    total_volume = len(cluster_data)
    bot_percentage = (bot_volume / total_volume) * 100
    
    avg_sentiment = cluster_data['sentiment_score'].mean()
    
    # 4. Determine Narrative Risk Level
    risk_level = "LOW"
    warning = "Organic conversation"
    
    # High Bot Activity
    if bot_percentage > 60:
        risk_level = "HIGH"
        warning = "🚨 Heavily Manipulated (Bot Army)"
        
    # "The Trap" (Bots + High Positive Sentiment)
    elif bot_percentage > 40 and avg_sentiment > 0.4:
        risk_level = "CRITICAL"
        warning = "⚠️ Artificial Hype / Bull Trap"
        
    # "The FUD" (Bots + High Negative Sentiment)
    elif bot_percentage > 40 and avg_sentiment < -0.4:
        risk_level = "HIGH"
        warning = "⚠️ Coordinated FUD Attack"
        
    narrative_risks.append({
        'narrative_id': row['narrative_id'],
        'token_id': row['token_id'],
        'topic': row['topic'],
        'risk_level': risk_level,
        'bot_percentage': round(bot_percentage, 1),
        'avg_sentiment': round(avg_sentiment, 2),
        'warning': warning
    })

# --- EXPORT ---
risk_df = pd.DataFrame(narrative_risks)
risk_df.to_csv(OUTPUT_FILE, index=False)

print("\n--- NARRATIVE RISK REPORT ---")
print(risk_df[['topic', 'risk_level', 'warning']].head(10))
print(f"\nSaved narrative risk analysis to {OUTPUT_FILE}")