# src/stat/api.py

# core
from .core.represent import Stat, represent
from .distributions import poisson

# workflows
from .workflows.workflows import standard_eda, remove_outliers

# prob
from .prob import Prob

# continuous dist
from .distributions.continuous import (
    Normal, Exponential, Gamma, Beta, TDistribution, ChiSquare
)

# discrete
from .distributions.binomial import Binomial
from .distributions.poisson import Poisson
from .distributions.geometric import Geometric
from .distributions.negative_binomial import NegativeBinomial

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
    'Poisson',
    'NegativeBinomial',
    'Geometric',
    'Prob',
    # utils
    'from_grouped'
]