"""
Data-related commands for Statica.

This module implements commands for data operations like load and describe.
These commands interact with data services (stubbed for now).
"""

from typing import Any, Dict
import pandas as pd  # For data loading
from .base import BaseCommand
from statica.core.context import Context
from statica.core.exceptions import RuntimeError

class LoadCommand(BaseCommand):
    """Command for loading datasets."""

    def execute(self, context: Context) -> Any:
        fname = self.cmd_dict["file"]
        header = self.cmd_dict["header"]
        try:
            df = pd.read_csv(fname, header=0 if header else None)
            varname = fname.split("/")[-1].split(".")[0]
            context.set_var(varname, df)
            return df
        except Exception as e:
            raise RuntimeError(f"Error loading file '{fname}': {str(e)}") from e

class DescribeCommand(BaseCommand):
    """Command for describing datasets."""

    def execute(self, context: Context) -> Any:
        dataset_name = self.cmd_dict["dataset"]
        df = context.get_var(dataset_name)
        if not isinstance(df, pd.DataFrame):
            raise RuntimeError(f"'{dataset_name}' is not a dataset.")
        # For now, print description; later use output formatter
        desc = df.describe(include='all').T.reset_index()
        print(desc)  # Replace with proper output in future
        return desc