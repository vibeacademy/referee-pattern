"""
Custom exceptions for the calculator.

Provides a clear exception hierarchy for precise error handling.
From robustness implementation.
"""


class CalculatorError(Exception):
    """Base exception for all calculator-related errors."""
    pass


class DivisionByZeroError(CalculatorError):
    """Raised when attempting to divide by zero."""

    def __init__(self, dividend):
        self.dividend = dividend
        super().__init__(f"Cannot divide {dividend} by zero. Division by zero is undefined.")


class InvalidInputError(CalculatorError):
    """Raised when input validation fails."""
    pass
