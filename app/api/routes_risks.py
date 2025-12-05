from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.post import Post
from app.models.risk import RiskScore
from app.schemas.risk_schema import RiskOut
from app.services import mock_pipeline
from app.services.risk_engine import compute_token_risk
from typing import List
from pydantic import BaseModel

router = APIRouter(prefix="/risks", tags=["risks"])

class BulkPosts(BaseModel):
    posts: list

@router.post("/ingest")
def ingest_posts(payload: BulkPosts, db: Session = Depends(get_db)):
    posts_in = payload.posts
    created = []

    # create Post rows and call mock analysis
    for p in posts_in:
        post = Post(
            post_id=p["post_id"],
            token_id=p["token"],
            account_id=p.get("account_id", "unknown"),
            text=p["text"],
            timestamp=p.get("timestamp"),
            type=p.get("type", "organic"),
        )
        clf = mock_pipeline.classify_post(p["text"])
        post.organic_score = clf["organic_score"]
        post.label = clf["label"]
        post.bot_score = mock_pipeline.bot_score_for_post(post.account_id, post.text)
        db.add(post)
        db.commit()
        db.refresh(post)
        created.append(post)

    # clustering
    mapping = mock_pipeline.cluster_posts([{"post_id": c.post_id, "text": c.text} for c in created])
    for c in created:
        if c.post_id in mapping:
            c.cluster_id = mapping[c.post_id]
            db.add(c)
    db.commit()

    # recompute risk for affected tokens
    affected = set([c.token_id for c in created])
    for token in affected:
        compute_token_risk(db, token)

    return {"ingested": len(created)}

@router.get("/{token_id}", response_model=RiskOut)
def get_risk_by_token(token_id: str, db: Session = Depends(get_db)):
    # compute/update risk on demand
    r = compute_token_risk(db, token_id)
    return {
        "token_id": token_id,
        "score": r["score"],
        "label": r["label"],
        "reason": r["reason"],
        "updated_at": r["updated_at"]
    }

@router.get("/{token_id}/posts", response_model=List[dict])
def get_posts_by_token(token_id: str, db: Session = Depends(get_db)):
    posts = db.query(Post).filter(Post.token_id == token_id).order_by(Post.timestamp.desc()).all()
    return [{"post_id": p.post_id, "text": p.text, "label": p.label, "organic_score": p.organic_score, "bot_score": p.bot_score, "cluster_id": p.cluster_id, "account_id": p.account_id, "type": p.type, "timestamp": p.timestamp} for p in posts]
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.post import Post
from app.models.risk import RiskScore
from app.schemas.risk_schema import RiskOut
from app.services import mock_pipeline
from app.services.risk_engine import compute_token_risk
from typing import List
from pydantic import BaseModel

router = APIRouter(prefix="/risks", tags=["risks"])

class BulkPosts(BaseModel):
    posts: list

@router.post("/ingest")
def ingest_posts(payload: BulkPosts, db: Session = Depends(get_db)):
    posts_in = payload.posts
    created = []

    # create Post rows and call mock analysis
    for p in posts_in:
        post = Post(
            post_id=p["post_id"],
            token_id=p["token"],
            account_id=p.get("account_id", "unknown"),
            text=p["text"],
            timestamp=p.get("timestamp"),
            type=p.get("type", "organic"),
        )
        clf = mock_pipeline.classify_post(p["text"])
        post.organic_score = clf["organic_score"]
        post.label = clf["label"]
        post.bot_score = mock_pipeline.bot_score_for_post(post.account_id, post.text)
        db.add(post)
        db.commit()
        db.refresh(post)
        created.append(post)

    # clustering
    mapping = mock_pipeline.cluster_posts([{"post_id": c.post_id, "text": c.text} for c in created])
    for c in created:
        if c.post_id in mapping:
            c.cluster_id = mapping[c.post_id]
            db.add(c)
    db.commit()

    # recompute risk for affected tokens
    affected = set([c.token_id for c in created])
    for token in affected:
        compute_token_risk(db, token)

    return {"ingested": len(created)}

@router.get("/{token_id}", response_model=RiskOut)
def get_risk_by_token(token_id: str, db: Session = Depends(get_db)):
    # compute/update risk on demand
    r = compute_token_risk(db, token_id)
    return {
        "token_id": token_id,
        "score": r["score"],
        "label": r["label"],
        "reason": r["reason"],
        "updated_at": r["updated_at"]
    }

@router.get("/{token_id}/posts", response_model=List[dict])
def get_posts_by_token(token_id: str, db: Session = Depends(get_db)):
    posts = db.query(Post).filter(Post.token_id == token_id).order_by(Post.timestamp.desc()).all()
    return [{"post_id": p.post_id, "text": p.text, "label": p.label, "organic_score": p.organic_score, "bot_score": p.bot_score, "cluster_id": p.cluster_id, "account_id": p.account_id, "type": p.type, "timestamp": p.timestamp} for p in posts]
