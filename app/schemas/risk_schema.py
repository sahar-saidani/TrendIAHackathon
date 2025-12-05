from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RiskOut(BaseModel):
    token_id: str
    score: float
    label: str
    reason: Optional[str]
    updated_at: datetime

    class Config:
        orm_mode = True
