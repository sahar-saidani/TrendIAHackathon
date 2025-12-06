from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import pickle
import re

app = FastAPI(title="TrendAI API", version="1.0")

# --- GLOBAL VARIABLES TO HOLD DATA ---
model = None
risk_df = None
narratives_df = None

# --- LOAD DATA ON STARTUP ---
@app.on_event("startup")
def load_resources():
    global model, risk_df, narratives_df
    print("Loading AI resources...")
    
    # 1. Load the AI Model
    try:
        with open('bot_detector.pkl', 'rb') as f:
            model = pickle.load(f)
        print("✅ Model loaded.")
    except Exception as e:
        print(f"⚠️ Warning: Could not load model ({e}). Live analysis will fail.")

    # 2. Load Risk Data
    try:
        risk_df = pd.read_csv('final_risk_scores.csv')
        print("✅ Risk data loaded.")
    except:
        print("⚠️ Warning: final_risk_scores.csv not found.")

    # 3. Load Narratives
    try:
        narratives_df = pd.read_csv('ai_generated_narratives.csv')
        print("✅ Narratives loaded.")
    except:
        print("⚠️ Warning: ai_generated_narratives.csv not found.")

# --- HELPER FUNCTIONS ---
def clean_text(text):
    if not isinstance(text, str): return ""
    return re.sub(r'[^\w\s]', '', text.lower())

# --- DATA MODELS ---
class PostAnalysisRequest(BaseModel):
    text: str

# --- ENDPOINTS ---

@app.get("/")
def health_check():
    return {"status": "active", "service": "TrendAI Backend"}

@app.get("/risk/{token_id}")
def get_token_risk(token_id: str):
    """
    Get the pre-calculated risk score and narratives for a specific token (e.g., NEURA).
    """
    token_id = token_id.upper()
    
    # 1. Get Risk Score
    token_risk = risk_df[risk_df['token_id'] == token_id]
    if token_risk.empty:
        raise HTTPException(status_code=404, detail="Token not found in database")
    
    risk_data = token_risk.iloc[0].to_dict()
    
    # 2. Get Narratives for this token
    token_narratives = narratives_df[narratives_df['token_id'] == token_id]
    narratives_list = token_narratives[['topic', 'start_time', 'end_time']].to_dict(orient='records')
    
    return {
        "token": token_id,
        "risk_level": risk_data.get('label'),
        "risk_score": risk_data.get('risk_score'),
        "reason": risk_data.get('reason'),
        "active_narratives": narratives_list
    }

@app.get("/rankings/high-risk")
def get_high_risk_tokens():
    """
    Returns the top 5 most dangerous tokens.
    """
    if risk_df is None: return []
    top_risk = risk_df.sort_values('risk_score', ascending=False).head(5)
    return top_risk[['token_id', 'risk_score', 'label', 'reason']].to_dict(orient='records')

@app.post("/analyze")
def analyze_post(request: PostAnalysisRequest):
    """
    Live AI: Send any text, and the model predicts if it's Organic or Suspicious.
    """
    if model is None:
        raise HTTPException(status_code=503, detail="AI Model is not loaded")
    
    # Preprocess
    clean = clean_text(request.text)
    
    # Predict
    pred_class = model.predict([clean])[0]
    prob = model.predict_proba([clean])[0][1] # Probability of being suspicious
    
    label = "SUSPICIOUS" if pred_class == 1 else "ORGANIC"
    
    return {
        "text_snippet": request.text[:50] + "...",
        "prediction": label,
        "suspicion_score": float(round(prob, 4)),
        "is_bot": bool(pred_class == 1)
    }