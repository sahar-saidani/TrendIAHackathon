import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()
Faker.seed(42)

# --- CONFIGURATION ---
NUM_ACCOUNTS = 500  # Number of accounts to generate
NUM_POSTS = 5000    # Number of posts to generate
TOKENS = ['TAO', 'ASI', 'RNDR', 'AITK', 'FEX', 'NEURA', 'OMNI', 'XCY', 'BLOC']
TOPICS = ['price hype', 'community volatility', 'partnership rumor', 'bot surge', 'AI breakthrough']
TYPES = ['coordinated', 'fake_news', 'bot', 'doubt', 'organic']

# --- 1. GENERATE ACCOUNTS ---
accounts_data = []
credibility_options = ['bot', 'low', 'medium', 'high']

for i in range(1, NUM_ACCOUNTS + 1):
    acc_id = f"acc{i:04d}"
    credibility = random.choices(credibility_options, weights=[0.3, 0.3, 0.2, 0.2])[0]
    
    # Logic: Bots post more, follow more, have newer accounts
    if credibility == 'bot':
        posts_per_day = round(random.uniform(50, 200), 2)
        created_at = fake.date_between(start_date='-1y', end_date='today')
        followers = random.randint(0, 500)
    elif credibility == 'high':
        posts_per_day = round(random.uniform(1, 20), 2)
        created_at = fake.date_between(start_date='-5y', end_date='-2y')
        followers = random.randint(10000, 100000)
    else:
        posts_per_day = round(random.uniform(20, 80), 2)
        created_at = fake.date_between(start_date='-3y', end_date='-1y')
        followers = random.randint(500, 10000)

    accounts_data.append({
        'account_id': acc_id,
        'username': f"user_{i:03d}",
        'created_at': created_at,
        'followers': followers,
        'following': random.randint(10, 5000),
        'posts_per_day': posts_per_day,
        'credibility': credibility
    })

df_accounts = pd.DataFrame(accounts_data)

# --- 2. GENERATE POSTS ---
posts_data = []
account_ids = df_accounts['account_id'].tolist()

# Templates to make text realistic
templates = {
    'bot': ["To the moon!!!", "Buy now!! Massive potential!", "Don't miss this 100x!", "Pump incoming!"],
    'coordinated': ["Strong team strong roadmap!", "This will be the next 100x!", "Undervalued gem!", "Massive pump incoming stay ready!"],
    'fake_news': ["Insider: massive deal incoming!", "BREAKING: Major partnership confirmed!", "Leaked info suggests huge collaboration!", "Rumor: Big tech involved!"],
    'doubt': ["Seems like coordinated hype.", "Where is the proof?", "This might be manipulated.", "Too many identical posts today..."],
    'organic': ["The project is growing steadily.", "Solid long-term potential.", "Market sentiment seems healthy.", "Strong development updates."]
}

current_time = datetime(2025, 12, 4, 14, 0, 0)

for i in range(1, NUM_POSTS + 1):
    post_id = f"p{i:04d}"
    post_type = random.choice(TYPES)
    token = random.choice(TOKENS)
    account = random.choice(account_ids)
    
    # Select text based on type
    text_base = random.choice(templates[post_type])
    text = f"{text_base} #{token}" if random.random() > 0.7 else text_base
    
    # Increment time slightly
    current_time += timedelta(seconds=random.randint(1, 30))
    
    posts_data.append({
        'post_id': post_id,
        'text': text,
        'account_id': account,
        'timestamp': current_time.isoformat(),
        'token': token,
        'type': post_type
    })

df_posts = pd.DataFrame(posts_data)

# --- 3. GENERATE NARRATIVES ---
# Group posts by Token and Type to form narratives
narratives_data = []
grouped = df_posts.groupby(['token', 'type'])

narrative_counter = 1
for (token, p_type), group in grouped:
    # Only create a narrative if there are enough posts
    if len(group) > 5:
        # Map post type to narrative topic
        topic_map = {
            'bot': 'bot surge',
            'coordinated': 'price hype',
            'fake_news': 'partnership rumor',
            'doubt': 'community volatility',
            'organic': 'AI breakthrough'
        }
        
        # Take a chunk of post IDs
        post_ids = group['post_id'].tolist()[:10] # Link first 10 posts for the narrative
        
        narratives_data.append({
            'narrative_id': f"n{narrative_counter:03d}",
            'token': token,
            'topic': topic_map.get(p_type, 'general_discussion'),
            'posts': ",".join(post_ids)
        })
        narrative_counter += 1

df_narratives = pd.DataFrame(narratives_data)

# --- EXPORT ---
print("Generating files...")
df_accounts.to_csv('generated_accounts.csv', index=False)
df_posts.to_csv('generated_posts.csv', index=False)
df_narratives.to_csv('generated_narratives.csv', index=False)
print(f"Done! Generated {len(df_accounts)} accounts, {len(df_posts)} posts, and {len(df_narratives)} narratives.")