"""
Service ML pour intégrer le modèle de détection de bots
"""
import pickle
import pandas as pd
import re
from typing import Dict, List, Any
from datetime import datetime
import numpy as np
from pathlib import Path
from app.core.config import ML_MODEL_PATH, RISK_SCORES_PATH, NARRATIVES_PATH

class MLService:
    def __init__(self, model_path: str = None):
         if model_path is None:
             model_path = str("model/bot_detector.pkl")
             
             self.model = None
             self.vectorizer = None
             self.load_model(model_path)
        
            # Charger les données de risque pré-calculées
             self.risk_scores = None
             self.narratives = None
             self.load_precomputed_data()
    
    def load_model(self, model_path: str):
        """Charge le modèle ML entraîné"""
        try:
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            print(f"✅ Modèle ML chargé depuis {model_path}")
        except Exception as e:
            print(f"⚠️ Erreur de chargement du modèle: {e}")
            self.model = None
    
    def load_precomputed_data(self):
        """Charge les données pré-calculées"""
        try:
            self.risk_scores = pd.read_csv("model/final_risk_scores.csv")
            print("✅ Scores de risque chargés")
        except:
            print("⚠️ final_risk_scores.csv non trouvé")
            self.risk_scores = None
        
        try:
            self.narratives = pd.read_csv("model/ai_generated_narratives.csv")
            print("✅ Narratives chargées")
        except:
            print("⚠️ ai_generated_narratives.csv non trouvé")
            self.narratives = None
    
    def clean_text(self, text: str) -> str:
        """Nettoie le texte (identique à l'entraînement)"""
        if not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r'http\S+', '', text)  # Remove URLs
        text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
        return text
    
    def predict_post(self, text: str) -> Dict[str, Any]:
        """Prédit si un post est organique ou suspect"""
        if self.model is None:
            return {
                "prediction": "ORGANIC",
                "suspicion_score": 0.0,
                "confidence": 0.5,
                "error": "Model not loaded"
            }
        
        clean_text = self.clean_text(text)
        
        try:
            # Prédiction
            prediction = self.model.predict([clean_text])[0]
            probabilities = self.model.predict_proba([clean_text])[0]
            
            suspicion_score = float(probabilities[1])  # Probabilité d'être suspect
            
            return {
                "prediction": "SUSPICIOUS" if prediction == 1 else "ORGANIC",
                "suspicion_score": round(suspicion_score, 4),
                "confidence": round(max(probabilities), 4),
                "is_bot": bool(prediction == 1),
                "clean_text": clean_text[:100] + "..." if len(clean_text) > 100 else clean_text
            }
        except Exception as e:
            print(f"Erreur de prédiction: {e}")
            return {
                "prediction": "ORGANIC",
                "suspicion_score": 0.0,
                "confidence": 0.0,
                "error": str(e)
            }
    
    def get_token_risk(self, token_id: str) -> Dict[str, Any]:
        """Récupère le risque pré-calculé d'un token"""
        if self.risk_scores is None:
            return {
                "token_id": token_id,
                "risk_score": 0.0,
                "label": "UNKNOWN",
                "reason": "Risk data not loaded",
                "total_posts": 0,
                "suspicious_posts": 0
            }
        
        token_risk = self.risk_scores[self.risk_scores['token_id'] == token_id.upper()]
        
        if token_risk.empty:
            return {
                "token_id": token_id,
                "risk_score": 0.0,
                "label": "NOT_FOUND",
                "reason": f"Token {token_id} not found in database",
                "total_posts": 0,
                "suspicious_posts": 0
            }
        
        risk_data = token_risk.iloc[0].to_dict()
        
        # Récupère les narratives pour ce token
        narratives = []
        if self.narratives is not None:
            token_narratives = self.narratives[self.narratives['token_id'] == token_id.upper()]
            narratives = token_narratives[['narrative_id', 'topic', 'start_time', 'end_time']].to_dict('records')
        
        return {
            "token_id": token_id.upper(),
            "risk_score": float(risk_data.get('risk_score', 0)),
            "label": risk_data.get('label', 'SAFE'),
            "reason": risk_data.get('reason', 'No data'),
            "total_posts": int(risk_data.get('total_posts', 0)),
            "suspicious_posts": int(risk_data.get('suspicious_posts', 0)),
            "suspicious_percentage": round(float(risk_data.get('risk_score', 0)) / 100, 4),
            "narratives": narratives[:5],  # Limite à 5 narratives
            "last_updated": datetime.now().isoformat()
        }
    
    def analyze_multiple_posts(self, posts: List[Dict[str, str]]) -> Dict[str, Any]:
        """Analyse plusieurs posts à la fois"""
        if not posts:
            return {"total": 0, "suspicious": 0, "score": 0.0}
        
        results = []
        suspicious_count = 0
        
        for post in posts:
            text = post.get('text', '')
            token = post.get('token_id', 'UNKNOWN')
            post_id = post.get('post_id', '')
            
            prediction = self.predict_post(text)
            
            result = {
                "post_id": post_id,
                "token_id": token,
                "text_preview": text[:50] + "..." if len(text) > 50 else text,
                **prediction
            }
            
            results.append(result)
            
            if prediction.get('is_bot', False):
                suspicious_count += 1
        
        # Calcul du score global
        total_posts = len(posts)
        risk_score = (suspicious_count / total_posts) * 100 if total_posts > 0 else 0
        
        return {
            "total_posts": total_posts,
            "suspicious_posts": suspicious_count,
            "risk_score": round(risk_score, 2),
            "suspicious_percentage": round(risk_score / 100, 4),
            "analysis": results,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_risk_rankings(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retourne le classement des tokens par risque"""
        if self.risk_scores is None:
            return []
        
        rankings = self.risk_scores.sort_values('risk_score', ascending=False).head(limit)
        
        result = []
        for _, row in rankings.iterrows():
            result.append({
                "rank": len(result) + 1,
                "token_id": row['token_id'],
                "risk_score": float(row['risk_score']),
                "label": row['label'],
                "reason": row.get('reason', ''),
                "total_posts": int(row.get('total_posts', 0)),
                "suspicious_posts": int(row.get('suspicious_posts', 0))
            })
        
        return result

# Instance globale
ml_service = MLService()