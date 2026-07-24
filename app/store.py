from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


@dataclass
class User:
    id: int
    name: str
    email: str
    password: str
    balance: float


@dataclass
class Transaction:
    id: int
    user_email: str
    amount: float
    type: str
    timestamp: str
    description: Optional[str] = None


class InMemoryStore:
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.users: dict[str, User] = {}
        self.transactions: list[Transaction] = []
        self._next_user_id = 1
        self._next_transaction_id = 1

    def create_user(self, name: str, email: str, password: str) -> User:
        user = User(
            id=self._next_user_id,
            name=name,
            email=email,
            password=password,
            balance=1000.0,
        )
        self.users[email] = user
        self._next_user_id += 1
        return user

    def get_user(self, email: str) -> User | None:
        return self.users.get(email)

    def add_transaction(self, user_email: str, amount: float, transaction_type: str, description: Optional[str] = None) -> Transaction:
        transaction = Transaction(
            id=self._next_transaction_id,
            user_email=user_email,
            amount=amount,
            type=transaction_type,
            timestamp=datetime.now(timezone.utc).isoformat(),
            description=description,
        )
        self.transactions.append(transaction)
        self._next_transaction_id += 1
        return transaction

    def get_transactions_for_user(self, email: str) -> list[Transaction]:
        return [transaction for transaction in self.transactions if transaction.user_email == email]


store = InMemoryStore()
