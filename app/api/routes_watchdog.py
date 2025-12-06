"""
Routes pour l'Agent Watchdog - Endpoints avancés d'analyse narrative
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, List
import json

from app.core.database import get_db
from app.services.agent_service import NarrativeWatchdogAgent, simple_watchdog_answer
from app.services.risk_engine import compute_token_risk
from app.models.post import Post

router = APIRouter(prefix="/watchdog", tags=["watchdog"])

@router.post("/analyze/{token_id}")
def analyze_token_narrative(token_id: str, db: Session = Depends(get_db)):
    """
    Analyse narrative complète d'un token
    """
    try:
        # 1. Calcule le risque actuel
        risk_data = compute_token_risk(db, token_id)
        
        # 2. Récupère les posts récents du token
        posts = db.query(Post).filter(Post.token_id == token_id).order_by(Post.timestamp.desc()).limit(100).all()
        
        posts_data = [
            {
                "post_id": p.post_id,
                "text": p.text,
                "account_id": p.account_id,
                "timestamp": p.timestamp.isoformat() if p.timestamp else None,
                "label": p.label,
                "organic_score": p.organic_score,
                "bot_score": p.bot_score,
                "cluster_id": p.cluster_id,
                "type": p.type
            }
            for p in posts
        ]
        
        # 3. Lance l'analyse narrative
        agent = NarrativeWatchdogAgent(db)
        narrative_report = agent.analyze_token_narrative(
            token_id=token_id,
            risk_data=risk_data,
            posts_data=posts_data
        )
        
        # 4. Version simplifiée pour compatibilité
        simple_answer = simple_watchdog_answer(token_id, risk_data)
        
        return {
            "status": "success",
            "token_id": token_id,
            "simple_summary": simple_answer,
            "narrative_report": narrative_report,
            "posts_analyzed": len(posts_data),
            "analysis_timestamp": narrative_report["generated_at"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'analyse: {str(e)}")

@router.get("/dashboard/{token_id}")
def get_watchdog_dashboard(token_id: str, db: Session = Depends(get_db)):
    """
    Tableau de bord complet pour l'agent watchdog
    """
    try:
        # Version simplifiée pour démo rapide
        risk_data = compute_token_risk(db, token_id)
        agent_response = simple_watchdog_answer(token_id, risk_data)
        
        # Récupère les statistiques de base
        total_posts = db.query(Post).filter(Post.token_id == token_id).count()
        suspicious_posts = db.query(Post).filter(
            Post.token_id == token_id, 
            Post.label == "Suspicious"
        ).count()
        
        # Derniers posts
        recent_posts = db.query(Post).filter(
            Post.token_id == token_id
        ).order_by(Post.timestamp.desc()).limit(5).all()
        
        recent_posts_data = [
            {
                "id": p.post_id,
                "text": p.text[:100] + "..." if len(p.text) > 100 else p.text,
                "account": p.account_id,
                "risk_score": p.bot_score,
                "label": p.label,
                "time": p.timestamp.isoformat() if p.timestamp else None
            }
            for p in recent_posts
        ]
        
        return {
            "token": token_id,
            "risk_overview": {
                "score": risk_data["score"],
                "label": risk_data["label"],
                "reason": risk_data["reason"],
                "urgency": agent_response["urgency"]
            },
            "statistics": {
                "total_posts": total_posts,
                "suspicious_posts": suspicious_posts,
                "suspicious_ratio": suspicious_posts / total_posts if total_posts > 0 else 0,
                "last_updated": risk_data["updated_at"].isoformat() if risk_data.get("updated_at") else None
            },
            "agent_insights": {
                "summary": agent_response["answer"],
                "recommendation": agent_response["recommendation"]
            },
            "recent_activity": recent_posts_data,
            "actions": [
                {
                    "id": "view_details",
                    "label": "Voir l'analyse détaillée",
                    "endpoint": f"/watchdog/analyze/{token_id}"
                },
                {
                    "id": "view_posts",
                    "label": "Voir tous les posts",
                    "endpoint": f"/risks/{token_id}/posts"
                }
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur du dashboard: {str(e)}")

@router.post("/bulk-analyze")
def bulk_analyze_tokens(token_ids: List[str], db: Session = Depends(get_db)):
    """
    Analyse multiple de tokens (pour comparaison)
    """
    results = []
    
    for token_id in token_ids[:10]:  # Limite à 10 tokens
        try:
            risk_data = compute_token_risk(db, token_id)
            agent_response = simple_watchdog_answer(token_id, risk_data)
            
            results.append({
                "token_id": token_id,
                "risk_score": risk_data["score"],
                "risk_label": risk_data["label"],
                "urgency": agent_response["urgency"],
                "recommendation": agent_response["recommendation"]
            })
        except Exception as e:
            results.append({
                "token_id": token_id,
                "error": str(e),
                "risk_score": None,
                "risk_label": "Error"
            })
    
    # Trie par risque décroissant
    results_sorted = sorted(
        [r for r in results if r.get("risk_score") is not None],
        key=lambda x: x["risk_score"],
        reverse=True
    )
    
    return {
        "analyzed_tokens": len(results),
        "high_risk_count": len([r for r in results_sorted if r.get("risk_score", 0) > 70]),
        "results": results_sorted,
        "top_risk": results_sorted[0] if results_sorted else None
    }