# src/stat/distributions/normal.py
import math
import numpy as np


class Normal:
    """
    A standalone Normal (Gaussian) Distribution object.
    """

    def __init__(self, mu: float = 0.0, sigma: float = 1.0):
        if sigma <= 0:
            raise ValueError("Standard deviation (sigma) must be > 0.")
        self.mu = mu
        self.sigma = sigma

    def pdf(self, x: float | np.ndarray) -> float | np.ndarray:
        """Calculates the Probability Density Function."""
        coefficient = 1.0 / (self.sigma * math.sqrt(2 * math.pi))
        exponent = np.exp(-0.5 * ((x - self.mu) / self.sigma) ** 2)
        return coefficient * exponent

    def cdf(self, x: float) -> float:
        """Calculates the Cumulative Distribution Function."""
        return 0.5 * (1 + math.erf((x - self.mu) / (self.sigma * math.sqrt(2))))

    def __repr__(self):
        return f"Normal(mu={self.mu}, sigma={self.sigma})"