"""
Performance Agent Implementation - Key Excerpts

Focus: Speed, memory efficiency, minimal overhead
"""

# ============================================================================
# FILE: calculator.py (Performance - Single File)
# ============================================================================

from typing import Union


class Calculator:
    """
    High-performance calculator with minimal overhead.

    Uses __slots__ for memory efficiency and direct method dispatch for speed.
    """

    __slots__ = ['_result']  # ~40% memory reduction

    def __init__(self):
        """Initialize with result of 0."""
        self._result: float = 0

    def add(self, value: Union[int, float]) -> float:
        """Add value to result."""
        self._result += value
        return self._result

    def subtract(self, value: Union[int, float]) -> float:
        """Subtract value from result."""
        self._result -= value
        return self._result

    def multiply(self, value: Union[int, float]) -> float:
        """Multiply result by value."""
        self._result *= value
        return self._result

    def divide(self, value: Union[int, float]) -> float:
        """
        Divide result by value.

        Raises:
            ValueError: If value is 0
        """
        if value == 0:
            raise ValueError("Cannot divide by zero")
        self._result /= value
        return self._result

    def get_result(self) -> float:
        """Get current result."""
        return self._result

    def reset(self) -> None:
        """Reset to 0."""
        self._result = 0


# ============================================================================
# ALTERNATIVE: Even More Performant (TOO EXTREME)
# ============================================================================

class UltraFastCalculator:
    """
    Maximum performance calculator - probably overkill.

    Uses integer IDs, pre-allocated arrays, etc.
    """

    __slots__ = ['_result', '_op_cache']

    def __init__(self):
        self._result: float = 0
        # Pre-cache operation functions (avoid method lookup)
        self._op_cache = {
            0: lambda a, b: a + b,      # add
            1: lambda a, b: a - b,      # subtract
            2: lambda a, b: a * b,      # multiply
            3: lambda a, b: a / b if b != 0 else self._div_error(),  # divide
        }

    def _div_error(self):
        raise ValueError("Cannot divide by zero")

    def execute(self, op_id: int, value: float) -> float:
        """Execute operation by ID (0=add, 1=sub, 2=mul, 3=div)."""
        self._result = self._op_cache[op_id](self._result, value)
        return self._result


# ============================================================================
# STRENGTHS OF THIS APPROACH
# ============================================================================

"""
✅ Memory Efficient: __slots__ reduces memory by ~40%
✅ Fast Dispatch: Direct method calls, no dictionary lookup
✅ Simple: Single file, easy to understand
✅ Minimal Overhead: No abstractions or indirection
✅ Type Hints: JIT-friendly for optimization
✅ O(1) Operations: Constant time for all operations

WEAKNESSES:
❌ Not Extensible: Adding operations requires modifying class
❌ Violates Open/Closed: Can't extend without modification
❌ Single File: All code in one place
❌ Minimal Documentation: Focused on performance over clarity
❌ No Custom Exceptions: Just uses ValueError
"""
