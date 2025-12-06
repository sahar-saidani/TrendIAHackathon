# app/api/routes_ml.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.core.database import get_db
from app.services.ml_integration import FakeNewsDetector

router = APIRouter(prefix="/api/ml", tags=["ML Integration"])

@router.post("/detect")
async def detect_fake_news(
    data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """
    Détecte les fake news dans un texte
    """
    text = data.get("text", "")
    if not text:
        raise HTTPException(status_code=400, detail="Text is required")
    
    detector = FakeNewsDetector(db)
    result = detector.detect_fake_news(text, data.get("metadata"))
    
    return {
        "success": True,
        "data": result
    }

@router.post("/detect/batch")
async def batch_detect_fake_news(
    data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """
    Détecte les fake news dans plusieurs textes
    """
    texts = data.get("texts", [])
    if not texts:
        raise HTTPException(status_code=400, detail="Texts list is required")
    
    detector = FakeNewsDetector(db)
    result = detector.batch_detect(texts)
    
    return result

@router.get("/tokens/high-risk")
async def get_high_risk_tokens():
    """
    Récupère les tokens à haut risque depuis l'API ML
    """
    from app.main import ml_client  # Import dynamique
    
    tokens = ml_client.get_high_risk_tokens()
    
    return {
        "success": True,
        "tokens": tokens
    }

@router.get("/tokens/{token_id}")
async def get_token_risk(token_id: str):
    """
    Récupère le risque d'un token spécifique
    """
    from app.main import ml_client
    
    result = ml_client.get_token_risk(token_id)
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    
    return {
        "success": True,
        "data": result
    }

@router.get("/health")
async def ml_health_check():
    """
    Vérifie la santé de l'API ML
    """
    from app.main import ml_client
    
    try:
        # Essayer d'appeler un endpoint simple
        response = ml_client.session.get(f"{ml_client.base_url}/")
        
        return {
            "ml_api_status": "healthy" if response.status_code == 200 else "unhealthy",
            "ml_api_url": ml_client.base_url,
            "response_code": response.status_code
        }
        
    except Exception as e:
        return {
            "ml_api_status": "unreachable",
            "error": str(e),
            "ml_api_url": ml_client.base_url
        }