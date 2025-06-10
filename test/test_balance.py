import unittest
from datetime import date

from src.balance.balance_with_history_and_strategy import BalanceWithHistoryAndStrategy


# Mock strategy for testing
class MockInterestStrategy:
    def __init__(self, rate: float):
        self.rate = rate

    def get_monthly_rate(self, current_date: date) -> float:
        return self.rate


class TestBalanceWithHistoryAndStrategy(unittest.TestCase):
    def setUp(self):
        self.initial_amount = 1000.0
        self.start_date = date(2023, 1, 1)
        self.strategy = MockInterestStrategy(0.05)  # 5% monthly growth
        self.balance = BalanceWithHistoryAndStrategy(self.initial_amount, self.start_date, self.strategy)

    def test_initialization(self):
        self.assertEqual(self.balance.current_amount(), self.initial_amount)
        self.assertEqual(self.balance.current_date(), self.start_date)
        self.assertEqual(self.balance.history(), [(self.start_date, self.initial_amount)])

    def test_add(self):
        self.balance.add(500.0)
        self.assertEqual(self.balance.current_amount(), 1500.0)
        self.assertEqual(len(self.balance.history()), 2)

    def test_subtract(self):
        self.balance.subtract(200.0)
        self.assertEqual(self.balance.current_amount(), 800.0)
        self.assertEqual(len(self.balance.history()), 2)

    def test_project_one_month(self):
        self.balance.project_one_month()
        expected_amount = self.initial_amount * (1 + self.strategy.rate)
        self.assertAlmostEqual(self.balance.current_amount(), expected_amount, places=5)
        self.assertEqual(self.balance.current_date(), date(2023, 2, 1))
        self.assertEqual(len(self.balance.history()), 2)

    def test_multiple_operations(self):
        self.balance.project_one_month()  # Feb 1
        self.balance.add(100.0)           # Feb 1
        self.balance.project_one_month()  # Mar 1
        expected_amount = (self.initial_amount * 1.05 + 100.0) * 1.05
        self.assertAlmostEqual(self.balance.current_amount(), expected_amount, places=5)
        self.assertEqual(self.balance.current_date(), date(2023, 3, 1))
        self.assertEqual(len(self.balance.history()), 4)

    # Edge cases
    def test_add_zero(self):
        self.balance.add(0.0)
        self.assertEqual(self.balance.current_amount(), self.initial_amount)
        self.assertEqual(len(self.balance.history()), 2)

    def test_subtract_zero(self):
        self.balance.subtract(0.0)
        self.assertEqual(self.balance.current_amount(), self.initial_amount)
        self.assertEqual(len(self.balance.history()), 2)

    def test_add_negative_amount_raises(self):
        with self.assertRaises(ValueError):
            self.balance.add(-100.0)

    def test_subtract_negative_amount_raises(self):
        with self.assertRaises(ValueError):
            self.balance.subtract(-50.0)

    def test_subtract_more_than_balance(self):
        self.balance.subtract(1500.0)
        self.assertEqual(self.balance.current_amount(), -500.0)
        self.assertEqual(len(self.balance.history()), 2)

    def test_large_growth_rate(self):
        high_growth_strategy = MockInterestStrategy(10.0)  # 1000% growth
        balance = BalanceWithHistoryAndStrategy(self.initial_amount, self.start_date, high_growth_strategy)
        balance.project_one_month()
        expected = self.initial_amount * 11.0
        self.assertAlmostEqual(balance.current_amount(), expected, places=5)

if __name__ == '__main__':
    unittest.main()
