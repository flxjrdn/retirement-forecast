from datetime import date
from typing import List

from balance import Balance, BalanceFixedRate


class Savings:
    def __init__(self, date_of_birth: date) -> None:
        self.date_of_birth = date_of_birth
        self.accounts: List[Balance] = []

    def add_balance_fixed_rate(
        self, initial_amount: float, start_date: date, rate: float
    ) -> None:
        self.accounts.append(
            BalanceFixedRate(
                initial_amount=initial_amount, start_date=start_date, annual_rate=rate
            )
        )
