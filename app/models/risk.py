from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from app.core.database import Base
import datetime
from sqlalchemy import ForeignKey

class RiskScore(Base):
    __tablename__ = "risk_scores"
    id = Column(Integer, primary_key=True, index=True)
    token_id = Column(String, index=True)  # uses token name as id (e.g., "AITK")
    score = Column(Float, nullable=False)   # 0..100
    label = Column(String, nullable=False)  # Safe / Suspicious / High Risk
    reason = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    #chat 9ali yzidha
    # narrative_id = Column(String, ForeignKey("narratives.narrative_id"), nullable=True)
