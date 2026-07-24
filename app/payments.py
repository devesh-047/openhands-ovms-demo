from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.models import PaymentRequest, PaymentResponse
from app.store import store

router = APIRouter()


@router.post("/payments", response_model=PaymentResponse)
def create_payment(request: PaymentRequest) -> PaymentResponse:
    user = store.get_user(request.email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if request.amount > user.balance:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient balance")

    user.balance -= request.amount
    transaction = store.add_transaction(
        user_email=user.email,
        amount=request.amount,
        transaction_type="payment",
        description=request.description,
    )
    return PaymentResponse(message="Payment successful", balance=user.balance, transaction_id=transaction.id)
