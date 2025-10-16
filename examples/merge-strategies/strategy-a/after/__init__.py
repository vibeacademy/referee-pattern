"""
Calculator package.

Clean public API adopted from Maintainability agent.
Users import `from calculator import Calculator`, not deep module paths.
"""

from .calculator import Calculator
from .exceptions import CalculatorError, DivisionByZeroError, InvalidOperationError

__all__ = [
    'Calculator',
    'CalculatorError',
    'DivisionByZeroError',
    'InvalidOperationError',
]
