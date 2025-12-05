from pydantic import BaseModel
from datetime import date

class AccountBase(BaseModel):
    account_id: str
    username: str
    created_at: date
    followers: int
    following: int
    posts_per_day: float
    credibility: str

class AccountIn(AccountBase):
    pass

class AccountOut(AccountBase):
    class Config:
        orm_mode = True
