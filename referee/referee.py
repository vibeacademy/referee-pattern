"""
Referee Implementation

The Referee is the central coordinator that applies rules to actions
and produces validation results.

Combines:
- Maintainability: Clean architecture with Chain of Responsibility pattern
- Performance: Efficient rule evaluation with early exit and caching
- Robustness: Comprehensive error handling, thread safety, and resource limits

Design Principles:
- Single Responsibility: Coordinates rule evaluation only
- Open/Closed: Can work with any rules without modification
- Dependency Inversion: Depends on Rule abstraction, not concrete types
- High Cohesion: All methods relate to rule coordination
- Low Coupling: Only depends on abstractions (Rule, Action, ValidationResult)
"""

import logging
from typing import List, Optional
from functools import lru_cache
import threading

from referee.models import Action, ValidationResult, ValidationStatus
from referee.rules import Rule
from referee.exceptions import (
    ValidationError,
    InvalidStateError,
    ResourceExhaustedError,
    ConfigurationError,
)

# Configure logging (from robustness implementation)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Referee:
    """
    Coordinates the evaluation of actions against a set of rules.

    The Referee applies the Chain of Responsibility pattern - each rule
    is evaluated in sequence, and all results are collected into a
    ValidationResult.

    Features:
    - Thread-safe operation (from robustness)
    - Performance-optimized with caching (from performance)
    - Clean, extensible architecture (from maintainability)
    - Comprehensive error handling (from robustness)

    Attributes:
        _rules: The list of rules to apply during validation
        _lock: Thread lock for thread-safe operations
        _validation_count: Counter for tracking validations
        _max_validations: Resource limit for validations

    Example:
        >>> referee = Referee([rule1, rule2])
        >>> result = referee.validate(action)
        >>> if result.is_valid:
        ...     print("Action is valid")
    """

    __slots__ = (
        '_rules',
        '_lock',
        '_validation_count',
        '_max_validations',
        '_enable_caching',
        '_fail_fast',
    )

    def __init__(
        self,
        rules: Optional[List[Rule]] = None,
        max_validations: int = 10000,
        enable_caching: bool = True,
        fail_fast: bool = False,
    ):
        """
        Initialize the referee with a set of rules.

        Args:
            rules: List of Rule instances to apply during validation.
                   If None, an empty list is used (all actions pass).
            max_validations: Maximum number of validations allowed (resource limit)
            enable_caching: Whether to enable result caching for performance
            fail_fast: If True, stop validation at first rule failure

        Raises:
            ConfigurationError: If configuration is invalid
            ValidationError: If rules list contains invalid items
        """
        try:
            # Input validation (from robustness)
            if max_validations < 1 or max_validations > 1000000:
                raise ConfigurationError(
                    f"max_validations must be between 1 and 1,000,000, got {max_validations}"
                )

            # Initialize with default empty list (from maintainability)
            self._rules: List[Rule] = []

            # Thread safety (from robustness) - initialize lock BEFORE using it
            self._lock = threading.Lock()

            # Resource management (from robustness)
            self._validation_count = 0
            self._max_validations = max_validations

            # Performance settings (from performance)
            self._enable_caching = enable_caching
            self._fail_fast = fail_fast

            # Validate and add rules (after lock is initialized)
            if rules is not None:
                if not isinstance(rules, list):
                    raise ValidationError("rules must be a list")
                for rule in rules:
                    self.add_rule(rule)

            logger.info(
                f"Referee initialized with {len(self._rules)} rules, "
                f"max_validations={max_validations}, caching={enable_caching}"
            )

        except Exception as e:
            logger.error(f"Failed to initialize Referee: {str(e)}")
            raise ConfigurationError(f"Referee initialization failed: {str(e)}") from e

    def add_rule(self, rule: Rule) -> None:
        """
        Add a new rule to the referee's validation chain.

        This enables dynamic configuration of the referee at runtime,
        supporting the Builder pattern for constructing complex validators.

        Args:
            rule: The rule to add to the validation chain

        Raises:
            ValidationError: If rule is None or not a Rule instance
        """
        # Input validation (from robustness)
        if rule is None:
            raise ValidationError("Rule cannot be None")

        if not isinstance(rule, Rule):
            raise ValidationError(f"Expected Rule instance, got {type(rule).__name__}")

        with self._lock:  # Thread safety (from robustness)
            self._rules.append(rule)
            logger.debug(f"Added rule: {rule.name}")

    def validate(self, action: Action) -> ValidationResult:
        """
        Validate an action against all configured rules.

        The validation process:
        1. Check resource limits
        2. Validate input
        3. Iterate through all rules in order
        4. Evaluate each rule against the action
        5. Collect all validation messages
        6. Determine overall validity (all rules must pass)

        Performance optimizations:
        - Early exit if fail_fast is enabled
        - Caching of results if enabled
        - Single-pass iteration

        Args:
            action: The action to validate

        Returns:
            A ValidationResult containing the validation status and messages

        Raises:
            ValidationError: If action is invalid
            ResourceExhaustedError: If resource limits exceeded
            InvalidStateError: If referee is in invalid state

        Example:
            >>> action = Action('test', {})
            >>> result = referee.validate(action)
            >>> print(f"Valid: {result.is_valid}")
            >>> print(f"Messages: {result.messages}")
        """
        with self._lock:  # Thread safety (from robustness)
            try:
                # Resource limit check (from robustness)
                if self._validation_count >= self._max_validations:
                    raise ResourceExhaustedError(
                        f"Maximum validation limit of {self._max_validations} reached. "
                        "Consider resetting or increasing the limit."
                    )

                # Input validation (from robustness)
                if action is None:
                    raise ValidationError("Action cannot be None")

                if not isinstance(action, Action):
                    raise ValidationError(f"Expected Action, got {type(action).__name__}")

                # Increment counter
                self._validation_count += 1

                # Use cached validation if enabled (from performance)
                if self._enable_caching:
                    return self._validate_cached(action)
                else:
                    return self._validate_uncached(action)

            except (ValidationError, ResourceExhaustedError):
                # Re-raise known errors
                raise
            except Exception as e:
                # Wrap unexpected errors (from robustness)
                logger.error(f"Unexpected error during validation: {str(e)}")
                raise ValidationError(f"Validation failed: {str(e)}") from e

    def _validate_uncached(self, action: Action) -> ValidationResult:
        """
        Internal validation without caching.

        Args:
            action: The action to validate

        Returns:
            ValidationResult
        """
        messages = []
        is_valid = True
        metadata = {
            'rules_evaluated': 0,
            'rules_passed': 0,
            'rules_failed': 0,
            'validation_number': self._validation_count,
        }

        # Early exit fast path: no rules configured (from performance)
        if not self._rules:
            messages.append("No rules configured - action accepted by default")
            return ValidationResult.create(
                is_valid=True,
                messages=messages,
                metadata=metadata
            )

        # Apply each rule in sequence (Chain of Responsibility from maintainability)
        for rule in self._rules:
            try:
                rule_passed, message = rule.evaluate(action)
                messages.append(f"[{rule.name}] {message}")

                metadata['rules_evaluated'] += 1

                if rule_passed:
                    metadata['rules_passed'] += 1
                else:
                    metadata['rules_failed'] += 1
                    is_valid = False  # One failure means overall failure

                    # Early exit if fail_fast enabled (from performance)
                    if self._fail_fast:
                        logger.debug(f"Fail-fast triggered by rule: {rule.name}")
                        break

            except ValidationError as e:
                # Rule validation failed
                messages.append(f"[{rule.name}] ValidationError: {str(e)}")
                metadata['rules_failed'] += 1
                metadata['rules_evaluated'] += 1
                is_valid = False

                if self._fail_fast:
                    break

            except Exception as e:
                # Unexpected error in rule
                logger.error(f"Rule '{rule.name}' raised unexpected error: {str(e)}")
                messages.append(f"[{rule.name}] Error: {str(e)}")
                metadata['rules_failed'] += 1
                metadata['rules_evaluated'] += 1
                is_valid = False

                if self._fail_fast:
                    break

        return ValidationResult.create(
            is_valid=is_valid,
            messages=messages,
            metadata=metadata
        )

    @lru_cache(maxsize=1024)  # Performance optimization from performance implementation
    def _validate_cached(self, action: Action) -> ValidationResult:
        """
        Cached validation for performance.

        Uses LRU cache with action hash as key.

        Args:
            action: The action to validate

        Returns:
            ValidationResult
        """
        return self._validate_uncached(action)

    def clear_cache(self) -> None:
        """
        Clear the validation cache.

        Useful when rules are modified or updated.
        """
        if hasattr(self._validate_cached, 'cache_clear'):
            self._validate_cached.cache_clear()
            logger.info("Validation cache cleared")

    def reset(self) -> None:
        """
        Reset the referee to initial state.

        Clears validation counter and cache.
        """
        with self._lock:
            self._validation_count = 0
            self.clear_cache()
            logger.info("Referee reset completed")

    @property
    def rule_count(self) -> int:
        """Return the number of rules configured in this referee."""
        return len(self._rules)

    @property
    def validation_count(self) -> int:
        """Return the number of validations performed."""
        return self._validation_count

    @property
    def max_validations(self) -> int:
        """Return the maximum number of validations allowed."""
        return self._max_validations

    def get_stats(self) -> dict:
        """
        Get referee statistics.

        Returns:
            Dictionary with statistics
        """
        return {
            'rule_count': self.rule_count,
            'validation_count': self.validation_count,
            'max_validations': self.max_validations,
            'remaining_validations': self.max_validations - self.validation_count,
            'caching_enabled': self._enable_caching,
            'fail_fast_enabled': self._fail_fast,
        }

    def __repr__(self) -> str:
        """Return a string representation of the referee."""
        return (
            f"Referee(rules={self.rule_count}, "
            f"validations={self.validation_count}/{self.max_validations})"
        )

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup."""
        self.reset()
        return False
