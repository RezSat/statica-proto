"""
Abstract base class for Statica commands.

This module defines the base class for all commands (parent class)
Commands encapsulate the logic for executing specific operations like load, ttest, etc.
Subclasses must implement the execute method.
"""

from typing import Any, Dict
from abc import ABC, abstractmethod
from ..core.context import Context
from ..core.exceptions import RuntimeError

class BaseCommand(ABC):
    """Abstract base class for Statica commands."""

    def __init__(self, cmd_dict: Dict[str, Any]) -> None:
        """Initialize the command with its dictionary representation.

        Args:
            cmd_dict: The command dictionary from the AST.
        """
        self.cmd_dict = cmd_dict

    @abstractmethod
    def execute(self, context: Context) -> Any:
        """Execute the command using the provided context.

        Args:
            context: The runtime context.

        Returns:
            The result of the command execution.

        Raises:
            RuntimeError: If execution fails.
        """
        pass