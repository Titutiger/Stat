# core.py
from numpy import ndarray

from utils import _conv, _cond

import numpy as np
import math
from typing import Any

'''
def mean(arr: np.ndarray, type_: str) -> float | None:
    if not isinstance(arr, np.ndarray):
        arr = _conv(arr)

    _cond(arr)

    n = len(arr)
    type_ = type_.lower()

    if type_ in ['a', 'ari', 'arithmetic']:
        return float(sum(arr) / n)

    elif type_ in ['g', 'geo', 'geometric']:
        if (arr<0).sum() > 0:
            raise ValueError('Negative values will break geometric mean.')

        return float(np.power(math.prod(arr), 1/n))

    elif type_ in ['h', 'har', 'harmonic']:
        return float(n / np.sum(1/arr))


    else:
        raise ValueError('Enter a valid type of mean.')

    return None

def median(arr: np.ndarray, type_: str) -> float | None:
    if not isinstance(arr, np.ndarray):
        arr = _conv(arr)

    _cond(arr)

    n = len(arr)
    type_ = type_.lower()

    if n % 2 != 0:
        return float(
            (n+1)/2
        )
    elif n % 2 == 0:
        return float(
            (n/2 + (n/2) + 1) / 2
        )


if __name__ == '__main__':
    arr = np.array([1, 2, 3, 4, 5])
    mean(arr, '')

'''


# trying classes
class Stat:
    def __init__(self, data: Any):
        self.data = self._convert(data)
        self._validate()

    # =========================
    # Internal Utilities
    # =========================

    @staticmethod
    def _convert(obj: Any) -> np.ndarray:
        try:
            return np.asarray(obj, dtype=float)
        except Exception:
            raise ValueError("Data cannot be converted to numeric array.")

    def _validate(self) -> None:
        if self.data.ndim != 1:
            raise ValueError("Data must be 1-dimensional.")
        if len(self.data) == 0:
            raise ValueError("Data cannot be empty.")

    # =========================
    # Descriptive Statistics
    # =========================

    def mean(self, method: str = "arithmetic") -> float:
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

    def variance(self, sample: bool = False) -> float:
        ddof = 1 if sample else 0
        return float(np.var(self.data, ddof=ddof))

    def std(self, sample: bool = False) -> float:
        ddof = 1 if sample else 0
        return float(np.std(self.data, ddof=ddof))

    def minimum(self) -> float:
        return float(np.min(self.data))

    def maximum(self) -> float:
        return float(np.max(self.data))

    def range(self) -> float:
        return self.maximum() - self.minimum()

    def summary(self) -> dict:
        return {
            "mean": self.mean(),
            "median": self.median(),
            "variance": self.variance(),
            "std": self.std(),
            "min": self.minimum(),
            "max": self.maximum(),
            "range": self.range(),
        }