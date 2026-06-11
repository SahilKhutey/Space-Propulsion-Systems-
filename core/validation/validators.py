"""
Input validation utilities for propulsion simulations.
"""
from typing import Any
import numpy as np


def validate_positive(name: str, value: Any) -> float:
    if value is None or value <= 0:
        raise ValueError(f"{name} must be positive, got {value}")
    return float(value)


def validate_range(name: str, value: float, lo: float, hi: float) -> float:
    if not (lo <= value <= hi):
        raise ValueError(f"{name} must be in [{lo}, {hi}], got {value}")
    return float(value)


def validate_choice(name: str, value: str, choices: list[str]) -> str:
    if value not in choices:
        raise ValueError(f"{name} must be one of {choices}, got {value}")
    return value
