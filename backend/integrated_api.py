"""
TrendAI Integrated Backend
FastAPI + Postgres Local + ML Model + Analysis Agent
"""

""" from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Float, Integer, String, Boolean, DateTime, JSON, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.postgresql import UUID
import pickle
import re
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from typing import Optional, List
import os
import uuid
from analysis_agent import AnalysisAgent
from sqlalchemy.orm import DeclarativeBase

app = FastAPI(title="TrendAI Integrated API", version="3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

nltk.download('vader_lexicon', quiet=True)
sia = SentimentIntensityAnalyzer()

# Chaîne de connexion Postgres (adaptez avec vos creds)
DATABASE_URL = "postgresql://postgres:admin123@localhost:5432/trendai"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass

# Modèles SQLAlchemy (tables)
class Post(Base):
    __tablename__ = 'posts'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    post_id = Column(String, nullable=False)
    token_id = Column(String, nullable=False)
    text = Column(String, nullable=False)
    post_type = Column(String, default='organic')
    is_bot = Column(Boolean, default=False)
    sentiment_score = Column(Float, default=0)
    sentiment_label = Column(String, default='Neutral')
    created_at = Column(DateTime, server_default=func.now())

class Token(Base):
    __tablename__ = 'tokens'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token_id = Column(String, unique=True, nullable=False)
    name = Column(String)
    risk_score = Column(Float, default=0)
    risk_label = Column(String, default='SAFE')
    bot_ratio = Column(Float, default=0)
    avg_sentiment = Column(Float, default=0)
    total_posts = Column(Integer, default=0)
    suspicious_posts = Column(Integer, default=0)
    reason = Column(String, default='')
    last_analyzed = Column(DateTime, server_default=func.now())

class Narrative(Base):
    __tablename__ = 'narratives'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    narrative_id = Column(String, nullable=False)
    token_id = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    risk_level = Column(String, default='LOW')
    bot_percentage = Column(Float, default=0)
    avg_sentiment = Column(Float, default=0)
    warning = Column(String, default='')
    post_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())

class Account(Base):
    __tablename__ = 'accounts'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=False)
    trust_score = Column(Float, default=50)
    trust_label = Column(String, default='NEUTRAL')
    bot_ratio = Column(Float, default=0)
    total_posts = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())

class AnalysisReport(Base):
    __tablename__ = 'analysis_reports'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token_id = Column(String, nullable=False)
    report_type = Column(String, default='FULL_ANALYSIS')
    risk_score = Column(Float, nullable=False)
    risk_label = Column(String, nullable=False)
    explanation = Column(String, nullable=False)
    key_findings = Column(JSON, default=list)
    recommendations = Column(String, default='')
    created_at = Column(DateTime, server_default=func.now())

# Dependency pour sessions DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

model = None
agent = AnalysisAgent()

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_resources()
    yield

app = FastAPI(lifespan=lifespan, title="TrendAI Integrated API", version="3.0")
def load_resources():
    global model
    print("Starting TrendAI Integrated Backend...")

    try:
        with open('bot_detector.pkl', 'rb') as f:
            model = pickle.load(f)
        print("AI Model: Loaded")
    except Exception as e:
        print(f"Warning: Could not load model - {e}")

    print("Analysis Agent: Ready")
    print("Database: Connected to Local Postgres")

    # Créer les tables si pas existantes
    Base.metadata.create_all(bind=engine)

def clean_text(text):
    if not isinstance(text, str):
        return ""
    return re.sub(r'[^\w\s]', '', text.lower())

def analyze_sentiment(text):
    score = sia.polarity_scores(text)['compound']
    if score > 0.3:
        return "Positive", score
    if score < -0.3:
        return "Negative", score
    return "Neutral", score

class TextPayload(BaseModel):
    text: str

class TokenQuery(BaseModel):
    token_id: str

@app.get("/")
def health_check():
    return {
        "status": "active",
        "version": "3.0",
        "components": {
            "ai_model": model is not None,
            "database": "Local Postgres",
            "agent": "Active"
        }
    }

@app.post("/analyze/post")
def analyze_single_post(payload: TextPayload, db: Session = Depends(get_db)):
    if model is None:
        raise HTTPException(status_code=503, detail="AI Model not available")

    clean = clean_text(payload.text)
    is_bot = model.predict([clean])[0]
    bot_prob = model.predict_proba([clean])[0][1]

    sent_label, sent_score = analyze_sentiment(payload.text)

    result = agent.generate_quick_check(
        payload.text,
        bool(is_bot == 1),
        bot_prob,
        sent_label,
        sent_score
    )

    return {
        "text_preview": payload.text[:100] + "..." if len(payload.text) > 100 else payload.text,
        "analysis": result
    }

@app.get("/analyze/token/{token_id}")
def get_token_analysis(token_id: str, db: Session = Depends(get_db)):
    try:
        token = db.query(Token).filter(Token.token_id == token_id.upper()).first()
        if not token:
            raise HTTPException(status_code=404, detail="Token not found")

        narratives = db.query(Narrative).filter(Narrative.token_id == token_id.upper()).order_by(Narrative.bot_percentage.desc()).all()
        suspicious_posts = db.query(Post).filter(Post.token_id == token_id.upper(), Post.is_bot == True).limit(5).all()

        token_data = {c.name: getattr(token, c.name) for c in token.__table__.columns if c.name != 'id'}
        narratives_list = [{c.name: getattr(n, c.name) for c in n.__table__.columns if c.name != 'id'} for n in narratives]
        suspicious_posts_list = [p.text for p in suspicious_posts]

        analysis = agent.generate_token_analysis(token_data, narratives_list, suspicious_posts_list)

        report = AnalysisReport(
            token_id=token_id.upper(),
            risk_score=analysis['risk_score'],
            risk_label=analysis['risk_label'],
            explanation=analysis['explanation'],
            key_findings=analysis['key_findings'],
            recommendations=analysis['recommendations']
        )
        db.add(report)
        db.commit()

        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

@app.get("/token/{token_id}/history")
def get_token_history(token_id: str, db: Session = Depends(get_db)):
    reports = db.query(AnalysisReport).filter(AnalysisReport.token_id == token_id.upper()).order_by(AnalysisReport.created_at.desc()).limit(10).all()
    return {
        "token_id": token_id.upper(),
        "reports": [{c.name: getattr(r, c.name) for c in r.__table__.columns if c.name != 'id'} for r in reports]
    }

@app.get("/dashboard/high-risk")
def get_high_risk_dashboard(db: Session = Depends(get_db)):
    tokens = db.query(Token).order_by(Token.risk_score.desc()).limit(10).all()
    return {
        "high_risk_tokens": [{c.name: getattr(t, c.name) for c in t.__table__.columns if c.name != 'id'} for t in tokens]
    }

@app.get("/dashboard/statistics")
def get_dashboard_statistics(db: Session = Depends(get_db)):
    total_tokens = db.query(func.count(Token.id)).scalar() or 0
    high_risk_tokens = db.query(func.count(Token.id)).filter(Token.risk_label.in_(['HIGH RISK', 'PUMP & DUMP', 'FUD ATTACK'])).scalar() or 0
    total_posts = db.query(func.count(Post.id)).scalar() or 0
    bot_posts = db.query(func.count(Post.id)).filter(Post.is_bot == True).scalar() or 0

    return {
        "total_tokens_tracked": total_tokens,
        "high_risk_tokens": high_risk_tokens,
        "total_posts_analyzed": total_posts,
        "bot_posts_detected": bot_posts
    }

@app.get("/narratives/token/{token_id}")
def get_token_narratives(token_id: str, db: Session = Depends(get_db)):
    narratives = db.query(Narrative).filter(Narrative.token_id == token_id.upper()).order_by(Narrative.bot_percentage.desc()).all()
    return {
        "token_id": token_id.upper(),
        "narratives": [{c.name: getattr(n, c.name) for c in n.__table__.columns if c.name != 'id'} for n in narratives]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) """
    
