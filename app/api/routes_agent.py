from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.agent_service import simple_watchdog_answer
from app.services.risk_engine import compute_token_risk
from app.api.routes_watchdog import analyze_token_narrative  # Import de la nouvelle fonction

router = APIRouter(prefix="/agent", tags=["agent"])

@router.post("/query")
def query_agent(token_id: str, db: Session = Depends(get_db)):
    """
    Endpoint d'agent simple (compatibilité)
    """
    # compute risk first (ensures DB updated)
    risk_obj = compute_token_risk(db, token_id)
    answer = simple_watchdog_answer(token_id, risk_obj)
    return answer

@router.post("/advanced-query/{token_id}")
def advanced_agent_query(token_id: str, db: Session = Depends(get_db)):
    """
    Nouvel endpoint avec analyse narrative complète
    """
    return analyze_token_narrative(token_id, db)