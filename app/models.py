from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str


class RegisterRequest(BaseModel):
    name: str = Field(min_length=1)
    email: str
    password: str = Field(min_length=1)


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    balance: float


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    message: str
    user: UserResponse


class PaymentRequest(BaseModel):
    email: str
    amount: float
    description: Optional[str] = None


class PaymentResponse(BaseModel):
    message: str
    balance: float
    transaction_id: int


class TransactionResponse(BaseModel):
    id: int
    amount: float
    type: str
    timestamp: str
    description: Optional[str] = None


class TransactionHistoryResponse(BaseModel):
    email: str
    transactions: list[TransactionResponse]
