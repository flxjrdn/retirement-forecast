from abc import ABC, abstractmethod
from datetime import date


class InterestStrategy(ABC):
    @abstractmethod
    def get_monthly_rate(self, current_date: date) -> float:
        pass