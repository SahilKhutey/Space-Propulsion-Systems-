import sys
import os

# Dynamically inject paths to core and engine directories
# Get monorepo root (three levels up from main.py)
MONOREPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

# 1. Add monorepo root so 'core' imports work
if MONOREPO_ROOT not in sys.path:
    sys.path.insert(0, MONOREPO_ROOT)

# 2. Add each engine directory under 'engines/' so they can be imported directly
ENGINES_DIR = os.path.join(MONOREPO_ROOT, "engines")
if os.path.exists(ENGINES_DIR):
    for entry in os.listdir(ENGINES_DIR):
        entry_path = os.path.join(ENGINES_DIR, entry)
        if os.path.isdir(entry_path) and entry_path not in sys.path:
            sys.path.insert(0, entry_path)

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import init_db
from ..api import api_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="PROPSIM - Simulation Microservice Engine Gateway"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    await init_db()


@app.get("/")
async def health_check():
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.VERSION
    }


if __name__ == "__main__":
    uvicorn.run("services.simulation_service.app.main:app", host="0.0.0.0", port=8000, reload=True)
