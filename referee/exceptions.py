"""
Custom Exceptions for the Referee System

Comprehensive exception hierarchy for precise error handling.
Inspired by the robustness implementation.
"""


class RefereeError(Exception):
    """Base exception for all referee system errors."""
    pass


class ValidationError(RefereeError):
    """Raised when input validation fails."""
    pass


class InvalidStateError(RefereeError):
    """Raised when the system is in an invalid state for the requested operation."""
    pass


class ResourceExhaustedError(RefereeError):
    """Raised when system resources are exhausted."""
    pass


class ConfigurationError(RefereeError):
    """Raised when system configuration is invalid."""
    pass
