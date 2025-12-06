from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.post import Post
from app.models.risk import RiskScore
from datetime import datetime

def compute_token_risk(db: Session, token_id: str):
    total_posts = db.query(func.count(Post.id)).filter(Post.token_id == token_id).scalar() or 0
    if total_posts == 0:
        # if there are no posts, create or update an entry with 0 score
        rs = db.query(RiskScore).filter(RiskScore.token_id == token_id).first()
        if rs:
            rs.score = 0.0
            rs.label = "Safe"
            rs.reason = "No posts"
            rs.updated_at = datetime.utcnow()
        else:
            rs = RiskScore(token_id=token_id, score=0.0, label="Safe", reason="No posts", updated_at=datetime.utcnow())
            db.add(rs)
        db.commit()
        db.refresh(rs)
        return {"score": rs.score, "label": rs.label, "reason": rs.reason, "updated_at": rs.updated_at}

    suspicious_count = db.query(func.count(Post.id)).filter(Post.token_id == token_id, Post.label == "Suspicious").scalar() or 0
    duplicate_count = db.query(func.count(Post.id)).filter(Post.token_id == token_id, Post.cluster_id != None).scalar() or 0
    suspicious_frac = suspicious_count / total_posts
    duplicate_frac = duplicate_count / total_posts

    mean_bot = db.query(func.avg(Post.bot_score)).filter(Post.token_id == token_id).scalar() or 0.0

    # tunable weighted formula
    risk_raw = (duplicate_frac * 0.5 + suspicious_frac * 0.35 + mean_bot * 0.15)
    score = min(100, round(risk_raw * 100, 2))

    if score <= 30:
        label = "Safe"
    elif score <= 65:
        label = "Suspicious"
    else:
        label = "High Risk"

    reasons = []
    if duplicate_frac > 0.2:
        reasons.append(f"High duplication ratio ({duplicate_frac:.2f})")
    if suspicious_frac > 0.2:
        reasons.append(f"Many suspicious posts ({suspicious_frac:.2f})")
    if mean_bot > 0.4:
        reasons.append(f"High bot-like activity (avg bot_score {mean_bot:.2f})")
    reason_text = "; ".join(reasons) if reasons else "Signals normal"

    rs = db.query(RiskScore).filter(RiskScore.token_id == token_id).first()
    if rs:
        rs.score = score
        rs.label = label
        rs.reason = reason_text
        rs.updated_at = datetime.utcnow()
    else:
        rs = RiskScore(token_id=token_id, score=score, label=label, reason=reason_text, updated_at=datetime.utcnow())
        db.add(rs)
    db.commit()
    db.refresh(rs)
    return {"score": score, "label": label, "reason": reason_text, "updated_at": rs.updated_at}
