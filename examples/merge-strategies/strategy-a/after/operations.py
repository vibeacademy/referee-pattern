"""
Calculator operations using Strategy pattern.

Adopted from Maintainability agent for extensibility.
New operations can be added by creating new Operation subclasses.
"""

from abc import ABC, abstractmethod


class Operation(ABC):
    """
    Abstract base class for calculator operations.

    This follows the Strategy pattern, making it easy to add new operations
    without modifying the Calculator class (Open/Closed Principle).
    """

    @abstractmethod
    def execute(self, current: float, value: float) -> float:
        """
        Execute the operation.

        Args:
            current: Current calculator result
            value: Value to apply in operation

        Returns:
            New result after applying operation
        """
        pass


class Addition(Operation):
    """Addition operation: current + value"""

    def execute(self, current: float, value: float) -> float:
        return current + value


class Subtraction(Operation):
    """Subtraction operation: current - value"""

    def execute(self, current: float, value: float) -> float:
        return current - value


class Multiplication(Operation):
    """Multiplication operation: current * value"""

    def execute(self, current: float, value: float) -> float:
        return current * value


class Division(Operation):
    """Division operation: current / value"""

    def execute(self, current: float, value: float) -> float:
        # Note: Division by zero checking happens in Calculator.execute()
        # to provide better error messages with context
        return current / value
