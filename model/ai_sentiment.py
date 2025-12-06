import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# --- SETUP ---
# Download the VADER lexicon (run this once)
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

INPUT_FILE = './data/big_posts.csv'
OUTPUT_FILE = 'big_posts_enriched.csv'

print("Loading data...")
df = pd.read_csv(INPUT_FILE)

# --- 1. CALCULATE SENTIMENT ---
print("Running Sentiment AI (VADER)...")

def get_sentiment(text):
    if not isinstance(text, str): return 0.0
    # Returns a score between -1 (Negative) and +1 (Positive)
    return sia.polarity_scores(text)['compound']

# Apply to all posts
df['sentiment_score'] = df['text'].apply(get_sentiment)

# --- 2. DEFINE SENTIMENT LABELS ---
def label_sentiment(score):
    if score > 0.3: return 'Positive'
    if score < -0.3: return 'Negative'
    return 'Neutral'

df['sentiment_label'] = df['sentiment_score'].apply(label_sentiment)

# --- 3. EXPORT ---
print(f"Sentiment Analysis Complete. Saving to {OUTPUT_FILE}...")
print(df[['text', 'sentiment_score', 'sentiment_label']].head(5))
df.to_csv(OUTPUT_FILE, index=False)