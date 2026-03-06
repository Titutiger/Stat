# src/stat/distributions/poisson.py

import math
import numpy as np
from typing import Union


class Poisson:
    """
    A standalone Poisson Distribution object.
    Models the probability of a given number of events occurring in a fixed interval.
    """

    def __init__(self, lam: float):
        if lam <= 0:
            raise ValueError("Rate parameter (lam) must be > 0.")
        self.lam = lam

    def pmf(self, k: Union[int, np.ndarray]) -> Union[float, np.ndarray]:
        """Calculates the Probability Mass Function: P(X = k)"""

        def _pmf(x):
            # Poisson is only defined for non-negative integers
            if x < 0 or not float(x).is_integer():
                return 0.0
            return ((self.lam ** x) * math.exp(-self.lam)) / math.factorial(int(x))

        # Support passing in a whole array of values at once
        if isinstance(k, np.ndarray):
            return np.vectorize(_pmf)(k)
        return _pmf(k)

    def cdf(self, k: Union[int, np.ndarray]) -> Union[float, np.ndarray]:
        """Calculates the Cumulative Distribution Function: P(X <= k)"""

        def _cdf(x):
            if x < 0:
                return 0.0
            # Sum the PMF from 0 up to k
            return sum(self.pmf(i) for i in range(int(x) + 1))

        if isinstance(k, np.ndarray):
            return np.vectorize(_cdf)(k)
        return _cdf(k)

    def __repr__(self):
        return f"Poisson(lam={self.lam})"