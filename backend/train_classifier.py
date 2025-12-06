import pandas as pd
import re
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score

# --- CONFIGURATION ---
DATA_FILE = './data/big_posts.csv'     # Your data file
MODEL_FILE = 'bot_detector.pkl' # Where to save the trained model

# --- 1. LOAD & PREPARE DATA ---
print("Loading data...")
df = pd.read_csv(DATA_FILE)

# Map detailed types to binary labels for classification
# Target: 0 = Organic, 1 = Suspicious (Bot/Fake/Coordinated)
def map_label(post_type):
    if post_type in ['bot', 'coordinated', 'fake_news']:
        return 1
    return 0

df['target'] = df['type'].apply(map_label)

# Basic text cleaning function
def clean_text(text):
    if not isinstance(text, str): return ""
    text = text.lower()
    text = re.sub(r'http\S+', '', text) # Remove URLs
    text = re.sub(r'[^\w\s]', '', text) # Remove punctuation
    return text

print("Cleaning text...")
df['clean_text'] = df['text'].apply(clean_text)

# --- 2. TRAIN MODEL ---
X = df['clean_text']
y = df['target']

# Split data: 80% for training, 20% for testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a Pipeline:
# 1. TF-IDF: Converts text to numbers
# 2. LogisticRegression: The classifier
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=5000, stop_words='english')),
    ('clf', LogisticRegression())
])

print("Training classifier (this may take a moment)...")
pipeline.fit(X_train, y_train)

# --- 3. EVALUATE ---
predictions = pipeline.predict(X_test)
print("\n--- Model Evaluation ---")
print(f"Accuracy: {accuracy_score(y_test, predictions):.2f}")
print(classification_report(y_test, predictions, target_names=['Organic', 'Suspicious']))

# --- 4. SAVE MODEL ---
print(f"Saving model to {MODEL_FILE}...")
with open(MODEL_FILE, 'wb') as f:
    pickle.dump(pipeline, f)

# --- 5. TEST FUNCTION ---
def predict_post(text):
    # Load model (simulating backend usage)
    with open(MODEL_FILE, 'rb') as f:
        loaded_model = pickle.load(f)
    
    clean = clean_text(text)
    pred_class = loaded_model.predict([clean])[0]
    prob = loaded_model.predict_proba([clean])[0][1] # Probability of being suspicious
    
    label = "SUSPICIOUS" if pred_class == 1 else "ORGANIC"
    print(f"\nInput: '{text}'")
    print(f"Prediction: {label} (Suspicion Score: {prob:.2f})")

# Run a quick test
predict_post("I've been reading the whitepaper and the tokenomics look solid.")
predict_post("BUY BUY BUY!!! 1000x GEMS MOON SOON! 🚀🚀🚀")