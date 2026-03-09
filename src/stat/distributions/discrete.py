# src/stat/distributions/discrete.py

import math
import numpy as np
from typing import Union
from .base import DiscreteDistribution

class Binomial(DiscreteDistribution):
    """
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
        def _pmf(x):
            if x < 0 or x > self.n or not float(x).is_integer():
                return 0.0
            return math.comb(self.n, int(x)) * (self.p ** x) * ((1 - self.p) ** (self.n - x))

        if isinstance(k, np.ndarray):
            return np.vectorize(_pmf)(k)
        return _pmf(k)

    def cdf(self, k: Union[int, np.ndarray]) -> Union[float, np.ndarray]:
        def _cdf(x):
            if x < 0: return 0.0
            limit = min(int(x), self.n)
            return sum(self.pmf(i) for i in range(limit + 1))

        if isinstance(k, np.ndarray):
            return np.vectorize(_cdf)(k)
        return _cdf(k)

    def rvs(self, size=1):
        return np.random.binomial(self.n, self.p, size)

    def mean(self): return self.n * self.p
    def variance(self): return self.n * self.p * (1 - self.p)

    def __repr__(self):
        return f"Binomial(n={self.n}, p={self.p})"


class Poisson(DiscreteDistribution):
    """
    Models the probability of a given number of events occurring in a fixed interval.
    """
    def __init__(self, lam: float):
        if lam <= 0:
            raise ValueError("Rate parameter (lam) must be > 0.")
        self.lam = lam

    def pmf(self, k: Union[int, np.ndarray]) -> Union[float, np.ndarray]:
        def _pmf(x):
            if x < 0 or not float(x).is_integer():
                return 0.0
            return ((self.lam ** x) * math.exp(-self.lam)) / math.factorial(int(x))

        if isinstance(k, np.ndarray):
            return np.vectorize(_pmf)(k)
        return _pmf(k)

    def cdf(self, k: Union[int, np.ndarray]) -> Union[float, np.ndarray]:
        def _cdf(x):
            if x < 0: return 0.0
            return sum(self.pmf(i) for i in range(int(x) + 1))

        if isinstance(k, np.ndarray):
            return np.vectorize(_cdf)(k)
        return _cdf(k)

    def rvs(self, size=1):
        return np.random.poisson(self.lam, size)

    def mean(self): return self.lam
    def variance(self): return self.lam

    def __repr__(self):
        return f"Poisson(lam={self.lam})"


class Geometric(DiscreteDistribution):
    """
    Models the number of trials needed to get the first success (k >= 1).
    """
    def __init__(self, p: float):
        if not (0.0 < p <= 1.0):
            raise ValueError("Probability (p) must be between 0.0 (exclusive) and 1.0.")
        self.p = p

    def pmf(self, k: Union[int, np.ndarray]) -> Union[float, np.ndarray]:
        def _pmf(x):
            if x < 1 or not float(x).is_integer():
                return 0.0
            return ((1 - self.p) ** (x - 1)) * self.p

        if isinstance(k, np.ndarray):
            return np.vectorize(_pmf)(k)
        return _pmf(k)

    def cdf(self, k: Union[int, np.ndarray]) -> Union[float, np.ndarray]:
        def _cdf(x):
            if x < 1: return 0.0
            return 1 - ((1 - self.p) ** int(x))

        if isinstance(k, np.ndarray):
            return np.vectorize(_cdf)(k)
        return _cdf(k)

    def rvs(self, size=1):
        return np.random.geometric(self.p, size)

    def mean(self): return 1 / self.p
    def variance(self): return (1 - self.p) / (self.p ** 2)

    def __repr__(self):
        return f"Geometric(p={self.p})"


class NegativeBinomial(DiscreteDistribution):
    """
    Models the number of failures before the r-th success.
    """
    def __init__(self, r: int, p: float):
        if r <= 0:
            raise ValueError("Number of target successes (r) must be > 0.")
        if not (0.0 < p <= 1.0):
            raise ValueError("Probability (p) must be between 0.0 (exclusive) and 1.0.")
        self.r = r
        self.p = p

    def pmf(self, k: Union[int, np.ndarray]) -> Union[float, np.ndarray]:
        def _pmf(x):
            if x < 0 or not float(x).is_integer():
                return 0.0
            return math.comb(int(x) + self.r - 1, int(x)) * (self.p ** self.r) * ((1 - self.p) ** x)

        if isinstance(k, np.ndarray):
            return np.vectorize(_pmf)(k)
        return _pmf(k)

    def cdf(self, k: Union[int, np.ndarray]) -> Union[float, np.ndarray]:
        def _cdf(x):
            if x < 0: return 0.0
            return sum(self.pmf(i) for i in range(int(x) + 1))

        if isinstance(k, np.ndarray):
            return np.vectorize(_cdf)(k)
        return _cdf(k)

    def rvs(self, size=1):
        return np.random.negative_binomial(self.r, self.p, size)

    def mean(self): return (self.r * (1 - self.p)) / self.p
    def variance(self): return (self.r * (1 - self.p)) / (self.p ** 2)

    def __repr__(self):
        return f"NegativeBinomial(r={self.r}, p={self.p})"
