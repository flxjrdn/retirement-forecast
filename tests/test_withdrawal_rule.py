import unittest
from datetime import date
from src.account_portfolio import AccountPortfolio, WithdrawalRule
from src.interest_strategy.fixed_interest_strategy import FixedInterestStrategy


class TestAccountPortfolioWithdrawals(unittest.TestCase):
    def setUp(self):
        self.birthdate = date(1990, 1, 1)
        self.portfolio = AccountPortfolio(self.birthdate)
        self.strategy = FixedInterestStrategy(0.0)  # No interest for clarity
        self.start_date = date(2023, 1, 1)
        self.portfolio.add_account("pension", 100000.0, self.start_date, self.strategy)

    def test_one_year_withdrawal(self):
        # $1,000/month withdrawal from age 33 to 34
        self.portfolio.add_withdrawal_rule(WithdrawalRule("pension", 1000.0, 33, 34))
        self.portfolio.project_to_age(34)
        balance = self.portfolio.get_balance("pension")
        expected = 100000.0 - 1000.0 * 12
        self.assertAlmostEqual(balance, expected, delta=0.01)

    def test_one_year_withdrawal_projecting_two_years(self):
        # $1,000/month withdrawal from age 33 to 34
        self.portfolio.add_withdrawal_rule(WithdrawalRule("pension", 1000.0, 33, 34))
        self.portfolio.project_to_age(35)
        balance = self.portfolio.get_balance("pension")
        expected = 100000.0 - 1000.0 * 12
        self.assertAlmostEqual(balance, expected, delta=0.01)

    def test_five_year_withdrawal(self):
        # $1,000/month withdrawal from age 33 to 38
        self.portfolio.add_withdrawal_rule(WithdrawalRule("pension", 1000.0, 33, 38))
        self.portfolio.project_to_age(38)
        balance = self.portfolio.get_balance("pension")
        expected = 100000.0 - 1000.0 * 12 * 5
        self.assertAlmostEqual(balance, expected, delta=0.01)


if __name__ == "__main__":
    unittest.main()
