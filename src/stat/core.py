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

        self.dim = self.data.shape[1] if self.is_df else 1

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

    @property
    def shape(self):
        if self.is_df:
            return self.data.shape
        return self.data.shape

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
    #def _apply(self, func, *args, **kwargs):
    #    if self.is_df:
    #        return self.data.apply(lambda col: func(col.values, *args, **kwargs))
    #    return func(self.data, *args, **kwargs)

    def _apply(self, func, target_column: str = None, *args, **kwargs):
        if self.is_df:
            # If a specific column is requested
            if target_column is not None:
                # Case-insensitive lookup
                col_map = {str(c).lower(): c for c in self.data.columns}
                col_name = str(target_column).lower()

                if col_name not in col_map:
                    raise ValueError(f"Column '{target_column}' not found.")

                # Extract the underlying numpy array for that column and run the func
                return func(self.data[col_map[col_name]].values, *args, **kwargs)

            # Default behavior: run on all numeric columns
            return self.data.apply(lambda col: func(col.values, *args, **kwargs))

        # Logic for 1D arrays i.e (lists/numpy)
        return func(self.data, *args, **kwargs)


    # =========================
    # Descriptive Statistics
    # =========================


    def mean(self, method: str = "arithmetic", series: str = None, skipna: bool = True) -> Union[float, pd.Series]:
        def _mean(arr):
            # NaNs
            if skipna:
                arr = arr[~np.isnan(arr)] # here, ~ finds the opposite.
                # if isnan finds the NaNs, then ~isnan finds the NOT NaNs.
            n = len(arr)

            if n == 0:
                return float('non')

            method_clean = method.lower()

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

        return self._apply(_mean, target_column=series)

    def median(self, series: str = None, skipna: bool = True) -> Union[float, pd.Series]:
        def _median(arr):
            if skipna:
                arr = arr[~np.isnan(arr)]
            n = len(arr)
            if n == 0:
                return float('nan')

            sorted_data = np.sort(arr)
            mid = n // 2

            if n % 2 == 1:
                return float(sorted_data[mid])
            else:
                return float((sorted_data[mid - 1] + sorted_data[mid]) / 2)

        return self._apply(_median, target_column=series)

    def mode(self, series: str = None, skipna: bool = True) -> Union[float, pd.Series]:
        def _mode(arr):
            if skipna:
                arr = arr[~np.isnan(arr)]
            if len(arr) == 0:
                return float('nan')

            values, counts = np.unique(arr, return_counts=True)
            max_count = np.max(counts)
            modes = values[counts == max_count]
            return float(modes[0])  # Returns first mode if multimodal

        return self._apply(_mode, target_column=series)

# ---------

    def variance(self, sample: bool = False, series: str = None, skipna: bool = True) -> Union[float, pd.Series]:
        def _variance(arr):
            if skipna:
                arr = arr[~np.isnan(arr)]
            n = len(arr)
            if n == 0 or (sample and n < 2):
                return float('nan')

            mean_value = np.mean(arr)
            squared_diffs = (arr - mean_value) ** 2
            denominator = n - 1 if sample else n
            return float(np.sum(squared_diffs) / denominator)

        return self._apply(_variance, series)

    def std(self, sample: bool = False, series: str = None, skipna: bool = True) -> Union[float, pd.Series]:
        var = self.variance(sample=sample, series=series, skipna=skipna)
        return var.apply(math.sqrt) if isinstance(var, pd.Series) else float(math.sqrt(var))

    def mad(self, series: str = None, skipna: bool = True) -> Union[float, pd.Series]:
        def _mad(arr):
            if skipna:
                arr = arr[~np.isnan(arr)]
            if len(arr) == 0:
                return float('nan')
            dataset_median = np.median(arr)
            ab_dev = np.abs(arr - dataset_median)
            return float(np.mean(ab_dev))
        return self._apply(_mad, target_column=series)

    def percentile(self, q: float, series: str = None, skipna: bool = True) -> Union[float, pd.Series]:
        if not (0 <= q <= 100):
            raise ValueError("Percentile 'q' must be between 0 and 100.")

        def _percentile(arr):
            if skipna:
                arr = arr[~np.isnan(arr)]

            if len(arr) == 0:
                return float('nan')

            return float(np.percentile(arr, q))

        return self._apply(_percentile, target_column=series)

    def quantile(self, q: float, series: str = None, skipna: bool = True) -> Union[float, pd.Series]:
        if not (0.0 <= q <= 1.0):
            raise ValueError("Quantile 'q' must be between 0.0 and 1.0.")

        return self.percentile(q * 100, series=series, skipna=skipna)

    def iqr(self, series: str = None, skipna: bool = True) -> Union[float, pd.Series]:
        q3 = self.quantile(0.75, series=series, skipna=skipna)
        q1 = self.quantile(0.25, series=series, skipna=skipna)
        return q3 - q1

# ---------

    def min(self, series: str = None, skipna: bool = True) -> Union[float, pd.Series]:
        def _min(arr):
            if skipna:
                arr = arr[~np.isnan(arr)]
            if len(arr) == 0:
                return float('nan')
            return float(np.min(arr))
        return self._apply(_min, series)

    def max(self, series: str = None, skipna: bool = True) -> Union[float, pd.Series]:
        def _max(arr):
            if skipna:
                arr = arr[~np.isnan(arr)]
            if len(arr) == 0:
                return float('nan')
            return float(np.max(arr))

        return self._apply(_max, target_column=series)

    def range(self, series: str = None, skipna: bool = True) -> Union[float, pd.Series]:
        return self.max(series=series, skipna=skipna) - self.min(series=series, skipna=skipna)

    def summary(self, series: str = None, skipna: bool = True) -> Union[dict, pd.DataFrame]:
        stats = {
            "mean": self.mean(series=series, skipna=skipna),
            "median": self.median(series=series, skipna=skipna),
            "variance": self.variance(series=series, skipna=skipna),
            "std": self.std(series=series, skipna=skipna),
            "mad": self.mad(series=series, skipna=skipna),
            "25%": self.percentile(q=25, series=series, skipna=skipna),
            "75%": self.percentile(q=75, series=series, skipna=skipna),
            "iqr": self.iqr(series=series, skipna=skipna),
            "min": self.min(series=series, skipna=skipna),
            "max": self.max(series=series, skipna=skipna),
            "range": self.range(series=series, skipna=skipna),
        }

        if self.is_df and series is None:
            # Convert dictionary of Series into a neatly formatted DataFrame
            return pd.DataFrame(stats)
        return stats