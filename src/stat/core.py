# core.py

import numpy as np
import math
import pandas as pd
from typing import Any, Union

# ---

class Stat:
    def __init__(self, data: Any):
        self.is_1d = False
        self.is_df = isinstance(data, pd.DataFrame) # checks for pd.DataFrame dtype
        self.data = self._transform(data)
        self._validate()

        self.dim = self.data.shape[1]

    # =========================
    # Magic Methods
    # =========================

    def __add__(self, other):
        if not isinstance(other, Stat):
            raise TypeError('Can only add another Stat object.')

        if self.is_df or other.is_df:
            #combined = pd.concat([self.data, other.data], ignore_index=True)
            ...
        else:
            combined = np.concatenate((self.data, other.data))
        return Stat(combined)

    def __repr__(self):
        return f'{self.data}'

    # =========================
    # Internal Utilities
    # =========================

    @staticmethod
    def _transform(obj: Any, to: str = 'np.ndarray') -> np.ndarray | pd.DataFrame:
        """
        Transforms selected datatypes to np.ndarray.
        - Takes an object `obj` and converts to `to`.

        Currently, can convert:
        list | tuple | set | pd.DataFrame -> np.ndarray
        """

        if isinstance(obj, pd.DataFrame):
            # drops non-number items
            numeric_df = obj.select_dtypes(include=[np.number])
            return numeric_df

        try:
            arr = np.asarray(obj, dtype=float)
            return arr
        except Exception as e:
            raise ValueError(f'Could not convert input because:\n{e}')


    def _validate(self) -> None:
        if not self.is_df and self.data.ndim != 1:
            raise ValueError("Data must be 1-dimensional.")
        if len(self.data) == 0 or (self.is_df and self.data.empty):
            raise ValueError("Data cannot be empty.")

    # Helper to apply 1D logic to either a 1D array or across DataFrame columns
    def _apply(self, func, *args, **kwargs):
        if self.is_df:
            return self.data.apply(lambda col: func(col.values, *args, **kwargs))
        return func(self.data, *args, **kwargs)

    """
    def _apply(self, func, series: str = None, *args, **kwargs):
        if self.is_df:
            if series is not None:
                # Create a lowercase mapping of columns for case-insensitive matching
                col_map = {str(c).lower(): c for c in self.data.columns}
                series_lower = str(series).lower()
                
                if series_lower not in col_map:
                    raise ValueError(f"Column '{series}' not found in the DataFrame.")
                
                actual_col = col_map[series_lower]
                return func(self.data[actual_col].values, *args, **kwargs)
                
            # If no series is specified, apply to all columns as usual
            return self.data.apply(lambda col: func(col.values, *args, **kwargs))
            
        else:
            if series is not None:
                raise ValueError("Cannot specify 'series' for 1-dimensional array data.")
            return func(self.data, *args, **kwargs)
    """

    # =========================
    # Descriptive Statistics
    # =========================


    def mean(self, method: str = "arithmetic") -> Union[float, pd.Series]:
        def _mean(arr):
            method_clean = method.lower()
            n = len(arr)

            if method_clean in ("a", "ari", "arithmetic"):
                return float(np.sum(arr) / n)

            elif method_clean in ("g", "geo", "geometric"):
                if np.any(arr <= 0):
                    raise ValueError("Geometric mean requires all values > 0.")
                # Using the log-mean trick to prevent overflow
                return float(np.exp(np.mean(np.log(arr))))

            elif method_clean in ("h", "har", "harmonic"):
                if np.any(arr == 0):
                    raise ValueError("Harmonic mean undefined for zero values.")
                return float(n / np.sum(1 / arr))

            else:
                raise ValueError("Invalid mean method.")

        return self._apply(_mean)

    def median(self) -> Union[float, pd.Series]:
        def _median(arr):
            sorted_data = np.sort(arr)
            n = len(sorted_data)
            mid = n // 2

            if n % 2 == 1:
                return float(sorted_data[mid])
            else:
                return float((sorted_data[mid - 1] + sorted_data[mid]) / 2)

        return self._apply(_median)

    def mode(self) -> Union[float, pd.Series]:
        def _mode(arr):
            values, counts = np.unique(arr, return_counts=True)
            max_count = np.max(counts)
            modes = values[counts == max_count]
            return float(modes[0])  # Returns first mode if multimodal

        return self._apply(_mode)

    def variance(self, sample: bool = False) -> Union[float, pd.Series]:
        def _variance(arr):
            n = len(arr)
            if sample and n < 2:
                raise ValueError("Sample variance requires at least 2 data points.")

            mean_value = np.mean(arr)
            squared_diffs = (arr - mean_value) ** 2
            denominator = n - 1 if sample else n
            return float(np.sum(squared_diffs) / denominator)

        return self._apply(_variance)

    def std(self, sample: bool = False) -> Union[float, pd.Series]:
        # Variance already handles the 1D/2D routing, so we can just square root the result
        var = self.variance(sample=sample)
        return var.apply(math.sqrt) if self.is_df else float(math.sqrt(var))

    def min(self) -> Union[float, pd.Series]:
        return self._apply(np.min)

    def max(self) -> Union[float, pd.Series]:
        return self._apply(np.max)

    def range(self) -> Union[float, pd.Series]:
        return self.max() - self.min()

    def summary(self) -> Union[dict, pd.DataFrame]:
        stats = {
            "mean": self.mean(),
            "median": self.median(),
            "variance": self.variance(),
            "std": self.std(),
            "min": self.min(),
            "max": self.max(),
            "range": self.range(),
        }

        if self.is_df:
            # Convert dictionary of Series into a neatly formatted DataFrame
            return pd.DataFrame(stats)
        return stats