import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from utils.config_validator import ConfigValidator, ConfigError


class MockConfig:
    WARM_COLORS = {"primary": "#E85A4F", "secondary": "#E98074"}
    WARM_PALETTE = ["#E85A4F", "#E98074"]


class BadConfig:
    WARM_COLORS = {"bad": "not-a-color"}


class TestConfig(unittest.TestCase):
    def test_valid_config(self):
        self.assertTrue(ConfigValidator.validate(MockConfig))

    def test_missing_keys(self):
        with self.assertRaises(ConfigError):
            ConfigValidator.validate(BadConfig)

    def test_invalid_color(self):
        class InvalidColorConfig:
            WARM_COLORS = {"primary": "ZZZ"}
            WARM_PALETTE = []

        with self.assertRaises(ConfigError):
            ConfigValidator.validate(InvalidColorConfig)


if __name__ == "__main__":
    unittest.main()
