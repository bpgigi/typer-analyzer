from typing import Any, Dict, List
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


class ConfigError(Exception):
    pass


class ConfigValidator:
    REQUIRED_KEYS = ["WARM_COLORS", "WARM_PALETTE"]

    @staticmethod
    def validate(config_module: Any) -> bool:
        missing = []
        for key in ConfigValidator.REQUIRED_KEYS:
            if not hasattr(config_module, key):
                missing.append(key)

        if missing:
            raise ConfigError(f"Missing configuration keys: {', '.join(missing)}")

        colors = getattr(config_module, "WARM_COLORS", {})
        for name, code in colors.items():
            if not ConfigValidator._is_valid_hex(code):
                raise ConfigError(f"Invalid color code for {name}: {code}")

        return True

    @staticmethod
    def _is_valid_hex(color: str) -> bool:
        if not isinstance(color, str):
            return False
        if not color.startswith("#"):
            return False
        try:
            int(color[1:], 16)
            return len(color) in (4, 7)
        except ValueError:
            return False
