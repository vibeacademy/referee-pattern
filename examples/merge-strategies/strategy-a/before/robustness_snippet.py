"""
Robustness Agent Implementation - Key Excerpts

Focus: Error handling, edge cases, defensive programming
"""

# ============================================================================
# FILE: calculator/exceptions.py (Robustness)
# ============================================================================


class CalculatorError(Exception):
    """Base exception for all calculator errors."""
    pass


class DivisionByZeroError(CalculatorError):
    """Raised when attempting to divide by zero."""

    def __init__(self, current_result: float):
        self.current_result = current_result
        super().__init__(
            f"Cannot divide by zero. Current result: {current_result}"
        )


class InvalidOperationError(CalculatorError):
    """Raised when an unsupported operation is requested."""

    def __init__(self, operation: str, available_operations: list):
        self.operation = operation
        self.available_operations = available_operations
        super().__init__(
            f"Operation '{operation}' not supported. "
            f"Available: {', '.join(available_operations)}"
        )


class InvalidInputError(CalculatorError):
    """Raised when input validation fails."""

    def __init__(self, value, expected_type):
        self.value = value
        self.expected_type = expected_type
        super().__init__(
            f"Invalid input: {value}. Expected {expected_type}"
        )


# ============================================================================
# FILE: calculator/calculator.py (Robustness)
# ============================================================================

from typing import Dict, Union
import logging

from .exceptions import (
    DivisionByZeroError,
    InvalidOperationError,
    InvalidInputError
)
from .operations import Operation, Addition, Subtraction, Multiplication, Division


logger = logging.getLogger(__name__)


class Calculator:
    """
    Robust calculator with comprehensive error handling.

    This implementation prioritizes reliability and defensive programming.
    All edge cases are handled with clear, actionable error messages.
    """

    def __init__(self):
        """Initialize calculator with result of 0."""
        self._result: float = 0
        self._operations: Dict[str, Operation] = self._setup_operations()
        logger.info("Calculator initialized with result=0")

    def _setup_operations(self) -> Dict[str, Operation]:
        """Set up available operations with validation."""
        return {
            'add': Addition(),
            'subtract': Subtraction(),
            'multiply': Multiplication(),
            'divide': Division(),
        }

    def _validate_input(self, value: Union[int, float]) -> None:
        """
        Validate input value.

        Args:
            value: Value to validate

        Raises:
            InvalidInputError: If value is not a number
        """
        if not isinstance(value, (int, float)):
            raise InvalidInputError(value, "int or float")

        if isinstance(value, float):
            if value != value:  # NaN check
                raise InvalidInputError(value, "valid number (not NaN)")
            if value == float('inf') or value == float('-inf'):
                raise InvalidInputError(value, "finite number")

    def execute(self, operation: str, value: Union[int, float]) -> float:
        """
        Execute an operation with comprehensive validation.

        Args:
            operation: Operation name
            value: Value to use in operation

        Returns:
            New result after operation

        Raises:
            InvalidOperationError: If operation not supported
            DivisionByZeroError: If dividing by zero
            InvalidInputError: If input validation fails
        """
        # Validate inputs
        self._validate_input(value)

        if operation not in self._operations:
            raise InvalidOperationError(
                operation,
                list(self._operations.keys())
            )

        # Special handling for division by zero
        if operation == 'divide' and value == 0:
            logger.error(f"Division by zero attempted. Current result: {self._result}")
            raise DivisionByZeroError(self._result)

        # Execute operation
        try:
            op = self._operations[operation]
            old_result = self._result
            self._result = op.execute(self._result, value)
            logger.debug(
                f"Operation '{operation}' executed: {old_result} -> {self._result}"
            )
            return self._result
        except Exception as e:
            logger.error(f"Operation '{operation}' failed: {e}")
            raise

    def get_result(self) -> float:
        """
        Get current result.

        Returns:
            Current calculator result
        """
        return self._result

    def reset(self) -> None:
        """Reset result to 0."""
        old_result = self._result
        self._result = 0
        logger.info(f"Calculator reset: {old_result} -> 0")


# ============================================================================
# ALTERNATIVE: Even More Defensive (TOO EXTREME)
# ============================================================================

import threading
from enum import Enum


class CalculatorState(Enum):
    """Calculator state for state machine."""
    READY = 1
    CALCULATING = 2
    ERROR = 3


class UltraRobustCalculator:
    """
    Maximum robustness - probably overkill.

    Includes thread locks, state machine, extensive validation, etc.
    """

    def __init__(self):
        self._result: float = 0
        self._lock = threading.Lock()
        self._state = CalculatorState.READY
        self._operation_history = []
        self._error_count = 0
        self._max_errors = 10

    def execute(self, operation: str, value: float) -> float:
        """Execute with thread safety and state management."""
        with self._lock:
            if self._state == CalculatorState.ERROR:
                raise CalculatorError("Calculator in error state. Reset required.")

            if self._error_count >= self._max_errors:
                raise CalculatorError("Too many errors. Calculator locked.")

            try:
                self._state = CalculatorState.CALCULATING
                # ... validation and execution ...
                self._state = CalculatorState.READY
                self._operation_history.append((operation, value))
                return self._result
            except Exception as e:
                self._error_count += 1
                self._state = CalculatorState.ERROR
                logger.error(f"Error #{self._error_count}: {e}")
                raise


# ============================================================================
# STRENGTHS OF THIS APPROACH
# ============================================================================

"""
✅ Custom Exception Hierarchy: Specific errors for specific problems
✅ Comprehensive Validation: NaN, infinity, type checks
✅ Defensive Programming: Check everything
✅ Clear Error Messages: Users know exactly what went wrong
✅ Logging: Track what happens for debugging
✅ Edge Case Handling: All corner cases covered

WEAKNESSES:
❌ Overhead: Validation adds latency
❌ Complexity: More code to maintain
❌ Logging Noise: Can be verbose in production
❌ Thread Locks: Unnecessary for single-threaded calculator
❌ State Machine: Overkill for simple calculator
"""
