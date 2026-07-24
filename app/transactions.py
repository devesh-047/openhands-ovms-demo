from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query, status

from app.models import TransactionHistoryResponse, TransactionResponse
from app.store import store

router = APIRouter()


@router.get("/transactions", response_model=TransactionHistoryResponse)
def get_transactions(email: str = Query(..., min_length=1)) -> TransactionHistoryResponse:
    user = store.get_user(email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    transactions = [
        TransactionResponse(
            id=transaction.id,
            amount=transaction.amount,
            type=transaction.type,
            timestamp=transaction.timestamp,
            description=transaction.description,
        )
        for transaction in store.get_transactions_for_user(email)
    ]
    return TransactionHistoryResponse(email=email, transactions=transactions)
