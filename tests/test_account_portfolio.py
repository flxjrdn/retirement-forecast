import unittest
from datetime import date
from src.account_portfolio import AccountPortfolio, ContributionRule, WithdrawalRule
from src.interest_strategy.fixed_interest_strategy import FixedInterestStrategy


class TestAccountPortfolio(unittest.TestCase):
    def setUp(self):
        self.birthdate = date(1990, 1, 1)
        self.portfolio = AccountPortfolio(self.birthdate)
        self.fixed_interest_rate = 0.04
        self.strategy = FixedInterestStrategy(self.fixed_interest_rate)
        self.portfolio.add_account("pension", 10000.0, date(2023, 1, 1), self.strategy)

    def test_add_valid_contribution_rule(self):
        rule = ContributionRule("pension", 500.0, 30, 65, 0.02)
        self.portfolio.add_contribution_rule(rule)
        self.assertIn(rule, self.portfolio._contribution_rules)

    def test_add_valid_withdrawal_rule(self):
        rule = WithdrawalRule("pension", 1000.0, 65, 85)
        self.portfolio.add_withdrawal_rule(rule)
        self.assertIn(rule, self.portfolio._withdrawal_rules)

    def test_contribution_rule_validation(self):
        with self.assertRaises(ValueError):
            ContributionRule("pension", -100.0, 30, 65, 0.02)
        with self.assertRaises(ValueError):
            ContributionRule("pension", 100.0, 30, 25)
        with self.assertRaises(ValueError):
            ContributionRule("pension", 100.0, 30, 65, 1.5)

    def test_withdrawal_rule_validation(self):
        with self.assertRaises(ValueError):
            WithdrawalRule("pension", -500.0, 65, 85)
        with self.assertRaises(ValueError):
            WithdrawalRule("pension", 1000.0, 70, 60)

    def test_projection_with_zero_contributions(self):
        rule = ContributionRule("pension", 0.0, 33, 40, 0.0)
        self.portfolio.add_contribution_rule(rule)
        self.portfolio.project_to_age(34)
        balance = self.portfolio.get_balance("pension")
        self.assertAlmostEqual(
            balance, 10000.0 * (1 + self.fixed_interest_rate), places=5
        )

    def test_projection_with_escalating_contributions(self):
        rule = ContributionRule("pension", 500.0, 33, 35, 0.1)
        self.portfolio.add_contribution_rule(rule)
        self.portfolio.project_to_age(34)
        balance = self.portfolio.get_balance("pension")
        self.assertGreater(balance, 10000.0)

    def test_projection_with_withdrawals(self):
        rule = WithdrawalRule("pension", 100.0, 33, 35)
        self.portfolio.add_withdrawal_rule(rule)
        self.portfolio.project_to_age(34)
        balance = self.portfolio.get_balance("pension")
        self.assertLess(balance, 10000.0)

    def test_add_duplicate_account_raises(self):
        with self.assertRaises(ValueError):
            self.portfolio.add_account(
                "pension", 5000.0, date(2024, 1, 1), self.strategy
            )

    def test_add_rule_to_nonexistent_account_raises(self):
        with self.assertRaises(KeyError):
            self.portfolio.add_contribution_rule(
                ContributionRule("savings", 500.0, 30, 60)
            )
        with self.assertRaises(KeyError):
            self.portfolio.add_withdrawal_rule(WithdrawalRule("savings", 500.0, 60, 70))


if __name__ == "__main__":
    unittest.main()
