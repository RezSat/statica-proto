"""Execution context for Statica.

This module manages the runtime state, including variables, datasets, and user-provided tables.
It provides methods for safe access and modification of the state.
"""

from typing import Dict, Any, Optional
import pandas as pd  # Assuming datasets are Pandas DataFrames
import logging

logger = logging.getLogger(__name__)

class Context:
    """Manages runtime state for Statica execution."""

    def __init__(self) -> None:
        """Initialize the context with empty state."""
        self.env: Dict[str, Any] = {}  # Variables, datasets, results
        self.user_tables: Dict[str, Any] = {}  # User-provided table values

    def set_var(self, name: str, value: Any) -> None:
        """Set a variable in the environment.

        Args:
            name: The variable name.
            value: The value to assign.
        """
        self.env[name] = value
        logger.info(f"Set variable '{name}'")

    def get_var(self, name: str) -> Any:
        """Get a variable from the environment.

        Args:
            name: The variable name.

        Returns:
            The variable value.

        Raises:
            RuntimeError: If the variable does not exist.
        """
        if name not in self.env:
            raise RuntimeError(f"Variable '{name}' not found")
        return self.env[name]

    def var_exists(self, name: str) -> bool:
        """Check if a variable exists in the environment.

        Args:
            name: The variable name.

        Returns:
            True if the variable exists, False otherwise.
        """
        return name in self.env

    def dataset_exists(self, name: str) -> bool:
        """Check if a dataset exists and is a DataFrame.

        Args:
            name: The dataset name.

        Returns:
            True if it exists and is a pandas DataFrame, False otherwise.
        """
        return name in self.env and isinstance(self.env[name], pd.DataFrame)

    def set_user_table(self, key: str, value: Any) -> None:
        """Set a user-provided table value.

        Args:
            key: The table key.
            value: The value to store.
        """
        self.user_tables[key] = value
        logger.info(f"Set user table '{key}'")

    def get_user_table(self, key: str) -> Optional[Any]:
        """Get a user-provided table value.

        Args:
            key: The table key.

        Returns:
            The value if exists, else None.
        """
        return self.user_tables.get(key)