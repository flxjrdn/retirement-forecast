import math
from datetime import date

from src.interest_strategy.interest_strategy import InterestStrategy


class FixedInterestStrategy(InterestStrategy):
    """
    An interest strategy that applies a constant annual interest rate,
    compounded monthly. The rate does not vary by date.
    """

    def __init__(self, annual_rate: float):
        if annual_rate is None or math.isnan(annual_rate):
            raise ValueError("Annual rate must be a valid number.")
        if annual_rate < -1:
            raise ValueError("Annual rate must be greater than -100%")
        self._annual_rate = annual_rate
        self._monthly_rate = (1 + self._annual_rate) ** (1 / 12) - 1

    def get_monthly_rate(self, current_date: date) -> float:
        """
        Returns the monthly compound rate derived from the fixed annual rate.
        The current_date parameter is ignored in this implementation.
        """
        return self._monthly_rate
