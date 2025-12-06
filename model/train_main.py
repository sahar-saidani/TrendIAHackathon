"""
API ML pour TrendAI - Version corrigée avec chemins relatifs
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import pickle
import re
import os
import sys
from typing import Optional

# Créer l'app FastAPI
app = FastAPI(
    title="TrendAI ML API",
    version="1.0",
    description="API d'analyse ML pour détection de manipulation"
)

# --- GLOBAL VARIABLES ---
model = None
risk_df = None
narratives_df = None

# --- HELPER FUNCTIONS ---
def find_file(filename, search_dirs=None):
    """Chercher un fichier dans plusieurs répertoires"""
    if search_dirs is None:
        search_dirs = ['.', 'model', 'data', 'model/data', '../model', '../data']
    
    for directory in search_dirs:
        path = os.path.join(directory, filename)
        if os.path.exists(path):
            return path
        # Essayer aussi avec des variantes
        if 'narrative' in filename.lower():
            # Chercher des fichiers similaires
            for f in os.listdir(directory):
                if 'narrative' in f.lower() and f.endswith('.csv'):
                    return os.path.join(directory, f)
    return None

# --- LOAD DATA ON STARTUP ---
@app.on_event("startup")
def load_resources():
    global model, risk_df, narratives_df
    print("🔍 Chargement des ressources AI...")
    print(f"📁 Répertoire actuel: {os.getcwd()}")
    
    # 1. Charger le modèle ML
    model_path = find_file('bot_detector.pkl')
    if model_path:
        try:
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            print(f"✅ Modèle chargé depuis: {model_path}")
        except Exception as e:
            print(f"❌ Erreur chargement modèle: {e}")
    else:
        print("⚠️ Modèle non trouvé. Créer bot_detector.pkl d'abord.")
        # Créer un modèle factice pour les tests
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.linear_model import LogisticRegression
        import numpy as np
        
        # Modèle factice
        vectorizer = TfidfVectorizer(max_features=100)
        dummy_model = LogisticRegression()
        
        # Entraîner sur données factices
        dummy_texts = ["bon token", "scam alert", "good project", "fake news"]
        dummy_labels = [0, 1, 0, 1]
        X = vectorizer.fit_transform(dummy_texts)
        dummy_model.fit(X, dummy_labels)
        
        model = {
            'vectorizer': vectorizer,
            'classifier': dummy_model,
            'predict': lambda texts: dummy_model.predict(vectorizer.transform(texts)),
            'predict_proba': lambda texts: dummy_model.predict_proba(vectorizer.transform(texts))
        }
        print("✅ Modèle factice créé pour tests")

    # 2. Charger les données de risque
    risk_path = find_file('final_risk_scores.csv')
    if risk_path:
        try:
            risk_df = pd.read_csv(risk_path)
            print(f"✅ Données risque chargées: {len(risk_df)} tokens")
            print(f"   Colonnes: {risk_df.columns.tolist()}")
        except Exception as e:
            print(f"❌ Erreur chargement risque: {e}")
            # Créer données factices
            risk_df = pd.DataFrame({
                'token_id': ['NEURA', 'TAO', 'RNDR', 'AGIX', 'FET'],
                'risk_score': [0.8, 0.6, 0.4, 0.7, 0.5],
                'label': ['HIGH', 'MEDIUM', 'LOW', 'HIGH', 'MEDIUM'],
                'reason': ['Volume suspect', 'Activité normale', 'Faible risque', 'Manipulation détectée', 'Risque modéré']
            })
    else:
        print("⚠️ Données risque non trouvées. Utilisation données factices.")
        risk_df = pd.DataFrame({
            'token_id': ['NEURA', 'TAO', 'RNDR', 'AGIX', 'FET'],
            'risk_score': [0.8, 0.6, 0.4, 0.7, 0.5],
            'label': ['HIGH', 'MEDIUM', 'LOW', 'HIGH', 'MEDIUM'],
            'reason': ['Volume suspect', 'Activité normale', 'Faible risque', 'Manipulation détectée', 'Risque modéré']
        })

    # 3. Charger les narratifs
    narrative_path = find_file('ai_generated_narratives.csv') or find_file('all_generated_narratives.csv')
    if narrative_path:
        try:
            narratives_df = pd.read_csv(narrative_path)
            print(f"✅ Narratifs chargés: {len(narratives_df)} entrées")
        except Exception as e:
            print(f"❌ Erreur chargement narratifs: {e}")
            narratives_df = None
    else:
        print("⚠️ Narratifs non trouvés")
        # Créer narratifs factices
        narratives_df = pd.DataFrame({
            'token_id': ['NEURA', 'NEURA', 'TAO', 'RNDR'],
            'topic': ['AI Revolution', 'Market Manipulation', 'Decentralized AI', 'GPU Rendering'],
            'start_time': ['2024-01-01', '2024-01-02', '2024-01-01', '2024-01-03'],
            'end_time': ['2024-01-10', '2024-01-05', '2024-01-15', '2024-01-10'],
            'sentiment': ['positive', 'negative', 'positive', 'neutral']
        })

def clean_text(text):
    """Nettoyer le texte pour l'analyse"""
    if not isinstance(text, str): 
        return ""
    return re.sub(r'[^\w\s]', '', text.lower())

