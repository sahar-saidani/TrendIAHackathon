from pydantic import BaseModel
from typing import List
from datetime import datetime

class NarrativeBase(BaseModel):
    narrative_id: str
    token_id: str
    topic: str
    start_time: datetime
    end_time: datetime

class NarrativeIn(NarrativeBase):
    posts: List[str]  # list of post_ids

class NarrativeOut(NarrativeBase):
    posts: List[str]

    class Config:
        orm_mode = True