"""
TrendAI Integrated Backend - Version Finale (Hackathon Ready)
"""

""" from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import pickle
import re
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from typing import Optional

# ========================================
# INITIALISATION FASTAPI
# ========================================
app = FastAPI(
    title="TrendAI - Crypto Manipulation Detector",
    description="Analyse en temps réel des posts, tokens et comptes crypto",
    version="2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========================================
# INITIALISATION DES OUTILS
# ========================================
nltk.download('vader_lexicon', quiet=True)
sia = SentimentIntensityAnalyzer()

# Variables globales
model = None
risk_df = None
narratives_df = None
trust_df = None

# ========================================
# CHARGEMENT DES RESSOURCES AU DÉMARRAGE
# ========================================
@app.on_event("startup")
def load_resources():
    global model, risk_df, narratives_df, trust_df
    print("Starting TrendAI Backend...")

    # 1. Modèle de détection de bots
    try:
        with open('bot_detector.pkl', 'rb') as f:
            model = pickle.load(f)
        print("AI Model: Loaded (Bot Detector)")
    except Exception as e:
        print(f"Warning: bot_detector.pkl not loaded → {e}")

    # 2. Données de risque
    for name, file, var in [
        ("Token Risk", 'final_risk_scores.csv', risk_df),
        ("Narrative Risk", 'final_narrative_risk.csv', narratives_df),
        ("Account Trust", 'final_account_trust.csv', trust_df)
    ]:
        try:
            df = pd.read_csv(file)
            globals()[name.lower().replace(" ", "_").rsplit("_", 1)[0] + "_df"] = df
            print(f"Data: {name} Loaded ({len(df)} lignes)")
        except Exception as e:
            print(f"Warning: {file} missing → {e}")

# ========================================
# FONCTIONS UTILITAIRES
# ========================================
def clean_text(text):
    if not isinstance(text, str):
        return ""
    return re.sub(r'[^\w\s]', '', text.lower())

def analyze_sentiment(text):
    score = sia.polarity_scores(text)['compound']
    if score > 0.3: return "Positive", score
    if score < -0.3: return "Negative", score
    return "Neutral", score

# ========================================
# MODÈLES PYDANTIC
# ========================================
class TextPayload(BaseModel):
    text: str
    token_id: Optional[str] = None  # Optionnel, pour le contexte

# ========================================
# ENDPOINTS
# ========================================

@app.get("/")
def health_check():
    return {
        "status": "TrendAI is running!",
        "ai_model": model is not None,
        "data_loaded": {
            "tokens": risk_df is not None,
            "narratives": narratives_df is not None,
            "accounts": trust_df is not None
        }
    }

# MAGIC ENDPOINT : Analyse en direct d’un post
@app.post("/analyze/live")
def live_analysis(payload: TextPayload):
    
    if model is None:
        # Fallback si modèle non chargé (quand même utilisable en démo)
        return {
            "text": payload.text[:100] + "...",
            "warning": "AI Model not loaded (demo mode)",
            "ai_verdict": {
                "is_bot": None,
                "bot_probability": None,
                "sentiment": analyze_sentiment(payload.text)[0],
                "warning_label": "Model unavailable"
            }
        }

    try:
        clean = clean_text(payload.text)
        pred = model.predict([clean])[0]
        prob = model.predict_proba([clean])[0][1]
        is_bot_flag = bool(pred == 1)
        sent_label, sent_score = analyze_sentiment(payload.text)

        warning = "Clean"
        if is_bot_flag and sent_label == "Positive":
            warning = "Artificial Hype (Pump & Dump Risk)"
        elif is_bot_flag and sent_label == "Negative":
            warning = "Coordinated FUD Attack"

        return {
            "text": payload.text[:100] + ("..." if len(payload.text) > 100 else ""),
            "token_context": payload.token_id,
            "ai_verdict": {
                "is_bot": is_bot_flag,
                "bot_probability": round(prob * 100, 1),
                "sentiment": sent_label,
                "sentiment_score": round(sent_score, 4)
            },
            "warning_label": warning,
            "risk_level": "HIGH" if is_bot_flag else "LOW"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# Rapport complet sur un token
@app.get("/token/{token_id}")
def get_token_report(token_id: str):
    token_id = token_id.upper()
    response = {"token": token_id}

    if risk_df is not None:
        row = risk_df[risk_df['token_id'] == token_id]
        response["risk_profile"] = row.iloc[0].to_dict() if not row.empty else "No data"

    if narratives_df is not None:
        nars = narratives_df[narratives_df['token_id'] == token_id]
        response["narratives"] = nars[['topic', 'risk_level', 'warning', 'bot_percentage']].to_dict(orient='records')

    return response

# Vérification de compte
@app.get("/account/{username_or_id}")
def get_account_trust(username_or_id: str):
    if trust_df is None:
        raise HTTPException(status_code=503, detail="Trust database not loaded")
    user = trust_df[
        (trust_df['account_id'] == username_or_id) |
        (trust_df['username'] == username_or_id)
    ]
    if user.empty:
        raise HTTPException(status_code=404, detail="User not found")
    return user.iloc[0].to_dict()

# Classements
@app.get("/rankings/high-risk")
def get_high_risk_tokens():
    if risk_df is None: return []
    return risk_df.head(10)[['token_id', 'risk_score', 'label', 'reason']].to_dict(orient='records')

@app.get("/rankings/bots")
def get_known_bots():
    if trust_df is None: return []
    return trust_df.sort_values('trust_score').head(10)[['username', 'trust_score', 'trust_label', 'bot_ratio']].to_dict(orient='records')

# ========================================
# LANCEMENT
# ========================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("integrated_api:app", host="0.0.0.0", port=8000, reload=True) """


