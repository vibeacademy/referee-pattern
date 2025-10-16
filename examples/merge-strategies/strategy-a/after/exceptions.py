"""
Calculator exceptions.

Custom exception hierarchy for calculator errors.
Adopted from Robustness agent for production-grade error handling.
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


class InvalidOperationError(CalculatorError):
    """
    Raised when an unsupported operation is requested.

    Attributes:
        operation: The requested operation name
        available_operations: List of supported operation names
    """

    def __init__(self, operation: str, available_operations: list):
        self.operation = operation
        self.available_operations = available_operations
        super().__init__(
            f"Operation '{operation}' not supported. "
            f"Available: {', '.join(available_operations)}"
        )
