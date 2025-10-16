"""
Calculator exceptions.

Adopted from Robustness agent for clear, production-grade error handling.
"""


class CalculatorError(Exception):
    """Base exception for all calculator errors."""
    pass


class DivisionByZeroError(CalculatorError):
    """
    Raised when attempting to divide by zero.

    Attributes:
        current_result: Calculator's result when error occurred
    """

    def __init__(self, current_result: float):
        self.current_result = current_result
        super().__init__(
            f"Cannot divide by zero. Current result: {current_result}"
        )
