from datetime import date

from src.interest_strategy.interest_strategy import InterestStrategy


class FixedInterestStrategy(InterestStrategy):
    def __init__(self, annual_rate: float):
        if annual_rate < -1:
            raise ValueError("Annual rate must be greater than -100%")
        self.annual_rate = annual_rate

    def get_monthly_rate(self, current_date: date) -> float:
        return (1 + self.annual_rate) ** (1 / 12) - 1
