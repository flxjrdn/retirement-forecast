import unittest
from datetime import date
from src.account_portfolio import AccountPortfolio, ContributionRule
from src.interest_strategy.fixed_interest_strategy import FixedInterestStrategy


class TestAccountPortfolioContributions(unittest.TestCase):
    def setUp(self):
        self.birthdate = date(1990, 1, 1)
        self.portfolio = AccountPortfolio(self.birthdate)
        self.strategy = FixedInterestStrategy(0.0)  # 0% interest for clarity
        self.start_date = date(2023, 1, 1)
        self.portfolio.add_account("pension", 10000.0, self.start_date, self.strategy)

    def test_one_year_contribution(self):
        # $500/month from age 33 to 34
        self.portfolio.add_contribution_rule(ContributionRule("pension", 500.0, 33, 34))
        self.portfolio.project_to_age(34)
        expected = 10000.0 + 500.0 * 12
        balance = self.portfolio.get_balance("pension")
        self.assertAlmostEqual(balance, expected, delta=0.01)

    def test_five_year_contribution(self):
        # $500/month from age 33 to 38
        self.portfolio.add_contribution_rule(ContributionRule("pension", 500.0, 33, 38))
        self.portfolio.project_to_age(38)
        expected = 10000.0 + 500.0 * 12 * 5
        balance = self.portfolio.get_balance("pension")
        self.assertAlmostEqual(balance, expected, delta=0.01)

    def test_escalating_contributions(self):
        # $500/month starting at age 33, increasing 10% annually, for 3 years
        self.portfolio.add_contribution_rule(
            ContributionRule("pension", 500.0, 33, 36, annual_increase_rate=0.10)
        )
        self.portfolio.project_to_age(36)

        # Year 1: $500 x 12
        year1 = 500.0 * 12
        # Year 2: $550 x 12 (10% increase)
        year2 = 550.0 * 12
        # Year 3: $605 x 12 (another 10% increase)
        year3 = 605.0 * 12

        expected = 10000.0 + year1 + year2 + year3
        balance = self.portfolio.get_balance("pension")
        self.assertAlmostEqual(balance, expected, delta=0.01)


if __name__ == "__main__":
    unittest.main()
