"""Custom exceptions for Statica.

This module defines a hierarchy of exceptions used throughout the Statica system.
These exceptions provide specific error types for better error handling.
"""

class StaticaError(Exception):
    """Base exception for all Statica-related errors."""

class SyntaxError(StaticaError):
    """Raised for syntax errors in the DSL input."""

class ValidationError(StaticaError):
    """Raised for semantic validation failures in the AST."""

class RuntimeError(StaticaError):
    """Raised for errors during command execution."""

class StatisticalAssumptionError(StaticaError):
    """Raised when statistical assumptions are violated (e.g., non-normal data)."""