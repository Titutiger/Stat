# src/stat/distributions/base.py

from abc import ABC, abstractmethod
import numpy as np
from typing import Union


class ContinuousDistribution(ABC):
    """Abstract base class for all continuous probability distributions."""

    @abstractmethod
    def pdf(self, x: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """Probability Density Function"""
        pass

    @abstractmethod
    def cdf(self, x: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """Cumulative Distribution Function"""
        pass

    @abstractmethod
    def ppf(self, q: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """Percent Point Function (Inverse CDF)"""
        pass

    @abstractmethod
    def rvs(self, size: Union[int, tuple] = 1) -> np.ndarray:
        """Random Variates Sample"""
        pass

    @abstractmethod
    def mean(self) -> float:
        pass

    @abstractmethod
    def variance(self) -> float:
        pass

    @abstractmethod
    def entropy(self) -> float:
        """Differential entropy of the distribution"""
        pass


class DiscreteDistribution(ABC):
    """Abstract base class for all discrete probability distributions."""

    @abstractmethod
    def pmf(self, k: Union[int, np.ndarray]) -> Union[float, np.ndarray]:
        """Probability Mass Function"""
        pass

    @abstractmethod
    def cdf(self, k: Union[int, np.ndarray]) -> Union[float, np.ndarray]:
        """Cumulative Distribution Function"""
        pass

    @abstractmethod
    def rvs(self, size: Union[int, tuple] = 1) -> np.ndarray:
        """Random Variates Sample"""
        pass

    @abstractmethod
    def mean(self) -> float:
        pass

    @abstractmethod
    def variance(self) -> float:
        pass