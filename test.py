import unittest

from main import slt


class TestSlt(unittest.TestCase):
    def test_sample_data_returns_none(self):
        result = slt(
            [100000, 95000, 105000, 98000],
            99000,
            0.85,
            [False, True, True, True],
        )
        self.assertIsNone(result)

    def test_two_eligible_above_threshold(self):
        result = slt([120, 130, 90], 100, 0.5, [True, True, True])
        self.assertAlmostEqual(result, 69.54915028125262, places=6)

    def test_all_below_threshold_returns_none(self):
        result = slt([150, 160], 200, 0.7, [True, True])
        self.assertIsNone(result)

    def test_only_one_eligible_returns_none(self):
        result = slt([300, 500, 200], 250, 0.9, [False, True, True])
        self.assertIsNone(result)

    def test_mixed_eligibility(self):
        result = slt([220, 260, 280, 310], 200, 1.0, [True, False, True, True])
        self.assertAlmostEqual(result, 197.6878528870718, places=6)

    def test_equal_prices_zero_sd(self):
        result = slt([300, 300, 300], 200, 0.8, [True, True, True])
        self.assertAlmostEqual(result, 176.0, places=6)

    def test_high_nppi(self):
        result = slt([400, 450, 470], 300, 1.2, [True, True, True])
        self.assertAlmostEqual(result, 328.2449444258758, places=6)

    def test_float_prices(self):
        result = slt([110.5, 121.2, 130.8], 100.0, 0.75, [True, True, True])
        self.assertAlmostEqual(result, 83.17443190630243, places=6)

    def test_eligibility_shorter_than_prices(self):
        result = slt([200, 240, 260], 180, 0.6, [True, False])
        self.assertIsNone(result)

    def test_threshold_strictly_greater(self):
        result = slt([110, 111, 112], 100, 0.5, [True, True, True])
        self.assertAlmostEqual(result, 69.99397677781218, places=6)


if __name__ == "__main__":
    unittest.main()
