# src/stat/distributions/geometric.py

import math
import numpy as np
from typing import Union

class Geometric:
    """
    Models the number of trials needed to get the first success.
    Supported on k >= 1.
    """
    def __init__(self, p: float):
        if not (0.0 < p <= 1.0):
            raise ValueError("Probability (p) must be between 0.0 (exclusive) and 1.0.")
        self.p = p

    def pmf(self, k: Union[int, np.ndarray]) -> Union[float, np.ndarray]:
        """Calculates the Probability Mass Function: P(X = k)"""
        def _pmf(x):
            if x < 1 or not float(x).is_integer():
                return 0.0
            # Formula: (1 - p)^(k - 1) * p
            return ((1 - self.p) ** (x - 1)) * self.p

        if isinstance(k, np.ndarray):
            return np.vectorize(_pmf)(k)
        return _pmf(k)

    def cdf(self, k: Union[int, np.ndarray]) -> Union[float, np.ndarray]:
        """Calculates the Cumulative Distribution Function: P(X <= k)"""
        def _cdf(x):
            if x < 1:
                return 0.0
            # Formula: 1 - (1 - p)^k
            return 1 - ((1 - self.p) ** int(x))

        if isinstance(k, np.ndarray):
            return np.vectorize(_cdf)(k)
        return _cdf(k)

    def __repr__(self):
        return f"Geometric(p={self.p})"