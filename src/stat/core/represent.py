# core/represent.py

import numpy as np
import pandas as pd
from typing import Any, Optional, Union
from .operations import DescriptiveMixin
from ..inferential import InferentialMixin
from ..themes import THEMES, get_rich_box

try:
    from rich.console import Console
    from rich.table import Table
    HAS_RICH = True
except ImportError:
    HAS_RICH = False


class Stat(DescriptiveMixin, InferentialMixin):
    def __init__(self, data: Any, tag: str = "other"):
        if isinstance(data, pd.DataFrame):
            self.raw_df = data.copy()
        else:
            self.raw_df = None

        self.data = self._transform(data)
        self.is_df = isinstance(self.data, pd.DataFrame)
        self.is_series = isinstance(self.data, pd.Series)
        self.is_1d = self.is_series or (not self.is_df and getattr(self.data, 'ndim', 1) == 1)
        
        self._validate()

        self.tag = tag
        if self.is_df:
            self.dim = self.data.select_dtypes(include=[np.number]).shape[1]
        else:
            self.dim = 1
        self.theme = "default"

    # =========================
    # Magic Methods & Properties
    # =========================

    def __add__(self, other):
        if not isinstance(other, Stat):
            raise TypeError('Can only add another Stat object.')
        if self.is_df or other.is_df:
            # combined = pd.concat([self.data, other.data], ignore_index=True)
            pass
        else:
            combined = np.concatenate((self.data, other.data))
        return represent(combined)  # Uses the factory function to return a new object!

    def __repr__(self):
        if HAS_RICH and self.theme:
            # Return a string that rich can handle if printed, 
            # but for standard REPL we might still want a string.
            # However, usually in interactive sessions, we want to see the table.
            return f"Stat(tag='{self.tag}', theme='{self.theme}')"
        return f"Stat(tag='{self.tag}', data=\n{self.data})"

    def show(self, title: str = f'Stat Object', theme: Optional[str] = None,
             max_rows: Union[int, str, None] = None, max_columns: Union[int, str, None] = None,
             width: Union[int, str, None] = None):
        """Displays the data using Rich tables if available, otherwise falls back to pandas."""
        current_theme_name = theme or self.theme

        if self.is_df:
            df = self.data
        else:
            df = pd.DataFrame(self.data, columns=["Value"])

        if max_rows in [None, 'default']:
            actual_max_rows = 20
        elif max_rows in ['all', '*']:
            actual_max_rows = len(df)
        else:
            actual_max_rows = int(max_rows)

        if max_columns in [None, 'all', '*']:
            actual_max_columns = len(df.columns)
        else:
            actual_max_columns = int(max_columns)

        df_to_show = df.iloc[:actual_max_rows, :actual_max_columns]

        if not HAS_RICH:
            print(df_to_show)
            if len(df) > actual_max_rows or len(df.columns) > actual_max_columns:
                print(f"... ({len(df)} rows x {len(df.columns)} columns)")
            return

        console = Console()
        theme_cfg = THEMES.get(current_theme_name, THEMES["default"])["rich"]

        expand_table = False
        table_width = None
        if width == '*':
            expand_table = True
        elif isinstance(width, int):
            table_width = width

        table = Table(
            title=title,
            box=get_rich_box(theme_cfg["box_style"]),
            header_style=theme_cfg["header"],
            width=table_width,
            expand=expand_table
        )

        table.add_column("Index", justify="right", style=theme_cfg["index"])

        for column in df_to_show.columns:
            table.add_column(str(column), style=theme_cfg["row"], overflow="fold")

        for index, row in df_to_show.iterrows():
            row_values = [str(val) for val in row]
            row_values.insert(0, str(index))
            table.add_row(*row_values)

        if len(df) > actual_max_rows or len(df.columns) > actual_max_columns:
            footer_vals = ["..." for _ in df_to_show.columns]
            table.add_row("...", *footer_vals)

        console.print(table)

    def plot(self, columns: Optional[Union[str, list]] = None, title: Optional[str] = None, theme: Optional[str] = None, **kwargs):
        """Displays graphs using matplotlib and seaborn with theme support."""
        from ..graphs.plotter import plot_stat
        
        current_theme_name = theme or self.theme
        plot_title = title or f"Stat Plot ({self.tag})"
        
        plot_stat(
            data=self.data,
            is_df=self.is_df,
            is_1d=self.is_1d,
            theme_name=current_theme_name,
            title=plot_title,
            columns=columns,
            **kwargs
        )

    def crosstab(self, index: str, columns: str, margins: bool = False):
        """
        Computes a cross-tabulation (frequency matrix) of two categorical columns.
        Returns a new Stat object so it can be chained with .show()
        """
        if not self.is_df:
            raise TypeError("crosstab requires a Pandas DataFrame.")

        if index not in self.data.columns:
            raise ValueError(f"Index column '{index}' not found.")
        if columns not in self.data.columns:
            raise ValueError(f"Columns column '{columns}' not found.")

        # Calculate the matrix using Pandas
        ct_df = pd.crosstab(self.data[index], self.data[columns], margins=margins)

        return represent(ct_df)

    def filter_types(self, keep: str = 'numeric'):
        """
        Filters a DataFrame to keep only numeric or non-numeric columns.
        Returns a new Stat object so operations can be chained.
        """
        if not self.is_df:
            # 1D arrays are already guaranteed to be numeric by your engine
            return self

        keep = keep.lower()

        if keep in ['numeric', 'num', 'n']:
            filtered_df = self.data.select_dtypes(include=[np.number])
        elif keep in ['categorical', 'cat', 'c', 'other', 'non_numeric', 'nn']:
            filtered_df = self.data.select_dtypes(exclude=[np.number])
        elif keep == 'all':
            filtered_df = self.data
        else:
            raise ValueError("keep parameter must be 'numeric', 'categorical', or 'all'")

        # Return a brand new Stat object using your factory!
        # (Assuming 'represent' is imported or available in this file)
        return represent(filtered_df)

    def transform(self, col: str, mapping: list[str]):
        """
        Replaces specific values in a DataFrame column.
        Expects a flat list of pairs: ['Old1', 'New1', 'Old2', 'New2']
        """
        if not self.is_df:
            raise TypeError("transform() can only be used on DataFrames.")

        if not col or col not in self.data.columns:
            raise ValueError(f"Column '{col}' not found in data.")

        if not mapping:
            return self  # Nothing to do

        if len(mapping) % 2 != 0:
            raise ValueError("`mapping` must be a list with an even number of elements. \nEx: ['OldValue', 'NewValue']")

        iterator = iter(mapping)
        mapping_dict = dict(zip(iterator, iterator))
        self.data[col] = self.data[col].replace(mapping_dict)

        return self

    def count_value(self, col: str, target: Any) -> int:
        """Counts how many times a specific value appears in a column."""
        # Use raw_df to ensure we can search for strings!
        df_to_search = self.raw_df if self.raw_df is not None else self.data

        if col not in df_to_search.columns:
            raise ValueError(f"Column '{col}' not found.")

        return int((df_to_search[col] == target).sum())



    @property
    def shape(self):
        return self.data.shape



    # =========================
    # Internal Utilities
    # =========================

    @staticmethod
    def _transform(obj: Any, to: str = 'np.ndarray') -> np.ndarray | pd.DataFrame | pd.Series:
        if isinstance(obj, (pd.DataFrame, pd.Series)):
            return obj
        try:
            return np.asarray(obj, dtype=float)
        except Exception as e:
            raise ValueError(f'Could not convert input because:\n{e}')

    def _validate(self) -> None:
        if not self.is_df and self.data.ndim != 1:
            raise ValueError("Data must be 1-dimensional.")
        if len(self.data) == 0 or (self.is_df and self.data.empty):
            raise ValueError("Data cannot be empty.")

    def _apply(self, func, target_column: str = None, *args, **kwargs):
        if self.is_df:
            if target_column is not None:
                col_map = {str(c).lower(): c for c in self.data.columns}
                col_name = str(target_column).lower()
                if col_name not in col_map:
                    raise ValueError(f"Column '{target_column}' not found.")
                return func(self.data[col_map[col_name]].values, *args, **kwargs)
            
            # Apply only to numeric columns by default
            numeric_data = self.data.select_dtypes(include=[np.number])
            return numeric_data.apply(lambda col: func(col.values, *args, **kwargs))
        return func(self.data, *args, **kwargs)


