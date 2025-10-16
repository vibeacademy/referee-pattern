"""
Rule Abstractions for the Referee Pattern

This module defines the rule interfaces and base implementations.
Following the Open/Closed Principle, the system is open for extension
(new rules can be added) but closed for modification (core logic is stable).

Design Principles Applied:
- Single Responsibility: Each rule has one validation concern
- Open/Closed: New rules extend base without modifying core
- Dependency Inversion: Referee depends on Rule abstraction, not concrete types

Combines maintainability's clean architecture with robustness's validation.
"""

from abc import ABC, abstractmethod
from typing import Tuple
from functools import lru_cache

from referee.models import Action
from referee.exceptions import ValidationError


class Rule(ABC):
    """
    Abstract base class for all validation rules.

    This interface defines the contract that all rules must follow,
    enabling the Referee to work with any rule implementation without
    knowing the specific details.

    The Strategy pattern is used here - each rule is a different strategy
    for validating actions.
    """

    @abstractmethod
    def evaluate(self, action: Action) -> Tuple[bool, str]:
        """
        Evaluate an action against this rule.

        Args:
            action: The action to validate

        Returns:
            A tuple of (is_valid, message) where:
            - is_valid: True if the action passes this rule
            - message: Description of the validation result

        Raises:
            ValidationError: If input validation fails

        Example:
            >>> rule = SomeRule()
            >>> is_valid, message = rule.evaluate(action)
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Return a human-readable name for this rule."""
        pass


class ValidationRule(Rule):
    """
    Base implementation for common validation rules.

    This class provides a template method pattern, where subclasses
    override specific validation logic while the evaluation structure
    remains consistent.

    Includes input validation from the robustness implementation.
    """

    __slots__ = ('_name',)  # Performance optimization from performance implementation

    def __init__(self, rule_name: str):
        """
        Initialize the validation rule.

        Args:
            rule_name: A descriptive name for this rule

        Raises:
            ValidationError: If rule_name is invalid
        """
        # Input validation from robustness implementation
        if not rule_name or not isinstance(rule_name, str):
            raise ValidationError("Rule name must be a non-empty string")

        if len(rule_name) > 255:
            raise ValidationError("Rule name exceeds maximum length of 255 characters")

        self._name = rule_name

    @property
    def name(self) -> str:
        """Return the rule name."""
        return self._name

    @abstractmethod
    def _validate(self, action: Action) -> Tuple[bool, str]:
        """
        Concrete validation logic to be implemented by subclasses.

        Args:
            action: The action to validate

        Returns:
            A tuple of (is_valid, message)

        Raises:
            ValidationError: If validation logic encounters an error
        """
        pass

    def evaluate(self, action: Action) -> Tuple[bool, str]:
        """
        Evaluate the action, delegating to the concrete validation logic.

        This method adds input validation and error handling, then delegates
        to the subclass-specific _validate method.

        Args:
            action: The action to validate

        Returns:
            A tuple of (is_valid, message)

        Raises:
            ValidationError: If action is None or validation fails
        """
        # Input validation from robustness implementation
        if action is None:
            raise ValidationError("Action cannot be None")

        if not isinstance(action, Action):
            raise ValidationError(f"Expected Action, got {type(action).__name__}")

        try:
            return self._validate(action)
        except ValidationError:
            # Re-raise ValidationError as-is
            raise
        except Exception as e:
            # Wrap unexpected errors
            raise ValidationError(f"Rule '{self.name}' failed: {str(e)}") from e

    def __repr__(self) -> str:
        """String representation."""
        return f"{self.__class__.__name__}(name='{self.name}')"


class CachedValidationRule(ValidationRule):
    """
    Validation rule with LRU caching for repeated validations.

    Performance optimization from the performance implementation.
    Use this for expensive validation operations.
    """

    def __init__(self, rule_name: str, cache_size: int = 128):
        """
        Initialize cached validation rule.

        Args:
            rule_name: A descriptive name for this rule
            cache_size: Maximum number of cached results
        """
        super().__init__(rule_name)
        self._cache_size = cache_size
        # Create cached version of _validate
        self._cached_validate = lru_cache(maxsize=cache_size)(self._validate_uncached)

    @abstractmethod
    def _validate_uncached(self, action: Action) -> Tuple[bool, str]:
        """
        Concrete validation logic (uncached version).

        Subclasses should implement this instead of _validate.
        """
        pass

    def _validate(self, action: Action) -> Tuple[bool, str]:
        """
        Validate with caching based on action hash.
        """
        # Use action hash for cache key
        return self._cached_validate(hash(action), action.action_type, str(action.data))

    def clear_cache(self) -> None:
        """Clear the validation cache."""
        self._cached_validate.cache_clear()


class ActionTypeRule(ValidationRule):
    """
    Validates that an action has a specific type.

    This is an example of a concrete rule implementation demonstrating
    how to extend the rule system.
    """

    __slots__ = ('_name', '_expected_type')

    def __init__(self, expected_type: str):
        """
        Initialize the action type rule.

        Args:
            expected_type: The action type that is considered valid

        Raises:
            ValidationError: If expected_type is invalid
        """
        if not expected_type or not isinstance(expected_type, str):
            raise ValidationError("Expected type must be a non-empty string")

        super().__init__(f"ActionTypeRule({expected_type})")
        self._expected_type = expected_type

    def _validate(self, action: Action) -> Tuple[bool, str]:
        """Validate the action type."""
        if action.action_type == self._expected_type:
            return True, f"Action type '{action.action_type}' is valid"
        return False, f"Expected action type '{self._expected_type}', got '{action.action_type}'"


class AlwaysValidRule(ValidationRule):
    """
    A rule that always passes validation.

    Useful for testing and as a null object pattern implementation.
    """

    __slots__ = ('_name',)

    def __init__(self):
        """Initialize the always-valid rule."""
        super().__init__("AlwaysValidRule")

    def _validate(self, action: Action) -> Tuple[bool, str]:
        """Always return valid."""
        return True, "Action is valid"
