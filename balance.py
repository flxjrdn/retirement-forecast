from datetime import date


class Balance:
    def __init__(self, initial_amount: float, start_date: date):
        self.amount = initial_amount
        self.start_date = start_date

    def add(self, amount: float) -> None:
        self.amount += amount

    def subtract(self, amount: float) -> None:
        self.amount -= amount

    def _project_one_month(self, rate: float) -> None:
        self.amount *= 1 + rate


class BalanceFixedRate(Balance):
    def __init__(
        self, initial_amount: float, start_date: date, annual_rate: float
    ) -> None:
        super().__init__(initial_amount=initial_amount, start_date=start_date)
        self.monthly_rate = annual_rate ** (1 / 12) - 1

    def project_one_month(self) -> None:
        self._project_one_month(self.monthly_rate)
