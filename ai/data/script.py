import pandas as pd
import random
from datetime import datetime, timedelta

# --- CONFIGURATION (Adjust these for Big Data) ---
NUM_ACCOUNTS = 5000       # e.g., 5,000 users
NUM_POSTS = 100000        # e.g., 1,000,000 posts
TOKENS = ['AITK', 'NEURA', 'BLOC', 'OMNI', 'XCY', 'TAO', 'RNDR']
START_DATE = datetime(2025, 1, 1)
DAYS_RANGE = 90           # Generate 3 months of history

random.seed(42)

# --- TEXT TEMPLATES (Longer Content) ---
intros = [
    "I've been analyzing the market trends deeply and realized something important about {token}.",
    "Hey everyone, just wanted to share my thoughts on the recent price action of {token}.",
    "Listen up, this is not financial advice but you need to see what's happening with {token}.",
    "The development team behind {token} has just released some interesting updates on their roadmap.",
    "Be careful out there, I'm seeing a lot of mixed signals regarding {token} lately."
]
bodies = [
    "The liquidity pools are showing massive inflows which usually signals a breakout. However, the RSI on the 4h chart is overbought.",
    "Several whale wallets have moved significant amounts to exchanges. This could mean a dump is incoming or just redistribution.",
    "If you look at the GitHub activity, the commit history has been incredibly active this week. Developers are shipping code fast.",
    "There are rumors circulating on Telegram about a potential partnership with a major tech giant, but nothing is confirmed yet.",
    "The community sentiment has shifted from fear to extreme greed in just 24 hours. This kind of volatility is dangerous."
]
outros = [
    "Do your own research before jumping in. The market is unpredictable right now.",
    "I'm personally accumulating more at these levels. Long term vision remains strong.",
    "Let's see how the daily candle closes. That will determine the next trend direction.",
    "Stay safe and don't get liquidated. Risk management is key in this environment.",
    "What do you guys think? Drop your comments below."
]

def generate_long_text(token, p_type):
    if p_type == 'bot':
        return f"🚀🚀 {token} TO THE MOON!! 🚀🚀 Don't miss this 1000x opportunity! Buy now! The chart is primed for a massive breakout and the whales are accumulating. #Crypto #Gems #{token}"
    elif p_type == 'coordinated':
        return f"ATTENTION: We are all buying {token} at exactly 2 PM UTC. The target is $10.00! We need everyone to hold the line and not sell. Spread the word to every group! #{token}Army"
    elif p_type == 'fake_news':
        return f"BREAKING NEWS 🚨: {token} just signed a secret deal with a major Fortune 500 company?! Insider sources confirm the partnership will be announced tomorrow! This changes everything. Load your bags! #{token}"
    else:
        # Organic / Doubt (Longer paragraphs)
        return f"{random.choice(intros).format(token=token)} {random.choice(bodies).format(token=token)} {random.choice(outros)}"

# --- 1. GENERATE ACCOUNTS ---
print("Generating Accounts...")
accounts = []
for i in range(1, NUM_ACCOUNTS + 1):
    acc_type = random.choice(['organic', 'bot', 'suspicious'])
    
    # Credibility logic
    if acc_type == 'bot':
        cred = 'low'
        post_freq = random.randint(50, 200)
    elif acc_type == 'suspicious':
        cred = 'medium'
        post_freq = random.randint(20, 80)
    else:
        cred = 'high'
        post_freq = random.randint(1, 10)
        
    accounts.append({
        'account_id': f"acc{i:05d}",
        'username': f"user_{i:05d}",
        'created_at': (START_DATE - timedelta(days=random.randint(0, 1000))).date(),
        'followers': random.randint(0, 50000),
        'following': random.randint(10, 2000),
        'posts_per_day': post_freq,
        'credibility': cred
    })
df_accounts = pd.DataFrame(accounts)

# --- 2. GENERATE POSTS ---
print("Generating Posts...")
posts = []
post_counter = 1
for _ in range(NUM_POSTS):
    token = random.choice(TOKENS)
    acc = random.choice(accounts)
    
    # Determine type
    if acc['credibility'] == 'low':
        p_type = random.choices(['bot', 'coordinated', 'fake_news'], weights=[0.6, 0.3, 0.1])[0]
    else:
        p_type = random.choices(['organic', 'doubt'], weights=[0.8, 0.2])[0]
    
    text = generate_long_text(token, p_type)
    ts = START_DATE + timedelta(seconds=random.randint(0, DAYS_RANGE * 24 * 3600))
    
    # Scores
    if p_type in ['bot', 'coordinated', 'fake_news']:
        label = 'Suspicious'
        org_score = random.uniform(0.0, 0.4)
    else:
        label = 'Organic'
        org_score = random.uniform(0.6, 1.0)
        
    posts.append({
        'id': post_counter,
        'post_id': f"p{post_counter:07d}",
        'token_id': token,
        'account_id': acc['account_id'],
        'text': text,
        'timestamp': ts,
        'type': p_type,
        'organic_score': round(org_score, 2),
        'label': label,
        'bot_score': round(1.0 - org_score, 2)
    })
    post_counter += 1
df_posts = pd.DataFrame(posts)

# --- 3. GENERATE NARRATIVES (Clustered by Week) ---
print("Generating Narratives...")
narratives = []
df_posts['week'] = df_posts['timestamp'].apply(lambda x: x.isocalendar()[1])
grouped = df_posts.groupby(['token_id', 'type', 'week'])

narrative_count = 1
for (token, p_type, week), group in grouped:
    # Only create narratives for significant clusters
    if len(group) >= 5 and p_type != 'organic':
        topic = f"{p_type.replace('_', ' ').title()} Spike (Week {week})"
        post_ids = ",".join(group['post_id'].tolist()[:20]) # First 20 IDs
        
        narratives.append({
            'narrative_id': f"n{narrative_count:05d}",
            'token_id': token,
            'topic': topic,
            'start_time': group['timestamp'].min(),
            'end_time': group['timestamp'].max(),
            'posts': post_ids
        })
        narrative_count += 1
df_narratives = pd.DataFrame(narratives)

# --- 4. GENERATE HISTORICAL RISK SCORES (Daily) ---
print("Generating Historical Risk Scores...")
risk_scores = []
dates = pd.date_range(start=START_DATE, periods=DAYS_RANGE, freq='D')
risk_id = 1

for date in dates:
    for token in TOKENS:
        # Simulate risk calculation for that specific day
        daily_posts = df_posts[(df_posts['token_id'] == token) & 
                               (df_posts['timestamp'].dt.date == date.date())]
        
        if len(daily_posts) > 0:
            suspicious = len(daily_posts[daily_posts['label'] == 'Suspicious'])
            score = (suspicious / len(daily_posts)) * 100
        else:
            score = 0.0
            
        label = 'High Risk' if score > 70 else ('Suspicious' if score > 30 else 'Safe')
        
        risk_scores.append({
            'id': risk_id,
            'token_id': token,
            'score': round(score, 2),
            'label': label,
            'reason': f"Daily analysis: {len(daily_posts)} posts detected.",
            'updated_at': date
        })
        risk_id += 1
df_risk = pd.DataFrame(risk_scores)

# --- EXPORT ---
print("Exporting...")
df_accounts.to_csv('big_accounts.csv', index=False)
df_posts.drop(columns=['week'], inplace=True) # Cleanup helper col
df_posts.to_csv('big_posts.csv', index=False)
df_narratives.to_csv('big_narratives.csv', index=False)
df_risk.to_csv('big_risk_scores.csv', index=False)
print("Done!")