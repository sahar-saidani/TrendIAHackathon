# app/schemas/token_schema.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TokenBase(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenOut(TokenBase):
    expires_in: Optional[int] = 3600
    created_at: datetime = datetime.now()