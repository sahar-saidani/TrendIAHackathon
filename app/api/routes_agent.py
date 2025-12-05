from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.agent import simple_watchdog_answer
from app.services.risk_engine import compute_token_risk

router = APIRouter(prefix="/agent", tags=["agent"])

@router.post("/query")
def query_agent(token_id: str, db: Session = Depends(get_db)):
    # compute risk first (ensures DB updated)
    risk_obj = compute_token_risk(db, token_id)
    answer = simple_watchdog_answer(token_id, risk_obj)
    return answer
