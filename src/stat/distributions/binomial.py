# src/stat/distributions/binomial.py

import math
import numpy as np
from typing import Union


class Binomial:
    """
    A standalone Binomial Distribution object.
    Models the number of successes in 'n' independent trials with probability 'p'.
    """

    def __init__(self, n: int, p: float):
        if n < 0:
            raise ValueError("Number of trials (n) must be >= 0.")
        if not (0.0 <= p <= 1.0):
            raise ValueError("Probability (p) must be between 0.0 and 1.0.")
        self.n = n
        self.p = p

    def pmf(self, k: Union[int, np.ndarray]) -> Union[float, np.ndarray]:
        """Calculates the Probability Mass Function: P(X = k)"""

        def _pmf(x):
            # You cannot have fewer than 0 or more than 'n' successes
            if x < 0 or x > self.n or not float(x).is_integer():
                return 0.0
            # Formula: nCr * p^k * (1-p)^(n-k)
            return math.comb(self.n, int(x)) * (self.p ** x) * ((1 - self.p) ** (self.n - x))

        if isinstance(k, np.ndarray):
            return np.vectorize(_pmf)(k)
        return _pmf(k)

    def cdf(self, k: Union[int, np.ndarray]) -> Union[float, np.ndarray]:
        """Calculates the Cumulative Distribution Function: P(X <= k)"""

        def _cdf(x):
            if x < 0:
                return 0.0
            limit = min(int(x), self.n)
            return sum(self.pmf(i) for i in range(limit + 1))

        if isinstance(k, np.ndarray):
            return np.vectorize(_cdf)(k)
        return _cdf(k)

    def __repr__(self):
        return f"Binomial(n={self.n}, p={self.p})"