"""The detection script is version controlled and unit tested, because
detection stays entirely deterministic — the loop's trust starts here.

Run: python3 -m unittest discover -s monitoring
(also picked up by `make test` via the CI workflow)
"""

import unittest

from detect import classify, load_bands


class TestClassify(unittest.TestCase):
    BASELINE = [0.10, 0.11, 0.09, 0.10, 0.12, 0.08, 0.10, 0.11, 0.09, 0.10]

    def test_stable_series_is_tier_0(self):
        verdict = classify(self.BASELINE + [0.10])
        self.assertEqual(verdict["tier"], 0)

    def test_rule1_spike_beyond_3_sigma(self):
        verdict = classify(self.BASELINE + [0.50])
        self.assertEqual(verdict["tier"], 3)
        self.assertEqual(verdict["rule"], "we1_beyond_3_sigma")

    def test_rule2_two_of_three_beyond_2_sigma(self):
        verdict = classify(self.BASELINE + [0.145, 0.10, 0.145])
        self.assertEqual(verdict["tier"], 2)
        self.assertEqual(verdict["rule"], "we2_two_of_three_beyond_2_sigma")

    def test_rule4_slow_drift_same_side(self):
        drift = [0.115, 0.113, 0.112, 0.114, 0.116, 0.113, 0.115, 0.114]
        verdict = classify(self.BASELINE + drift)
        self.assertEqual(verdict["tier"], 2)
        self.assertEqual(verdict["rule"], "we4_eight_consecutive_same_side")

    def test_zero_sigma_does_not_divide_by_zero(self):
        verdict = classify([0.1] * 12)
        self.assertEqual(verdict["tier"], 0)


class TestLoadBands(unittest.TestCase):
    def test_loads_repo_bands_yaml(self):
        import os

        path = os.path.join(os.path.dirname(__file__), "bands.yaml")
        config = load_bands(path)
        self.assertEqual(config["metric"], "ci_test_failure_rate")
        self.assertEqual(config["tiers"]["1sigma"]["action"], "log")
        self.assertEqual(config["tiers"]["2sigma"]["action"], "diagnose")
        self.assertEqual(config["tiers"]["3sigma"]["action"], "propose")
        self.assertIn("pull_request", config["tiers"]["3sigma"]["routes"])


if __name__ == "__main__":
    unittest.main()
