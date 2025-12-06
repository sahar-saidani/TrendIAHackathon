import pandas as pd
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
print(f"\nSaved detailed risk analysis to {OUTPUT_FILE}")