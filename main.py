from fastapi import FastAPI
from contextlib import asynccontextmanager
import threading
import time
import requests
import sys
import os

# Ajouter agents au path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

# Lifespan manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestion du cycle de vie de l'application"""
    print("🚀 Démarrage du système TrendAI...")
    yield
    print("🛑 Arrêt du système TrendAI...")

# Création de l'app FastAPI principale
app = FastAPI(
    title="TrendAI API",
    version="2.0",
    description="Système complet de détection de manipulation de marché",
    lifespan=lifespan
)

# Routes principales
@app.get("/")
async def root():
    return {
        "status": "active",
        "service": "TrendAI Backend Principal",
        "version": "2.0",
        "endpoints": {
            "health": "/health",
            "api_docs": "/docs",
            "analyze_post": "/api/analyze (POST)",
            "token_risk": "/api/risk/{token_id}",
            "high_risk": "/api/rankings/high-risk",
            "predictions": "/api/predict/{token_id}",
            "early_warnings": "/api/early-warning/{token_id}",
            "correlation": "/api/correlation/sentiment-price/{token_id}",
            "market_insights": "/api/market/insights"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "service": "TrendAI Main API"
    }

# Importer dynamiquement les fonctions d'agent
def get_agent_functions():
    """Importer les fonctions d'agent dynamiquement"""
    try:
        from agents.prediction_agent import (
            get_price_prediction,
            get_correlation_analysis,
            get_early_warning_signals,
            get_market_insights
        )
        return {
            "get_price_prediction": get_price_prediction,
            "get_correlation_analysis": get_correlation_analysis,
            "get_early_warning_signals": get_early_warning_signals,
            "get_market_insights": get_market_insights
        }
    except ImportError as e:
        print(f"⚠️ Erreur import agents: {e}")
        # Retourner des fonctions factices
        def dummy_prediction(token_id, horizon="24h"):
            return {"error": "Agent non disponible", "token": token_id}
        
        return {
            "get_price_prediction": dummy_prediction,
            "get_correlation_analysis": lambda x: {"error": "Agent non disponible"},
            "get_early_warning_signals": lambda x: {"error": "Agent non disponible"},
            "get_market_insights": lambda: {"error": "Agent non disponible"}
        }

# Obtenir les fonctions d'agent
agent_funcs = get_agent_functions()

# Routes d'API
@app.post("/api/analyze")
async def proxy_analyze_post(request: dict):
    """Analyser du texte (via API ML si disponible)"""
    try:
        response = requests.post(
            "http://localhost:8001/analyze",
            json=request,
            timeout=10
        )
        return response.json()
    except:
        # Fallback local
        text = request.get("text", "")
        return {
            "text": text[:100],
            "prediction": "ORGANIC" if len(text) > 20 else "SUSPICIOUS",
            "suspicion_score": 0.3 if len(text) > 20 else 0.7,
            "is_bot": False,
            "source": "fallback"
        }

@app.get("/api/risk/{token_id}")
async def proxy_get_token_risk(token_id: str):
    """Risque d'un token"""
    try:
        response = requests.get(
            f"http://localhost:8001/risk/{token_id}",
            timeout=10
        )
        return response.json()
    except:
        # Données factices
        return {
            "token": token_id.upper(),
            "risk_level": "MEDIUM",
            "risk_score": 0.5,
            "reason": "Données non disponibles",
            "active_narratives": []
        }

@app.get("/api/rankings/high-risk")
async def proxy_get_high_risk_tokens():
    """Tokens à haut risque"""
    try:
        response = requests.get(
            "http://localhost:8001/rankings/high-risk",
            timeout=10
        )
        return response.json()
    except:
        return [
            {"token_id": "NEURA", "risk_score": 0.85, "label": "HIGH"},
            {"token_id": "VXV", "risk_score": 0.77, "label": "HIGH"},
            {"token_id": "AGIX", "risk_score": 0.73, "label": "HIGH"}
        ]

@app.get("/api/predict/{token_id}")
async def get_prediction(token_id: str, horizon: str = "24h"):
    """Prédiction de prix"""
    return agent_funcs["get_price_prediction"](token_id, horizon)

@app.get("/api/early-warning/{token_id}")
async def get_early_warning(token_id: str):
    """Signaux d'alerte précoce"""
    return agent_funcs["get_early_warning_signals"](token_id)

@app.get("/api/correlation/sentiment-price/{token_id}")
async def get_correlation_sentiment_price(token_id: str):
    """Corrélation sentiment vs prix"""
    return agent_funcs["get_correlation_analysis"](token_id)

@app.get("/api/market/insights")
async def get_market_insights():
    """Insights du marché"""
    return agent_funcs["get_market_insights"]()

@app.get("/api/predictions/batch")
async def get_batch_predictions(tokens: str = "NEURA,TAO,RNDR", horizon: str = "24h"):
    """Prédictions batch"""
    token_list = [t.strip() for t in tokens.split(",")]
    results = []
    for token in token_list:
        results.append(agent_funcs["get_price_prediction"](token, horizon))
    return {"predictions": results}

# Démarrer directement
if __name__ == "__main__":
    import uvicorn
    print("============================================================")
    print("       🤖 TRENDIA FAKE NEWS DETECTION SYSTEM")
    print("============================================================")
    print("🚀 Démarrage du backend principal...")
    print("📡 URL: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    print("============================================================")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )