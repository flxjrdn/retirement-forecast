from datetime import date
from typing import List, Tuple
from copy import deepcopy

from src.interest_strategy.interest_strategy import InterestStrategy


class BalanceWithHistoryAndStrategy:
    def __init__(
        self, initial_amount: float, start_date: date, strategy: InterestStrategy
    ):
        self._history: List[Tuple[date, float]] = [(start_date, initial_amount)]
        self._strategy = strategy

    def current_amount(self) -> float:
        return self._history[-1][1]

    def current_date(self) -> date:
        return self._history[-1][0]

    def history(self) -> List[Tuple[date, float]]:
        return deepcopy(self._history)

    def add(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("Cannot add a negative amount.")
        self._record_change(amount)

    def subtract(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("Cannot subtract a negative amount.")
        self._record_change(-amount)

    def project_one_month(self) -> None:
        prev_date, prev_amount = self._history[-1]
        rate = self._strategy.get_monthly_rate(prev_date)
        new_date = self._advance_one_month(prev_date)
        new_amount = prev_amount * (1 + rate)
        self._history.append((new_date, new_amount))

    def _record_change(self, delta: float) -> None:
        prev_date, prev_amount = self._history[-1]
        new_amount = prev_amount + delta
        self._history.append((prev_date, new_amount))

    def _advance_one_month(self, d: date) -> date:
        month = d.month % 12 + 1
        year = d.year + (d.month // 12)
        return date(year, month, 1)