# =========================
# The Factory Function
# =========================

def represent(data: Any) -> Stat:
    """
    Converts input data into a Stat object and automatically tags its origin.
    Works identically to np.array() converting data to an np.ndarray.
    """
    # Auto-tagging logic from your previous Represent class
    if isinstance(data, pd.DataFrame):
        tag = "dataframe"
    elif isinstance(data, (list, tuple)):
        tag = "ordered"
    elif isinstance(data, set):
        tag = "unordered"
    elif isinstance(data, str):
        tag = 'grouped'
    elif isinstance(data, np.ndarray):
        tag = "numpy"
    else:
        tag = "other"

    return Stat(data, tag=tag)


def from_grouped(frequency_dict: dict):
    """
    Takes grouped data (ranges and frequencies) and expands it into an array
    of midpoints that the Stat class can understand.
    """
    unpacked_data = []

    for class_range, frequency in frequency_dict.items():
        # 1. Split the string "10-20" into 10 and 20
        lower, upper = class_range.split('-')

        # 2. Find the midpoint: (10 + 20) / 2 = 15.0
        midpoint = (float(lower) + float(upper)) / 2.0

        # 3. Add that midpoint to our list 'frequency' times
        # e.g., if frequency is 3, this adds [15.0, 15.0, 15.0]
        unpacked_data.extend([midpoint] * frequency)

    # Return it through your existing factory function!
    return represent(unpacked_data)

