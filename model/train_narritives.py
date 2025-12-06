import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# --- CONFIGURATION ---
INPUT_FILE = './data/big_posts.csv'  # Use your generated big file
CLUSTERS_PER_TOKEN = 3        # How many narratives to find per token

# --- 1. LOAD DATA ---
print("Loading data...")
df = pd.read_csv(INPUT_FILE)

# Basic cleaning function
def clean_text(text):
    if not isinstance(text, str): return ""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text) 
    return text

df['clean_text'] = df['text'].apply(clean_text)

# --- 2. THE AI ENGINE (Per Token) ---
narrative_results = []
narrative_id_counter = 1

unique_tokens = df['token_id'].unique()

print(f"Analyzing narratives for {len(unique_tokens)} tokens...")

for token in unique_tokens:
    # Get posts for this token
    token_df = df[df['token_id'] == token].copy()
    
    # Skip if too few posts to cluster
    if len(token_df) < 10:
        continue
        
    # A. VECTORIZATION
    # Convert text to numbers, ignoring common English words
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    X = vectorizer.fit_transform(token_df['clean_text'])
    
    # B. CLUSTERING (K-Means)
    kmeans = KMeans(n_clusters=CLUSTERS_PER_TOKEN, random_state=42)
    kmeans.fit(X)
    
    # Assign cluster IDs back to the dataframe
    token_df['cluster'] = kmeans.labels_
    
    # C. TOPIC EXTRACTION
    # Get words that define each cluster center
    order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()
    
    for i in range(CLUSTERS_PER_TOKEN):
        # Get top 3 keywords for this cluster
        top_terms = [terms[ind] for ind in order_centroids[i, :3]]
        topic_name = " ".join(top_terms).title() # e.g. "Price Moon Buy"
        
        # Get time range and post IDs
        cluster_posts = token_df[token_df['cluster'] == i]
        start_time = cluster_posts['timestamp'].min()
        end_time = cluster_posts['timestamp'].max()
        post_ids = ",".join(cluster_posts['post_id'].astype(str).tolist()[:20]) # Limit IDs for CSV
        
        narrative_results.append({
            'narrative_id': f"n{narrative_id_counter:04d}",
            'token_id': token,
            'topic': f"Trend: {topic_name}", # The AI-detected topic
            'start_time': start_time,
            'end_time': end_time,
            'posts': post_ids
        })
        narrative_id_counter += 1

# --- 3. EXPORT ---
df_narratives = pd.DataFrame(narrative_results)
df_narratives.to_csv('ai_generated_narratives.csv', index=False)

print("SUCCESS!")
print(f"Generated {len(df_narratives)} narratives based on actual text analysis.")
print(df_narratives[['token_id', 'topic']].head(10))