import os
from dotenv import load_dotenv

load_dotenv()

# Example: postgresql://postgres:postgres@localhost:5432/trendai
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/trendai"
)

# other configs
APP_NAME = os.getenv("APP_NAME", "TrendAI Watchdog Backend")
