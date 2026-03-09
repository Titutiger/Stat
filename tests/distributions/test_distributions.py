import pytest
import numpy as np
import src.stat as stat
from src.stat.distributions.base import DiscreteDistribution, ContinuousDistribution

# ==========================================
# DISCRETE DISTRIBUTIONS
# ==========================================

def test_binomial():
    coin = stat.Binomial(n=10, p=0.5)
    # P(X=5) for n=10, p=0.5
    assert coin.pmf(5) == pytest.approx(0.24609375)
    assert coin.mean() == 5.0
    assert coin.variance() == 2.5
    assert len(coin.rvs(10)) == 10
    assert isinstance(coin, DiscreteDistribution)

def test_poisson():
    server = stat.Poisson(lam=2)
    # P(X=4) for lam=2
    assert server.pmf(4) == pytest.approx(0.0902235)
    assert server.mean() == 2.0
    assert server.variance() == 2.0
    assert isinstance(server, DiscreteDistribution)

def test_geometric():
    geo = stat.Geometric(p=0.5)
    # P(X=1) = p = 0.5
    assert geo.pmf(1) == 0.5
    # P(X=2) = (1-p)*p = 0.25
    assert geo.pmf(2) == 0.25
    assert geo.mean() == 2.0
    assert geo.variance() == 2.0
    assert isinstance(geo, DiscreteDistribution)

def test_negative_binomial():
    nb = stat.NegativeBinomial(r=5, p=0.5)
    # Mean = r(1-p)/p = 5(0.5)/0.5 = 5
    assert nb.mean() == 5.0
    assert nb.variance() == 10.0
    assert isinstance(nb, DiscreteDistribution)

# ==========================================
# CONTINUOUS DISTRIBUTIONS
# ==========================================

def test_normal():
    norm = stat.Normal(mu=100, sigma=15)
    # 95th percentile is approx 1.645 standard deviations from mean
    assert norm.ppf(0.95) == pytest.approx(124.67, rel=1e-3)
    assert norm.mean() == 100.0
    assert norm.variance() == 225.0
    assert isinstance(norm, ContinuousDistribution)

def test_gamma():
    g = stat.Gamma(alpha=2, beta=1)
    assert g.mean() == 2.0
    assert g.variance() == 2.0
    assert len(g.rvs(5)) == 5
    assert isinstance(g, ContinuousDistribution)

def test_chisquare():
    chi = stat.ChiSquare(df=4)
    # Chi-Square(df) has mean df and variance 2df
    assert chi.mean() == 4.0
    assert chi.variance() == 8.0
    # Test vectorized CDF
    cdf_vals = chi.cdf(np.array([1, 2, 3]))
    assert len(cdf_vals) == 3
    assert isinstance(chi, ContinuousDistribution)
