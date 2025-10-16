"""
Calculator package with balanced design.

Public API for Strategy C implementation.
"""

from .calculator import Calculator
from .exceptions import CalculatorError, DivisionByZeroError

__all__ = ['Calculator', 'CalculatorError', 'DivisionByZeroError']
