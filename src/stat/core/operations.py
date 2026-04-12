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

    def corr(self, method: str = "pearson") -> Union[float, 'Stat']:
        """
        Calculates the correlation matrix between columns.
        Supported methods: 'pearson', 'kendall', 'spearman'.
        """
        from .represent import represent
        if not self.is_df:
            # A 1D array perfectly correlates with itself
            return 1.0

            # Pandas automatically handles NaN skipping pairwise for correlation matrices!
        return represent(self.data.corr(method=method))

    # ---------

    def frequencies(self, series: str) -> 'Stat':
        """
        Returns the counts of unique values in a categorical column.
        (Answers: "What is the most frequent model?")
        """
        from .represent import represent
        if self.raw_df is None:
            raise TypeError("Frequencies require a Pandas DataFrame.")
        if series not in self.raw_df.columns:
            raise ValueError(f"Column '{series}' not found in the raw data.")

        # Return the counts, sorted highest to lowest
        counts = self.raw_df[series].value_counts()
        return represent(pd.DataFrame(counts))

    def groupby(self, by: str, operation: str = 'mean') -> 'Stat':
        """
        Groups the data by a categorical column and performs math on the numeric columns.
        (Answers: "What is the mean battery life FOR EACH machine?")
        """
        from .represent import represent
        if self.raw_df is None:
            raise TypeError("GroupBy requires a Pandas DataFrame.")
        if by not in self.raw_df.columns:
            raise ValueError(f"Category column '{by}' not found.")

        # Group the raw data by your chosen column
        grouped = self.raw_df.groupby(by)

        # Apply the requested math, ignoring string columns automatically!
        if operation.lower() == 'mean':
            res = grouped.mean(numeric_only=True)
        elif operation.lower() == 'median':
            res = grouped.median(numeric_only=True)
        elif operation.lower() in ['std', 'standard_deviation']:
            res = grouped.std(numeric_only=True)
        elif operation.lower() in ['max', 'maximum']:
            res = grouped.max(numeric_only=True)
        elif operation.lower() in ['min', 'minimum']:
            res = grouped.min(numeric_only=True)
        else:
            raise ValueError(f"Operation '{operation}' not currently supported in groupby.")
        
        return represent(res)

    def skewness(self, series: str = None, skipna: bool = True, sample: bool = True) -> Union[float, pd.Series]:
        """Calculates the skewness (asymmetry) of the dataset."""

        def _skew(arr):
            if skipna:
                arr = arr[~np.isnan(arr)]
            n = len(arr)

            # Sample skewness requires at least 3 data points
            if n < 3 and sample:
                return float('nan')
            elif n == 0:
                return float('nan')

            mean_val = np.mean(arr)

            # Calculate the 2nd and 3rd central moments
            m2 = np.sum((arr - mean_val) ** 2) / n
            m3 = np.sum((arr - mean_val) ** 3) / n

            if m2 == 0:
                return 0.0

            # Population skewness formula
            pop_skew = m3 / (m2 ** 1.5)

            if sample:
                # Fisher-Pearson standardized moment coefficient for sample skewness
                return float(pop_skew * np.sqrt(n * (n - 1)) / (n - 2))

            return float(pop_skew)

        return self._apply(_skew, target_column=series)

    def kurtosis(self, series: str = None, skipna: bool = True, sample: bool = True) -> Union[float, pd.Series]:
        """Calculates the excess kurtosis (tailedness) of the dataset."""

        def _kurtosis(arr):
            if skipna:
                arr = arr[~np.isnan(arr)]
            n = len(arr)

            # Sample kurtosis requires at least 4 data points
            if n < 4 and sample:
                return float('nan')
            elif n == 0:
                return float('nan')

            mean_val = np.mean(arr)

            # Calculate the 2nd and 4th central moments
            m2 = np.sum((arr - mean_val) ** 2) / n
            m4 = np.sum((arr - mean_val) ** 4) / n

            if m2 == 0:
                return 0.0

            # Population excess kurtosis formula (subtracting 3 normalizes a normal dist to 0)
            pop_kurt = m4 / (m2 ** 2) - 3.0

            if sample:
                # Sample excess kurtosis formula
                val1 = (n - 1) / ((n - 2) * (n - 3))
                val2 = (n + 1) * pop_kurt + 6
                return float(val1 * val2)

            return float(pop_kurt)

        return self._apply(_kurtosis, target_column=series)

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





    def intersect(self, eq1: str, eq2: str):
        ...








    def summary(self, series: str = None, skipna: bool = True) -> Union['Stat', dict]:
        from .represent import represent
        stats = {
            "mean": self.mean(series=series, skipna=skipna),
            "med": self.median(series=series, skipna=skipna),
            "var": self.variance(series=series, skipna=skipna),
            "std": self.std(series=series, skipna=skipna),
            "sem": self.sem(series=series, skipna=skipna),
            "mad": self.mad(series=series, skipna=skipna),
            "skewness": self.skewness(series=series, skipna=skipna),
            "kurtosis": self.kurtosis(series=series, skipna=skipna),
            "25%": self.percentile(q=25, series=series, skipna=skipna),
            "75%": self.percentile(q=75, series=series, skipna=skipna),
            "iqr": self.iqr(series=series, skipna=skipna),
            "min": self.min(series=series, skipna=skipna),
            "max": self.max(series=series, skipna=skipna),
            "range": self.range(series=series, skipna=skipna),
        }

        if self.is_df and series is None:
            return represent(pd.DataFrame(stats))
        
        # If it's 1D, stats are floats. We can wrap it in a DataFrame for .show() if desired,
        # but for now let's return the dict as before, but maybe the user wants it pretty too.
        # Let's return a Stat object even for 1D summary if requested.
        return stats


# ======================================================================================================================