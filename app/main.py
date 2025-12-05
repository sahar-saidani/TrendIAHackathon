from fastapi import FastAPI
from app.core.database import Base, engine
from app.api.routes_tokens import router as tokens_router
from app.api.routes_risks import router as risks_router
from app.api.routes_agent import router as agent_router
from app.core.config import APP_NAME

# Create DB tables (simple approach for hackathon)
Base.metadata.create_all(bind=engine)

app = FastAPI(title=APP_NAME)

app.include_router(tokens_router)
app.include_router(risks_router)
app.include_router(agent_router)

@app.get("/")
def root():
    return {"status": "ok"}
