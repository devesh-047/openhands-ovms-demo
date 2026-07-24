from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.models import LoginRequest, LoginResponse, RegisterRequest, UserResponse
from app.store import store

router = APIRouter()


def _is_valid_email(email: str) -> bool:
    return "@" in email


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest) -> UserResponse:
    if not _is_valid_email(request.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email")

    if store.get_user(request.email) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user = store.create_user(request.name, request.email, request.password)
    return UserResponse(id=user.id, name=user.name, email=user.email, balance=user.balance)


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest) -> LoginResponse:
    user = store.get_user(request.email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user.password != request.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")

    return LoginResponse(
        message="Login successful",
        user=UserResponse(id=user.id, name=user.name, email=user.email, balance=user.balance),
    )
