"""
Main calculator implementation combining all best practices.

Combines:
- Maintainability: Strategy Pattern, clean architecture, extensibility
- Performance: __slots__ for memory efficiency, Flyweight for operation reuse
- Robustness: Comprehensive error handling, clear exception messages

This represents the best merged approach from all three specialized implementations.
"""

import logging
from typing import Union, Optional
from calculator.operations import (
    AddOperation,
    SubtractOperation,
    MultiplyOperation,
    DivideOperation
)

# Optional logging from robustness implementation
logger = logging.getLogger(__name__)


class Calculator:
    """
    A calculator that performs basic arithmetic operations.

    Features:
    - Strategy Pattern for extensibility (from maintainability)
    - Memory-efficient with __slots__ (from performance)
    - Comprehensive error handling (from robustness)
    - Clean, simple API

    Example:
        >>> calc = Calculator()
        >>> calc.add(5, 3)
        8
        >>> calc.divide(10, 2)
        5.0
    """

    __slots__ = ('_add_op', '_subtract_op', '_multiply_op', '_divide_op', '_last_result')

    def __init__(self):
        """
        Initialize the calculator with available operations.

        Operations are instantiated once and reused (Flyweight pattern)
        for memory efficiency.
        """
        self._add_op = AddOperation()
        self._subtract_op = SubtractOperation()
        self._multiply_op = MultiplyOperation()
        self._divide_op = DivideOperation()
        self._last_result: Optional[Union[int, float]] = None

    def add(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """
        Add two numbers.

        Args:
            a: First number
            b: Second number

        Returns:
            Sum of a and b
        """
        self._last_result = self._add_op.execute(a, b)
        return self._last_result

    def subtract(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """
        Subtract b from a.

        Args:
            a: Number to subtract from
            b: Number to subtract

        Returns:
            Difference of a and b
        """
        self._last_result = self._subtract_op.execute(a, b)
        return self._last_result

    def multiply(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """
        Multiply two numbers.

        Args:
            a: First number
            b: Second number

        Returns:
            Product of a and b
        """
        self._last_result = self._multiply_op.execute(a, b)
        return self._last_result

    def divide(self, a: Union[int, float], b: Union[int, float]) -> float:
        """
        Divide a by b.

        Args:
            a: Dividend
            b: Divisor

        Returns:
            Quotient of a and b

        Raises:
            DivisionByZeroError: If b is zero
        """
        self._last_result = self._divide_op.execute(a, b)
        return self._last_result

    def get_last_result(self) -> Optional[Union[int, float]]:
        """
        Get the result of the last operation.

        Returns:
            The last calculated result, or None if no operations performed
        """
        return self._last_result

    def clear(self):
        """Clear the last result."""
        self._last_result = None
