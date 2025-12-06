from sqlalchemy import Column, String, Integer, Date
from ..core.database import Base

class Account(Base):
    __tablename__ = "accounts"

    account_id = Column(String, primary_key=True, index=True)
    username = Column(String, index=True)
    created_at = Column(Date)
    followers = Column(Integer)
    following = Column(Integer)
    posts_per_day = Column(Integer)
    credibility = Column(String)
