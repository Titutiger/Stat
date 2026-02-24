# core.py

import numpy as np
import math
import pandas as pd
from typing import Any

# ...

# trying classes
class Stat:
    def __init__(self, data: Any):
        self.data = self._transform(data)
        self._validate()

    # =========================
    # Internal Utilities
    # =========================

    @staticmethod
    def _transform(obj: Any, to: str = 'n.ndarray') -> np.ndarray | pd.DataFrame:
        """
        Transforms selected datatypes to np.ndarray.
        - Takes an object `obj` and converts to `to`.

        Currently, can convert:
        list | tuple | set | pd.DataFrame -> np.ndarray
        """
        def log_str(reason: str | Exception) -> str:
            return f"Could not convert {obj} to {to} because:\n{reason}"

        try: arr = np.asarray(obj)
        except Exception as e: raise ValueError(log_str(e))

        return arr

    def _validate(self) -> None:
        if self.data.ndim != 1:
            raise ValueError("Data must be 1-dimensional.")
        if len(self.data) == 0:
            raise ValueError("Data cannot be empty.")


    # =========================
    # Descriptive Statistics
    # =========================

    def mean(self, method: str = "arithmetic") -> float | str:
        method = method.lower()
        n = len(self.data)

        if method in ("a", "ari", "arithmetic"):
            return float(np.sum(self.data) / n)


        elif method in ("g", "geo", "geometric"):
            if np.any(self.data <= 0):
                raise ValueError("Geometric mean requires all values > 0.")

            return float(np.prod(self.data) ** (1 / n))

        elif method in ("h", "har", "harmonic"):
            if np.any(self.data == 0):
                raise ValueError("Harmonic mean undefined for zero values.")

            return float(n / np.sum(1 / self.data))

        else:
            raise ValueError("Invalid mean method.")

    def median(self, return_index: bool = False):
        sorted_indices = np.argsort(self.data)
        sorted_data = self.data[sorted_indices]
        n = len(sorted_data)

        if n % 2 == 1:
            mid = n // 2
            value = float(sorted_data[mid])

            if return_index:
                original_index = int(sorted_indices[mid])
                return {
                    "index": original_index,
                    "value": value
                }
            return value

        else:
            mid1 = n // 2 - 1
            mid2 = n // 2

            value = float((sorted_data[mid1] + sorted_data[mid2]) / 2)

            if return_index:
                return {
                    "index": (int(sorted_indices[mid1]), int(sorted_indices[mid2])),
                    "value": value
                }
            return value

    def mode(self) -> float:
        values, counts = np.unique(self.data, return_counts=True)
        max_count = np.max(counts)
        modes = values[counts == max_count]
        return float(modes if len(modes) > 1 else float(modes[0]))

    def variance(self, sample: bool = False) -> float:
        n = len(self.data)

        if sample and n < 2:
            raise ValueError("Sample variance requires at least 2 data points.")

        mean_value = self.mean()
        squared_diffs = (self.data - mean_value) ** 2

        denominator = n - 1 if sample else n

        return float(np.sum(squared_diffs) / denominator)

    def std(self, sample: bool = False) -> float:
        return float(math.sqrt(self.variance(sample=sample)))

    def min(self) -> float:
        return float(np.min(self.data))

    def max(self) -> float:
        return float(np.max(self.data))

    def range(self) -> float:
        return self.max() - self.min()

    def summary(self) -> dict:
        return {
            "mean": self.mean(),
            "median": self.median(),
            "variance": self.variance(),
            "std": self.std(),
            "min": self.min(),
            "max": self.max(),
            "range": self.range(),
        }