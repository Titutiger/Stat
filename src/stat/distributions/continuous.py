# src/stat/distributions/continuous.py

import numpy as np
import scipy.special as sp
from typing import Union
from .base import ContinuousDistribution

class Normal(ContinuousDistribution):
    def __init__(self, mu: float = 0.0, sigma: float = 1.0):
        if sigma <= 0: raise ValueError("Sigma must be > 0.")
        self.mu = mu
        self.sigma = sigma

    def pdf(self, x):
        return (1 / (self.sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - self.mu) / self.sigma)**2)
    def cdf(self, x):
        return 0.5 * (1 + sp.erf((x - self.mu) / (self.sigma * np.sqrt(2))))
    def ppf(self, q):
        return self.mu + self.sigma * np.sqrt(2) * sp.erfinv(2 * np.asarray(q) - 1)
    def rvs(self, size=1):
        return np.random.normal(self.mu, self.sigma, size)
    def mean(self): return self.mu
    def variance(self): return self.sigma**2
    def entropy(self): return 0.5 * np.log(2 * np.pi * np.e * self.sigma**2)

    def __repr__(self):
        return f"Normal(mu={self.mu}, sigma={self.sigma})"

class Exponential(ContinuousDistribution):
    def __init__(self, lam: float = 1.0):
        if lam <= 0: raise ValueError("Lambda must be > 0.")
        self.lam = lam

    def pdf(self, x):
        x = np.asarray(x)
        return np.where(x >= 0, self.lam * np.exp(-self.lam * x), 0.0)
    def cdf(self, x):
        x = np.asarray(x)
        return np.where(x >= 0, 1 - np.exp(-self.lam * x), 0.0)
    def ppf(self, q):
        return -np.log(1 - np.asarray(q)) / self.lam
    def rvs(self, size=1):
        return np.random.exponential(1 / self.lam, size)
    def mean(self): return 1 / self.lam
    def variance(self): return 1 / (self.lam**2)
    def entropy(self): return 1 - np.log(self.lam)

    def __repr__(self):
        return f"Exponential(lam={self.lam})"

class Gamma(ContinuousDistribution):
    def __init__(self, alpha: float, beta: float):
        if alpha <= 0 or beta <= 0: raise ValueError("Alpha and Beta must be > 0.")
        self.alpha = alpha
        self.beta = beta

    def pdf(self, x):
        x = np.asarray(x)
        return np.where(x > 0, (self.beta**self.alpha * x**(self.alpha - 1) * np.exp(-self.beta * x)) / sp.gamma(self.alpha), 0.0)
    def cdf(self, x):
        # sp.gammainc is the regularized lower incomplete gamma function
        x = np.asarray(x)
        return np.where(x > 0, sp.gammainc(self.alpha, self.beta * x), 0.0)
    def ppf(self, q):
        return sp.gammaincinv(self.alpha, np.asarray(q)) / self.beta
    def rvs(self, size=1):
        return np.random.gamma(self.alpha, 1 / self.beta, size)
    def mean(self): return self.alpha / self.beta
    def variance(self): return self.alpha / (self.beta**2)
    def entropy(self):
        return self.alpha - np.log(self.beta) + sp.gammaln(self.alpha) + (1 - self.alpha) * sp.digamma(self.alpha)

    def __repr__(self):
        return f"Gamma(alpha={self.alpha}, beta={self.beta})"

class Beta(ContinuousDistribution):
    def __init__(self, a: float, b: float):
        if a <= 0 or b <= 0: raise ValueError("Alpha (a) and Beta (b) must be > 0.")
        self.a = a
        self.b = b

    def pdf(self, x):
        x = np.asarray(x)
        return np.where((x >= 0) & (x <= 1), (x**(self.a - 1) * (1 - x)**(self.b - 1)) / sp.beta(self.a, self.b), 0.0)
    def cdf(self, x):
        x = np.asarray(x)
        return np.where(x >= 0, np.where(x <= 1, sp.betainc(self.a, self.b, x), 1.0), 0.0)
    def ppf(self, q):
        return sp.betaincinv(self.a, self.b, np.asarray(q))
    def rvs(self, size=1):
        return np.random.beta(self.a, self.b, size)
    def mean(self): return self.a / (self.a + self.b)
    def variance(self): return (self.a * self.b) / (((self.a + self.b)**2) * (self.a + self.b + 1))
    def entropy(self):
        return np.log(sp.beta(self.a, self.b)) - (self.a - 1)*sp.digamma(self.a) - (self.b - 1)*sp.digamma(self.b) + (self.a + self.b - 2)*sp.digamma(self.a + self.b)

    def __repr__(self):
        return f"Beta(a={self.a}, b={self.b})"

class TDistribution(ContinuousDistribution):
    def __init__(self, df: float):
        if df <= 0: raise ValueError("Degrees of freedom (df) must be > 0.")
        self.df = df

    def pdf(self, x):
        return (sp.gamma((self.df + 1) / 2) / (np.sqrt(self.df * np.pi) * sp.gamma(self.df / 2))) * (1 + (x**2) / self.df)**(- (self.df + 1) / 2)
    def cdf(self, x):
        return sp.stdtr(self.df, np.asarray(x))
    def ppf(self, q):
        return sp.stdtrit(self.df, np.asarray(q))
    def rvs(self, size=1):
        return np.random.standard_t(self.df, size)
    def mean(self): return 0.0 if self.df > 1 else float('nan')
    def variance(self):
        if self.df > 2: return self.df / (self.df - 2)
        if self.df > 1: return float('inf')
        return float('nan')
    def entropy(self):
        half_df = self.df / 2
        return ((self.df + 1) / 2) * (sp.digamma((self.df + 1) / 2) - sp.digamma(half_df)) + np.log(np.sqrt(self.df) * sp.beta(half_df, 0.5))

    def __repr__(self):
        return f"TDistribution(df={self.df})"

class ChiSquare(Gamma):
    """
    Chi-Square is mathematically a special case of the Gamma distribution
    where alpha = df/2 and beta = 1/2. We can just inherit from Gamma!
    """
    def __init__(self, df: float):
        if df <= 0: raise ValueError("Degrees of freedom (df) must be > 0.")
        self.df = df
        super().__init__(alpha=df / 2, beta=0.5)

    def rvs(self, size=1):
        return np.random.chisquare(self.df, size)
    def __repr__(self):
        return f"ChiSquare(df={self.df})"