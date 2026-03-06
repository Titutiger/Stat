# src/stat/distributions/negative_binomial.py

import math
import numpy as np
from typing import Union

class NegativeBinomial:
    """
    Models the number of failures (k) before the r-th success.
    Supported on k >= 0.
    """
    def __init__(self, r: int, p: float):
        if r <= 0:
            raise ValueError("Number of target successes (r) must be > 0.")
        if not (0.0 < p <= 1.0):
            raise ValueError("Probability (p) must be between 0.0 (exclusive) and 1.0.")
        self.r = r
        self.p = p

    def pmf(self, k: Union[int, np.ndarray]) -> Union[float, np.ndarray]:
        """Calculates the Probability Mass Function: P(X = k)"""
        def _pmf(x):
            if x < 0 or not float(x).is_integer():
                return 0.0
            # Formula: nCr(k + r - 1, k) * p^r * (1 - p)^k
            return math.comb(int(x) + self.r - 1, int(x)) * (self.p ** self.r) * ((1 - self.p) ** x)

        if isinstance(k, np.ndarray):
            return np.vectorize(_pmf)(k)
        return _pmf(k)

    def cdf(self, k: Union[int, np.ndarray]) -> Union[float, np.ndarray]:
        """Calculates the Cumulative Distribution Function: P(X <= k)"""
        def _cdf(x):
            if x < 0:
                return 0.0
            return sum(self.pmf(i) for i in range(int(x) + 1))

        if isinstance(k, np.ndarray):
            return np.vectorize(_cdf)(k)
        return _cdf(k)

    def __repr__(self):
        return f"NegativeBinomial(r={self.r}, p={self.p})"