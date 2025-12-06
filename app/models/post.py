from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from app.core.database import Base
import datetime

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(String, unique=True, index=True)   # original post id (p001, p010, etc)
    token_id = Column(String, index=True)                # now a text token id (e.g., "AITK")
    account_id = Column(String, index=True)              # account who posted (acc001...)
    text = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    type = Column(String, nullable=True)                 # organic, bot, fake_news, etc.

    # analysis fields (filled by pipeline)
    organic_score = Column(Float, nullable=True)   # 0..1 low => suspicious
    label = Column(String, nullable=True)          # 'Organic' or 'Suspicious'
    bot_score = Column(Float, nullable=True)       # 0..1 higher = more bot-like
    cluster_id = Column(Integer, nullable=True)    # clustering group id

    #chat 9ali yzidha 
    # narratives = relationship("PostNarrativeLink", back_populates="post")
