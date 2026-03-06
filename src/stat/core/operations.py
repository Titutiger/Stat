# core/operations.py

import numpy as np
import pandas as pd
import math
from typing import Union


class DescriptiveMixin:
    """
    Contains all statistical operations.
    Assumes the parent class has `self.data`, `self.is_df`, and `self._apply()`.
    """

    def mean(self, method: str = "arithmetic", series: str = None, skipna: bool = True) -> Union[float, pd.Series]:
        def _mean(arr):
            if skipna:
                arr = arr[~np.isnan(arr)]
            n = len(arr)
            if n == 0: return float('nan')

            method_clean = method.lower()
            if method_clean in ("a", "ari", "arithmetic"):
                return float(np.sum(arr) / n)
            elif method_clean in ("g", "geo", "geometric"):
                return float(np.exp(np.mean(np.log(arr))))
            elif method_clean in ("h", "har", "harmonic"):
                return float(n / np.sum(1 / arr))
            else:
                raise ValueError("Invalid mean method.")

        return self._apply(_mean, target_column=series)

    # Alias
    avg = mean
    x = mean

    def median(self, series: str = None, skipna: bool = True) -> Union[float, pd.Series]:
        def _median(arr):
            if skipna:
                arr = arr[~np.isnan(arr)]
            n = len(arr)
            if n == 0: return float('nan')

            sorted_data = np.sort(arr)
            mid = n // 2
            return float(sorted_data[mid]) if n % 2 == 1 else float((sorted_data[mid - 1] + sorted_data[mid]) / 2)

        return self._apply(_median, target_column=series)

    # Alias
    med = median

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

    # alias
    mod = mode

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

    # alias
    var = variance

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

    # alias
    ptile = percentile

    def quantile(self, q: float, series: str = None, skipna: bool = True) -> Union[float, pd.Series]:
        if not (0.0 <= q <= 1.0):
            raise ValueError("Quantile 'q' must be between 0.0 and 1.0.")

        return self.percentile(q * 100, series=series, skipna=skipna)

    # alias
    qtile = quantile

    def iqr(self, series: str = None, skipna: bool = True) -> Union[float, pd.Series]:
        q3 = self.quantile(0.75, series=series, skipna=skipna)
        q1 = self.quantile(0.25, series=series, skipna=skipna)
        return q3 - q1

    def sem(self, series: str = None, skipna: bool = True) -> Union[float, pd.Series]:
        """Calculates the Standard Error of the Mean (SEM)."""

        def _sem(arr):
            if skipna:
                arr = arr[~np.isnan(arr)]
            n = len(arr)
            # SEM requires at least 2 data points to calculate sample std deviation
            if n < 2:
                return float('nan')

            # Use ddof=1 for sample standard deviation
            sample_std = np.std(arr, ddof=1)
            return float(sample_std / math.sqrt(n))

        return self._apply(_sem, target_column=series)

    def corr(self, method: str = "pearson") -> Union[float, pd.DataFrame]:
        """
        Calculates the correlation matrix between columns.
        Supported methods: 'pearson', 'kendall', 'spearman'.
        """
        if not self.is_df:
            # A 1D array perfectly correlates with itself
            return 1.0

            # Pandas automatically handles NaN skipping pairwise for correlation matrices!
        return self.data.corr(method=method)

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
            "sem": self.sem(series=series, skipna=skipna),       # <--- Added SEM here!
            "mad": self.mad(series=series, skipna=skipna),
            "25%": self.percentile(q=25, series=series, skipna=skipna),
            "75%": self.percentile(q=75, series=series, skipna=skipna),
            "iqr": self.iqr(series=series, skipna=skipna),
            "min": self.min(series=series, skipna=skipna),
            "max": self.max(series=series, skipna=skipna),
            "range": self.range(series=series, skipna=skipna),
        }

        if self.is_df and series is None:
            return pd.DataFrame(stats)
        return stats