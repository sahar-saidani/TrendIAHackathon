from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base

class PostNarrativeLink(Base):
    __tablename__ = "post_narrative_link"

    post_id = Column(String, ForeignKey("posts.post_id"), primary_key=True)
    narrative_id = Column(String, ForeignKey("narratives.narrative_id"), primary_key=True)

    post = relationship("Post", back_populates="narratives")
    narrative = relationship("Narrative", back_populates="posts")