"""
TrendAI - Version Finale avec Agent + PostgreSQL + Écriture en base
"""

"""
TrendAI - Version Finale Complète (PostgreSQL + Agent + Écriture en base)
Hackathon Ready - Tout fonctionne
"""

"""
TrendAI - Version Finale 100% Fonctionnelle
PostgreSQL + Agent + Analyse complète + Écriture en base
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text, Column, String, Float, JSON, DateTime, func
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
import pickle
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from analysis_agent import AnalysisAgent

# ========================================
# CONFIG
# ========================================
app = FastAPI(title="TrendAI - Full Agent + PostgreSQL", version="3.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# CHANGE TON MOT DE PASSE ICI (sans accent !)
DATABASE_URL = "postgresql://postgres:admin123@localhost:5432/trendai"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Table pour stocker les rapports
class AnalysisReport(Base):
    __tablename__ = "analysis_reports"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token_id = Column(String, nullable=False, index=True)
    risk_score = Column(Float)
    risk_label = Column(String)
    explanation = Column(String)
    key_findings = Column(JSON, default=list)
    recommendations = Column(String)
    created_at = Column(DateTime, server_default=func.now())

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ========================================
# CHARGEMENT MODÈLE + AGENT
# ========================================
nltk.download('vader_lexicon', quiet=True)
sia = SentimentIntensityAnalyzer()
model = None
agent = AnalysisAgent()

@app.on_event("startup")
def startup():
    global model
    try:
        with open("bot_detector.pkl", "rb") as f:
            model = pickle.load(f)
        print("Bot Detector Model: Loaded")
    except Exception as e:
        print(f"Model not loaded: {e}")
    print("TrendAI Ready - Agent + PostgreSQL")

# ========================================
# ENDPOINT PRINCIPAL : Analyse complète avec agent
# ========================================
@app.get("/analyze/token/{token_id}")
def analyze_token(token_id: str, db: Session = Depends(get_db)):
    token_id = token_id.upper()

    # Requête corrigée avec .mappings()
    query = text("""
        SELECT 
            t.token_id,
            t.risk_score,
            t.risk_label,
            t.bot_ratio,
            t.avg_sentiment,
            t.reason,
            COUNT(p.id) as total_posts,
            COALESCE(SUM(CASE WHEN p.is_bot THEN 1 ELSE 0 END), 0) as bot_posts
        FROM tokens t
        LEFT JOIN posts p ON p.token_id = t.token_id
        WHERE t.token_id = :tid
        GROUP BY t.id, t.token_id, t.risk_score, t.risk_label, t.bot_ratio, t.avg_sentiment, t.reason
    """)

    result = db.execute(query, {"tid": token_id}).mappings().fetchone()

    if not result:
        raise HTTPException(status_code=404, detail=f"Token {token_id} not found")

    total_posts = result["total_posts"] or 0
    bot_posts = result["bot_posts"] or 0
    bot_ratio = bot_posts / total_posts if total_posts > 0 else 0

    token_data = {
        "token_id": result["token_id"],
        "risk_score": float(result["risk_score"] or 0),
        "risk_label": result["risk_label"] or "UNKNOWN",
        "bot_ratio": round(bot_ratio, 3),
        "avg_sentiment": float(result["avg_sentiment"] or 0)
    }

    # Narratives - CORRIGÉ avec .mappings()
    narratives_result = db.execute(
        text("SELECT topic, risk_level, warning, bot_percentage FROM narratives WHERE token_id = :tid"),
        {"tid": token_id}
    ).mappings().fetchall()
    narratives_list = [dict(row) for row in narratives_result]

    # Posts suspects
    suspicious_result = db.execute(
        text("SELECT text FROM posts WHERE token_id = :tid AND is_bot = true LIMIT 5"),
        {"tid": token_id}
    ).fetchall()
    suspicious_texts = [row.text for row in suspicious_result]

    # Agent génère le rapport
    try:
        report = agent.generate_token_analysis(token_data, narratives_list, suspicious_texts)
    except Exception as e:
        report = {
            "token_id": token_id,
            "risk_score": token_data["risk_score"],
            "explanation": f"Agent failed: {str(e)}",
            "key_findings": ["Error during analysis"],
            "recommendations": "Check server logs",
            "confidence": "ERROR"
        }

    # Écriture en base
    db_report = AnalysisReport(
        token_id=token_id,
        risk_score=report.get("risk_score"),
        risk_label=report.get("risk_label"),
        explanation=report.get("explanation", ""),
        key_findings=report.get("key_findings", []),
        recommendations=report.get("recommendations", "")
    )
    db.add(db_report)
    db.commit()

    return report

# Voir les rapports
@app.get("/reports")
def get_reports(db: Session = Depends(get_db)):
    reports = db.query(AnalysisReport).order_by(AnalysisReport.created_at.desc()).limit(10).all()
    return [{"token_id": r.token_id, "created_at": str(r.created_at), "explanation": r.explanation[:150]} for r in reports]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("integrated_api:app", host="0.0.0.0", port=8000, reload=True)