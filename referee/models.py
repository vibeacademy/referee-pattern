"""
Domain Models for the Referee Pattern

Immutable data structures with performance optimizations.
Combines maintainability's clean design with performance's memory efficiency.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List
from enum import IntEnum


class ValidationStatus(IntEnum):
    """
    Use IntEnum for fast integer comparison instead of string-based enums.
    Performance optimization from the performance implementation.
    """
    PENDING = 0
    VALID = 1
    INVALID = 2


@dataclass(frozen=True, slots=True)
class Action:
    """
    Represents an action to be validated by the referee system.

    An action encapsulates the type and associated data that needs to be
    evaluated against a set of rules.

    Performance optimizations:
    - frozen=True for immutability and hashability
    - slots=True reduces memory overhead by ~40% (from performance implementation)

    Attributes:
        action_type: A string identifying the type of action
        data: A dictionary containing action-specific data

    Example:
        >>> action = Action('user_registration', {'email': 'user@example.com'})
    """
    action_type: str
    data: Dict[str, Any] = field(default_factory=dict)

    def get(self, key: str, default: Any = None) -> Any:
        """Safely retrieve a value from the action data."""
        return self.data.get(key, default)

    def __hash__(self) -> int:
        """
        Custom hash for performance optimization.
        From performance implementation: fast hashing using action_type only.
        """
        return hash(self.action_type)


@dataclass(frozen=True, slots=True)
class ValidationResult:
    """
    Represents the result of validating an action through the referee system.

    This is the output of the referee's evaluation process, containing both
    the validation status and any relevant messages or metadata.

    Performance optimizations:
    - frozen=True for immutability
    - slots=True for memory efficiency

    Attributes:
        is_valid: Whether the action passed all validation rules
        messages: List of validation messages (errors, warnings, info)
        metadata: Additional data collected during validation

    Example:
        >>> result = ValidationResult(is_valid=False, messages=['Invalid email'])
    """
    is_valid: bool
    messages: tuple[str, ...] = field(default_factory=tuple)  # Tuple is more memory efficient than list
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __bool__(self) -> bool:
        """Allow using the result in boolean contexts."""
        return self.is_valid

    @classmethod
    def create(cls, is_valid: bool, messages: List[str], metadata: Dict[str, Any] = None):
        """
        Factory method for creating ValidationResult with proper type conversion.

        Args:
            is_valid: Whether validation passed
            messages: List of messages (will be converted to tuple)
            metadata: Optional metadata dictionary

        Returns:
            ValidationResult instance
        """
        return cls(
            is_valid=is_valid,
            messages=tuple(messages),
            metadata=metadata or {}
        )
