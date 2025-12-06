"""
Agent de prédiction pour TrendAI
Prédit les mouvements de prix basé sur le sentiment
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from typing import Dict, List, Tuple

def get_price_prediction(token_id: str, horizon: str = "24h") -> Dict:
    """
    Prédire le mouvement de prix d'un token
    
    Args:
        token_id: Symbole du token (ex: NEURA)
        horizon: Horizon de prédiction (6h, 24h, 7d)
    
    Returns:
        Dict avec prédiction et métadonnées
    """
    # Mapping des horizons
    horizon_map = {
        "6h": {"periods": 6, "volatility": 0.03},
        "24h": {"periods": 24, "volatility": 0.05},
        "7d": {"periods": 168, "volatility": 0.15}
    }
    
    if horizon not in horizon_map:
        horizon = "24h"
    
    # Facteurs simulés basés sur le token
    token_factors = {
        "NEURA": {"momentum": 0.7, "sentiment": 0.8, "risk": 0.6},
        "TAO": {"momentum": 0.5, "sentiment": 0.6, "risk": 0.4},
        "RNDR": {"momentum": 0.6, "sentiment": 0.7, "risk": 0.5},
        "AGIX": {"momentum": 0.4, "sentiment": 0.5, "risk": 0.3},
        "FET": {"momentum": 0.5, "sentiment": 0.6, "risk": 0.4},
        "OCEAN": {"momentum": 0.5, "sentiment": 0.5, "risk": 0.5},
        "NMR": {"momentum": 0.4, "sentiment": 0.4, "risk": 0.4},
        "VXV": {"momentum": 0.6, "sentiment": 0.6, "risk": 0.7}
    }
    
    # Récupérer les facteurs du token ou utiliser des valeurs par défaut
    token_upper = token_id.upper()
    factors = token_factors.get(token_upper, {
        "momentum": 0.5,
        "sentiment": 0.5,
        "risk": 0.5
    })
    
    # Calculer la prédiction
    base_return = np.random.normal(0, horizon_map[horizon]["volatility"])
    sentiment_boost = factors["sentiment"] * 0.02
    momentum_boost = factors["momentum"] * 0.01
    
    predicted_return = base_return + sentiment_boost + momentum_boost
    
    # Déterminer la direction
    direction = "UP" if predicted_return > 0 else "DOWN"
    confidence = min(0.95, abs(predicted_return) * 10)
    
    # Générer des features pour l'explication
    features = {
        "sentiment_score": round(factors["sentiment"], 2),
        "momentum_score": round(factors["momentum"], 2),
        "risk_score": round(factors["risk"], 2),
        "social_volume": random.randint(1000, 10000),
        "volatility_24h": round(random.uniform(0.02, 0.08), 3)
    }
    
    # Générer des alertes si nécessaire
    warnings = []
    if factors["risk"] > 0.7:
        warnings.append("Risque élevé de manipulation détecté")
    if abs(predicted_return) > 0.1:
        warnings.append(f"Mouvement important attendu ({direction})")
    
    # Générer une explication
    if direction == "UP":
        explanation = f"Analyse pour {token_upper} ({horizon}): Sentiment positif ({features['sentiment_score']}/1.0), Momentum favorable ({features['momentum_score']}/1.0). Volume social: {features['social_volume']} posts. Recommandation: Surveillance pour entrée potentielle."
    else:
        explanation = f"Analyse pour {token_upper} ({horizon}): Sentiment mitigé ({features['sentiment_score']}/1.0), Momentum faible ({features['momentum_score']}/1.0). Volatilité: {features['volatility_24h']*100}%. Recommandation: Attendre confirmation."
    
    return {
        "token": token_upper,
        "horizon": horizon,
        "predicted_return": round(predicted_return * 100, 2),  # en pourcentage
        "direction": direction,
        "confidence": round(confidence, 2),
        "features": features,
        "warnings": warnings,
        "explanation": explanation,
        "timestamp": datetime.now().isoformat()
    }

def get_batch_predictions(tokens: List[str], horizon: str = "24h") -> List[Dict]:
    """Prédictions pour plusieurs tokens"""
    return [get_price_prediction(token, horizon) for token in tokens]

def get_correlation_analysis(token_id: str) -> Dict:
    """Analyse de corrélation entre sentiment et prix"""
    # Données simulées
    correlations = {
        "sentiment_price": round(random.uniform(0.3, 0.9), 3),
        "volume_volatility": round(random.uniform(0.4, 0.8), 3),
        "lag_optimal": random.choice(["1h", "3h", "6h"]),
        "r_squared": round(random.uniform(0.2, 0.7), 3)
    }
    
    return {
        "token": token_id.upper(),
        "analysis": "correlation",
        "correlations": correlations,
        "insight": "Le sentiment précède généralement les mouvements de prix",
        "strength": "forte" if correlations["sentiment_price"] > 0.7 else "modérée",
        "timestamp": datetime.now().isoformat()
    }

def get_early_warning_signals(token_id: str) -> Dict:
    """Signaux d'alerte précoce"""
    signals = []
    token_upper = token_id.upper()
    
    # Générer des signaux aléatoires
    if random.random() > 0.5:
        signals.append({
            "type": "bullish_divergence",
            "confidence": round(random.uniform(0.6, 0.9), 2),
            "description": "Sentiment en hausse mais prix stagnant",
            "action": "Surveiller pour entrée potentielle"
        })
    
    if random.random() > 0.7:
        signals.append({
            "type": "volume_spike",
            "confidence": round(random.uniform(0.7, 0.95), 2),
            "description": "Pic de volume sans mouvement de prix correspondant",
            "action": "Risque de manipulation"
        })
    
    if random.random() > 0.6:
        signals.append({
            "type": "sentiment_flip",
            "confidence": round(random.uniform(0.5, 0.85), 2),
            "description": "Retournement soudain du sentiment",
            "action": "Préparer à la volatilité"
        })
    
    # Ajouter des signaux spécifiques selon le token
    if token_upper == "NEURA" and random.random() > 0.4:
        signals.append({
            "type": "ai_token_volatility",
            "confidence": 0.8,
            "description": "Token AI sujet à forte volatilité",
            "action": "Positionner des stops"
        })
    
    return {
        "token": token_upper,
        "signals": signals,
        "risk_level": "HIGH" if len(signals) > 1 else "MEDIUM",
        "timestamp": datetime.now().isoformat(),
        "recommendation": "Surveillance accrue requise" if signals else "Pas d'alerte immédiate"
    }

def get_market_insights() -> Dict:
    """Insights généraux du marché"""
    ai_tokens = ["NEURA", "TAO", "RNDR", "AGIX", "FET", "OCEAN"]
    
    # Simuler des insights
    trending = random.sample(ai_tokens, 3)
    declining = random.sample([t for t in ai_tokens if t not in trending], 2)
    
    return {
        "market_trend": random.choice(["bullish", "neutral", "bearish"]),
        "trending_tokens": trending,
        "declining_tokens": declining,
        "overall_sentiment": round(random.uniform(0.3, 0.8), 2),
        "total_alerts": random.randint(0, 10),
        "high_risk_tokens": random.sample(ai_tokens, 2),
        "timestamp": datetime.now().isoformat()
    }