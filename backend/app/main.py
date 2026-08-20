from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import CORS_ORIGINS
from app.routes import (
    chat,
    dashboard,
    disease,
    schemes,
    weather,
)

app = FastAPI(
    title="KisanAI API",
    description="Backend API for the KisanAI agricultural assistant.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(
    chat.router,
    prefix="/api/v1",
    tags=["Chat"],
)

app.include_router(
    disease.router,
    prefix="/api/v1",
    tags=["Disease Detection"],
)

app.include_router(
    weather.router,
    prefix="/api/v1",
    tags=["Weather"],
)

app.include_router(
    schemes.router,
    prefix="/api/v1",
    tags=["Government Schemes"],
)

app.include_router(
    dashboard.router,
    prefix="/api/v1",
    tags=["Dashboard"],
)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}