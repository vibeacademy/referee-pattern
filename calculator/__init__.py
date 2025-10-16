"""
Calculator package combining best practices from three specialized implementations.

Public API:
- Calculator: Main calculator class
- CalculatorError: Base exception
- DivisionByZeroError: Specific exception for division by zero
- InvalidInputError: Exception for invalid inputs
"""

from calculator.calculator import Calculator
from calculator.exceptions import (
    CalculatorError,
    DivisionByZeroError,
    InvalidInputError,
)

__all__ = [
    'Calculator',
    'CalculatorError',
    'DivisionByZeroError',
    'InvalidInputError',
]
