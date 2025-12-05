from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.token_schema import TokenOut
from app.models.post import Post
from app.models.risk import RiskScore
from typing import List

router = APIRouter(prefix="/tokens", tags=["tokens"])

@router.get("", response_model=List[TokenOut])
def list_tokens(db: Session = Depends(get_db)):
    # gather token ids from posts and risk_scores
    post_tokens = db.query(Post.token_id).distinct().all()
    risk_tokens = db.query(RiskScore.token_id).distinct().all()
    tokens = set([t[0] for t in post_tokens] + [r[0] for r in risk_tokens if r[0] is not None])
    return [{"token_id": t} for t in sorted(tokens)]

@router.post("/init")
def init_token(token_id: str, db: Session = Depends(get_db)):
    # create a default risk entry if missing
    existing = db.query(RiskScore).filter(RiskScore.token_id == token_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Token already initialized")
    rs = RiskScore(token_id=token_id, score=0.0, label="Safe", reason="Initialized", updated_at=None)
    db.add(rs)
    db.commit()
    db.refresh(rs)
    return {"token_id": token_id, "status": "initialized"}
