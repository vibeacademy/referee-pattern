"""
Maintainability Agent Implementation - Key Excerpts

Focus: Clean architecture, SOLID principles, extensibility
"""

# ============================================================================
# FILE: calculator/operations.py (Maintainability)
# ============================================================================

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
    """Addition operation."""

    def execute(self, current: float, value: float) -> float:
        return current + value


class Subtraction(Operation):
    """Subtraction operation."""

    def execute(self, current: float, value: float) -> float:
        return current - value


class Multiplication(Operation):
    """Multiplication operation."""

    def execute(self, current: float, value: float) -> float:
        return current * value


class Division(Operation):
    """Division operation."""

    def execute(self, current: float, value: float) -> float:
        if value == 0:
            raise ValueError("Cannot divide by zero")
        return current / value


# ============================================================================
# FILE: calculator/calculator.py (Maintainability)
# ============================================================================

from typing import Dict
from .operations import Operation, Addition, Subtraction, Multiplication, Division


class Calculator:
    """
    A calculator supporting basic arithmetic operations.

    This implementation prioritizes clean architecture and extensibility.
    New operations can be added by creating new Operation subclasses.
    """

    def __init__(self):
        """Initialize calculator with result of 0."""
        self._result: float = 0
        self._operations: Dict[str, Operation] = self._setup_operations()

    def _setup_operations(self) -> Dict[str, Operation]:
        """
        Set up available operations.

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
            ValueError: If operation not supported or invalid value
        """
        if operation not in self._operations:
            available = ', '.join(self._operations.keys())
            raise ValueError(f"Operation '{operation}' not supported. Available: {available}")

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


# ============================================================================
# STRENGTHS OF THIS APPROACH
# ============================================================================

"""
✅ Strategy Pattern: Easy to add new operations by creating new classes
✅ Separation of Concerns: Operations separated from Calculator logic
✅ Open/Closed Principle: Extend without modifying existing code
✅ Clear Documentation: Every method and class documented
✅ Type Hints: Full type safety and IDE support
✅ Professional Structure: Multiple focused modules
✅ Testability: Each operation can be tested independently

WEAKNESSES:
❌ More files: Requires understanding multiple modules
❌ Slight overhead: Dictionary lookup for operations
❌ Memory: Standard Python classes (no __slots__)
"""
