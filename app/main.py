from __future__ import annotations

from fastapi import FastAPI

from app.auth import router as auth_router
from app.models import HealthResponse
from app.payments import router as payments_router
from app.transactions import router as transactions_router

app = FastAPI(title="Demo Banking API")


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


app.include_router(auth_router)
app.include_router(payments_router)
app.include_router(transactions_router)
