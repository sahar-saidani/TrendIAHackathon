from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from ..core.database import Base

class Narrative(Base):
    __tablename__ = "narratives"

    narrative_id = Column(String, primary_key=True, index=True)
    token_id = Column(String, index=True)
    topic = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    posts = relationship("PostNarrativeLink", back_populates="narrative")
