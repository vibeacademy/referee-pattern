"""
Referee Pattern Implementation

A comprehensive referee system combining maintainability, performance,
and robustness best practices.

Public API:
- Action: Immutable domain object representing an action
- ValidationResult: Result of validation with status and metadata
- Rule: Abstract base class for validation rules
- ValidationRule: Base implementation with template method pattern
- Referee: Central coordinator for rule evaluation
- RefereeError: Base exception for all referee errors
"""

from referee.models import Action, ValidationResult
from referee.rules import Rule, ValidationRule
from referee.referee import Referee
from referee.exceptions import (
    RefereeError,
    ValidationError,
    InvalidStateError,
    ResourceExhaustedError,
)

__all__ = [
    'Action',
    'ValidationResult',
    'Rule',
    'ValidationRule',
    'Referee',
    'RefereeError',
    'ValidationError',
    'InvalidStateError',
    'ResourceExhaustedError',
]
