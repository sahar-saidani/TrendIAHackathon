from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PostIn(BaseModel):
    post_id: str
    text: str
    account_id: str
    timestamp: Optional[datetime] = None
    token_id: str
    type: Optional[str] = "organic"

class PostOut(BaseModel):
    id: int
    post_id: str
    token_id: str
    account_id: str
    text: str
    timestamp: Optional[datetime]
    type: Optional[str] = None
    organic_score: Optional[float] = None
    label: Optional[str] = None
    bot_score: Optional[float] = None
    cluster_id: Optional[int] = None

    class Config:
        orm_mode = True
