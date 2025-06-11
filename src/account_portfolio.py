from datetime import date
from dateutil.relativedelta import relativedelta
from typing import Dict, List
from dataclasses import dataclass

from src.balance.balance_with_history_and_strategy import BalanceWithHistoryAndStrategy
from src.interest_strategy.interest_strategy import InterestStrategy


@dataclass
class ContributionRule:
    """
    Defines a recurring contribution to an account from a certain age range.
    Can optionally escalate annually by a fixed rate.
    """

    account_name: str
    amount: float  # Initial monthly deposit
    start_age: int
    end_age: int
    annual_increase_rate: float = 0.0  # e.g., 0.02 for 2% annual increase

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Contribution amount must be non-negative.")
        if not (0.0 <= self.annual_increase_rate <= 1.0):
            raise ValueError("Annual increase rate must be between 0.0 and 1.0.")
        if self.start_age >= self.end_age:
            raise ValueError(
                "Start age must be less than end age for contribution rule."
            )


@dataclass
class WithdrawalRule:
    """
    Defines a recurring withdrawal from an account over a specific age range.
    """

    account_name: str
    amount: float  # Monthly withdrawal
    start_age: int
    end_age: int

    def __post_init__(self):
        if self.amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if self.start_age >= self.end_age:
            raise ValueError("Start age must be less than end age for withdrawal rule.")


class AccountPortfolio:
    """
    Represents all financial accounts of a person, each with a balance and growth strategy.
    Supports deposits, withdrawals, and projections by date or age, including age-based contribution
    and withdrawal rules with optional escalation.
    """

    def __init__(self, birthdate: date):
        """Initialize the portfolio with a person's birthdate."""
        self._birthdate = birthdate
        self._accounts: Dict[str, BalanceWithHistoryAndStrategy] = {}
        self._contribution_rules: List[ContributionRule] = []
        self._withdrawal_rules: List[WithdrawalRule] = []

    def add_account(
        self,
        name: str,
        initial_amount: float,
        start_date: date,
        strategy: InterestStrategy,
    ) -> None:
        """Add a new account to the portfolio."""
        if name in self._accounts:
            raise ValueError(f"Account '{name}' already exists.")
        self._accounts[name] = BalanceWithHistoryAndStrategy(
            initial_amount, start_date, strategy
        )

    def add_contribution_rule(self, rule: ContributionRule) -> None:
        """Add a recurring contribution rule for a specific account."""
        if rule.account_name not in self._accounts:
            raise KeyError(f"Account '{rule.account_name}' not found.")
        self._contribution_rules.append(rule)

    def add_withdrawal_rule(self, rule: WithdrawalRule) -> None:
        """Add a recurring withdrawal rule for a specific account."""
        if rule.account_name not in self._accounts:
            raise KeyError(f"Account '{rule.account_name}' not found.")
        self._withdrawal_rules.append(rule)

    def get_account_names(self) -> List[str]:
        """Return a list of all account names."""
        return list(self._accounts.keys())

    def get_balance(self, name: str) -> float:
        """Return the current balance of the specified account."""
        return self._get_account(name).current_amount()

    def deposit(self, name: str, amount: float) -> None:
        """Deposit a specific amount into an account."""
        self._get_account(name).add(amount)

    def withdraw(self, name: str, amount: float) -> None:
        """Withdraw a specific amount from an account."""
        self._get_account(name).subtract(amount)

    def _current_age(self, on_date: date) -> int:
        """Return the age of the person on a given date."""
        return relativedelta(on_date, self._birthdate).years

    def _months_since_age(self, current_date: date, target_age: int) -> int:
        """Return the number of months since a given target age."""
        age_date = self._birthdate + relativedelta(years=target_age)
        delta = relativedelta(current_date, age_date)
        return delta.years * 12 + delta.months

    def _apply_contribution_rules(
        self, name: str, account: BalanceWithHistoryAndStrategy, date: date
    ) -> None:
        """Apply all applicable contribution rules to an account on a given date."""
        age = self._current_age(date)
        for rule in self._contribution_rules:
            if rule.account_name == name and rule.start_age <= age < rule.end_age:
                months_since_start = self._months_since_age(date, rule.start_age)
                years_since_start = months_since_start // 12
                escalated_amount = rule.amount * (
                    (1 + rule.annual_increase_rate) ** years_since_start
                )
                account.add(escalated_amount)

    def _apply_withdrawal_rules(
        self, name: str, account: BalanceWithHistoryAndStrategy, date: date
    ) -> None:
        """Apply all applicable withdrawal rules to an account on a given date."""
        age = self._current_age(date)
        for rule in self._withdrawal_rules:
            if rule.account_name == name and rule.start_age <= age < rule.end_age:
                account.subtract(rule.amount)

    def project_one_month(self) -> None:
        """Advance each account by one month, applying all relevant rules."""
        for name, account in self._accounts.items():
            current_date = account.current_date()
            self._apply_contribution_rules(name, account, current_date)
            self._apply_withdrawal_rules(name, account, current_date)
            account.project_one_month()

    def project_to_date(self, target_date: date) -> None:
        """Project all accounts forward to a specific date."""
        while any(
            account.current_date() < target_date for account in self._accounts.values()
        ):
            self.project_one_month()

    def project_to_age(self, target_age: int) -> None:
        """Project all accounts forward until the person reaches a specific age."""
        target_date = self._birthdate + relativedelta(years=target_age)
        self.project_to_date(target_date)

    def total_balance(self) -> float:
        """Return the total balance across all accounts."""
        return sum(account.current_amount() for account in self._accounts.values())

    def account_history(self, name: str):
        """Return the transaction history for a specific account."""
        return self._get_account(name).history()

    def birthdate(self) -> date:
        """Return the person's birthdate."""
        return self._birthdate

    def _get_account(self, name: str) -> BalanceWithHistoryAndStrategy:
        """Retrieve an account by name or raise an error if not found."""
        if name not in self._accounts:
            raise KeyError(f"Account '{name}' not found.")
        return self._accounts[name]