# --- DATA MODELS ---
class PostAnalysisRequest(BaseModel):
    text: str

# --- ENDPOINTS ---

@app.get("/")
def root():
    return {
        "status": "active",
        "service": "TrendAI ML API",
        "model_loaded": model is not None,
        "risk_data_loaded": risk_df is not None,
        "narratives_loaded": narratives_df is not None
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "ML API"}

@app.get("/risk/{token_id}")
def get_token_risk(token_id: str):
    """Obtenir le score de risque pour un token"""
    if risk_df is None:
        raise HTTPException(503, "Données risque non chargées")
    
    token_upper = token_id.upper()
    
    # Chercher le token
    token_data = risk_df[risk_df['token_id'] == token_upper]
    if token_data.empty:
        # Essayer d'autres colonnes
        for col in risk_df.columns:
            if col != 'token_id' and risk_df[col].dtype == 'object':
                token_data = risk_df[risk_df[col].str.upper() == token_upper]
                if not token_data.empty:
                    break
    
    if token_data.empty:
        # Retourner une valeur par défaut
        return {
            "token": token_upper,
            "risk_level": "UNKNOWN",
            "risk_score": 0.5,
            "reason": "Token non trouvé dans la base",
            "active_narratives": []
        }
    
    risk_row = token_data.iloc[0]
    
    # Obtenir les narratifs si disponibles
    narratives = []
    if narratives_df is not None:
        token_narratives = narratives_df[narratives_df['token_id'] == token_upper]
        if not token_narratives.empty:
            narratives = token_narratives.to_dict('records')
    
    return {
        "token": token_upper,
        "risk_level": str(risk_row.get('label', 'UNKNOWN')),
        "risk_score": float(risk_row.get('risk_score', 0.5)),
        "reason": str(risk_row.get('reason', 'No data')),
        "active_narratives": narratives
    }

@app.get("/rankings/high-risk")
def get_high_risk_tokens(limit: int = 5):
    """Tokens les plus risqués"""
    if risk_df is None:
        return []
    
    try:
        # Trier par risque
        risk_df['risk_score'] = pd.to_numeric(risk_df['risk_score'], errors='coerce')
        top_risky = risk_df.sort_values('risk_score', ascending=False).head(limit)
        return top_risky.to_dict('records')
    except:
        # Retourner les premiers tokens
        return risk_df.head(limit).to_dict('records')

@app.post("/analyze")
def analyze_post(request: PostAnalysisRequest):
    """Analyse de texte en temps réel"""
    if model is None:
        raise HTTPException(503, "Modèle non chargé")
    
    try:
        # Nettoyer le texte
        clean = clean_text(request.text)
        
        # Prédiction
        if isinstance(model, dict):  # Modèle factice
            pred = model['predict']([clean])[0]
            proba = model['predict_proba']([clean])[0]
        else:  # Modèle réel
            pred = model.predict([clean])[0]
            proba = model.predict_proba([clean])[0]
        
        # Calculer le score de suspicion (probabilité classe 1)
        suspicion_score = float(proba[1]) if len(proba) > 1 else 0.5
        
        return {
            "text": request.text[:100] + ("..." if len(request.text) > 100 else ""),
            "prediction": "SUSPICIOUS" if pred == 1 else "ORGANIC",
            "suspicion_score": round(suspicion_score, 4),
            "is_bot": bool(pred == 1),
            "analysis": "Texte suspect détecté" if pred == 1 else "Texte organique normal"
        }
    except Exception as e:
        raise HTTPException(500, f"Erreur analyse: {str(e)}")

@app.get("/debug/files")
def debug_files():
    """Endpoint de débogage pour voir les fichiers disponibles"""
    files_info = {}
    
    for root, dirs, files in os.walk('.'):
        if root.startswith('./.') or '__pycache__' in root:
            continue
        
        csv_files = [f for f in files if f.endswith('.csv')]
        pkl_files = [f for f in files if f.endswith('.pkl')]
        
        if csv_files or pkl_files:
            files_info[root] = {
                'csv': csv_files,
                'pkl': pkl_files
            }
    
    return {
        "current_dir": os.getcwd(),
        "files": files_info,
        "loaded": {
            "model": model is not None,
            "risk_data": risk_df is not None,
            "narratives": narratives_df is not None
        }
    }

# Démarrer directement si exécuté
if __name__ == "__main__":
    import uvicorn
    print("🚀 Démarrage API ML sur port 8001...")
    uvicorn.run(app, host="0.0.0.0", port=8001)