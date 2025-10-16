"""
Operation strategies for the calculator using the Strategy Pattern.

From maintainability implementation with performance optimizations.
Uses __slots__ for memory efficiency from performance implementation.
"""

from abc import ABC, abstractmethod
from typing import Union
from calculator.exceptions import DivisionByZeroError


class Operation(ABC):
    """
    Abstract base class for all arithmetic operations.

    Defines the contract for all operations, enabling polymorphism
    and the Open/Closed Principle (open for extension, closed for modification).
    """

    __slots__ = ()  # Performance optimization from performance implementation

    @abstractmethod
    def execute(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """
        Execute the operation on two operands.

        Args:
            a: First operand
            b: Second operand

        Returns:
            Result of the operation

        Raises:
            CalculatorError: If the operation cannot be performed
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Return the name of the operation for logging/debugging."""
        pass


class AddOperation(Operation):
    """Addition operation: a + b"""

    __slots__ = ()

    def execute(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        return a + b

    def get_name(self) -> str:
        return "addition"


class SubtractOperation(Operation):
    """Subtraction operation: a - b"""

    __slots__ = ()

    def execute(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        return a - b

    def get_name(self) -> str:
        return "subtraction"


class MultiplyOperation(Operation):
    """Multiplication operation: a * b"""

    __slots__ = ()

    def execute(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        return a * b

    def get_name(self) -> str:
        return "multiplication"


class DivideOperation(Operation):
    """
    Division operation: a / b

    Includes validation to prevent division by zero.
    """

    __slots__ = ()

    def execute(self, a: Union[int, float], b: Union[int, float]) -> float:
        # Early exit for division by zero (performance optimization)
        if b == 0:
            raise DivisionByZeroError(a)
        return a / b

    def get_name(self) -> str:
        return "division"
