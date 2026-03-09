# src/stat/api.py

# core
from .core.represent import Stat, represent

# workflows
from .workflows.workflows import standard_eda, remove_outliers

# prob
from .prob import Prob

# distributions
from .distributions import (
    Normal, Exponential, Gamma, Beta, TDistribution, ChiSquare,
    Binomial, Poisson, Geometric, NegativeBinomial
)

# utils
from .utils import from_grouped

# ======================================================================================================================

__all__ = [
    # core
    'Stat', 'represent',
    # workflow
    'standard_eda',
    'remove_outliers',
    # models
    'Normal',
    'Exponential',
    'Gamma',
    'Beta',
    'TDistribution',
    'ChiSquare',
    'Binomial',
    'Poisson',
    'NegativeBinomial',
    'Geometric',
    'Prob',
    # utils
    'from_grouped'
]
