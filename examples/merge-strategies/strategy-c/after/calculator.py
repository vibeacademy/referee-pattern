"""
Balanced calculator implementation.

Strategy C: Balanced Synthesis
- Memory efficient (Performance)
- Clear structure (Maintainability)
- Production-ready errors (Robustness)
"""

from typing import Union
from .exceptions import DivisionByZeroError


class Calculator:
    """
    Calculator with balanced design priorities.

    This implementation combines the best aspects of all three approaches:
    - Memory optimization from Performance (__slots__)
    - Clear documentation from Maintainability
    - Custom exceptions from Robustness
    - Direct methods for simplicity (no Strategy pattern)

    Good for: General-purpose applications with balanced requirements
    """

    __slots__ = ['_result']  # ⚡ From Performance: Memory efficiency

    def __init__(self):
        """Initialize calculator with result of 0."""
        self._result: float = 0

    def add(self, value: Union[int, float]) -> float:
        """
        Add value to current result.

        Args:
            value: Number to add

        Returns:
            New result after addition

        Example:
            >>> calc = Calculator()
            >>> calc.add(5)
            5.0
            >>> calc.add(3)
            8.0
        """
        self._result += value
        return self._result

    def subtract(self, value: Union[int, float]) -> float:
        """
        Subtract value from current result.

        Args:
            value: Number to subtract

        Returns:
            New result after subtraction
        """
        self._result -= value
        return self._result

    def multiply(self, value: Union[int, float]) -> float:
        """
        Multiply current result by value.

        Args:
            value: Number to multiply by

        Returns:
            New result after multiplication
        """
        self._result *= value
        return self._result

    def divide(self, value: Union[int, float]) -> float:
        """
        Divide current result by value.

        Args:
            value: Divisor (cannot be zero)

        Returns:
            New result after division

        Raises:
            DivisionByZeroError: If attempting to divide by zero

        Example:
            >>> calc = Calculator()
            >>> calc.add(10)
            10.0
            >>> calc.divide(2)
            5.0
        """
        if value == 0:
            # 🛡️ From Robustness: Custom exception with context
            raise DivisionByZeroError(self._result)
        self._result /= value
        return self._result

    def get_result(self) -> float:
        """
        Get current calculator result.

        Returns:
            Current result value
        """
        return self._result

    def reset(self) -> None:
        """
        Reset calculator result to 0.

        Example:
            >>> calc = Calculator()
            >>> calc.add(5)
            5.0
            >>> calc.reset()
            >>> calc.get_result()
            0.0
        """
        self._result = 0
