"""
Calculator implementation using Strategy A: Architectural Base + Feature Adoption.

This implementation:
- Uses Maintainability agent's modular architecture (Strategy pattern)
- Adds Performance agent's __slots__ optimization
- Includes Robustness agent's custom exception handling
"""

from typing import Dict
from .operations import Operation, Addition, Subtraction, Multiplication, Division
from .exceptions import DivisionByZeroError, InvalidOperationError


class Calculator:
    """
    A calculator supporting basic arithmetic operations.

    This implementation prioritizes maintainability through clean architecture
    while incorporating performance optimizations and robust error handling.

    Architecture decisions:
    - Strategy pattern for operations (from Maintainability)
    - __slots__ for memory efficiency (from Performance)
    - Custom exceptions for clarity (from Robustness)
    """

    __slots__ = ['_result', '_operations']  # ⚡ From Performance: ~40% memory reduction

    def __init__(self):
        """Initialize calculator with result of 0."""
        self._result: float = 0
        self._operations: Dict[str, Operation] = self._setup_operations()

    def _setup_operations(self) -> Dict[str, Operation]:
        """
        Set up available operations using Strategy pattern.

        From Maintainability: This makes adding new operations easy.
        Just create a new Operation subclass and add it here.

        Returns:
            Dictionary mapping operation names to Operation instances
        """
        return {
            'add': Addition(),
            'subtract': Subtraction(),
            'multiply': Multiplication(),
            'divide': Division(),
        }

    def execute(self, operation: str, value: float) -> float:
        """
        Execute an operation.

        Args:
            operation: Operation name ('add', 'subtract', 'multiply', 'divide')
            value: Value to use in operation

        Returns:
            New result after operation

        Raises:
            InvalidOperationError: If operation not supported
            DivisionByZeroError: If dividing by zero

        Examples:
            >>> calc = Calculator()
            >>> calc.execute('add', 5)
            5.0
            >>> calc.execute('multiply', 3)
            15.0
        """
        # 🛡️ From Robustness: Validate operation exists
        if operation not in self._operations:
            raise InvalidOperationError(
                operation,
                list(self._operations.keys())
            )

        # 🛡️ From Robustness: Explicit division by zero check with context
        if operation == 'divide' and value == 0:
            raise DivisionByZeroError(self._result)

        # 🏗️ From Maintainability: Strategy pattern dispatch
        op = self._operations[operation]
        self._result = op.execute(self._result, value)
        return self._result

    def get_result(self) -> float:
        """
        Get current result.

        Returns:
            Current calculator result
        """
        return self._result

    def reset(self) -> None:
        """Reset result to 0."""
        self._result = 0
