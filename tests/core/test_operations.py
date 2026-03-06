import pytest
import numpy as np
import pandas as pd
import math
from src.stat.core import represent

# ==========================================
# FIXTURES (Shared Test Data)
# ==========================================

@pytest.fixture
def arr_1d():
    return represent([2, 4, 4, 4, 5, 5, 7, 9])

@pytest.fixture
def arr_nan():
    return represent([2, 4, np.nan, 8])

@pytest.fixture
def df_data():
    df = pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': [2, 4, 6, 8, 10], # Perfect positive correlation with A
        'C': [10, 8, 6, 4, 2]  # Perfect negative correlation with A
    })
    return represent(df)

# ==========================================
# TESTS FOR DESCRIPTIVE MIXIN
# ==========================================

def test_mean(arr_1d, arr_nan, df_data):
    # Standard arithmetic mean
    assert arr_1d.mean() == pytest.approx(5.0)
    # Geometric mean
    assert arr_1d.mean(method='geometric') == pytest.approx(4.502, rel=1e-3)
    # Harmonic mean
    assert arr_1d.mean(method='harmonic') == pytest.approx(4.041, rel=1e-3)
    # Skip NA handling
    assert arr_nan.mean(skipna=True) == pytest.approx(4.666, rel=1e-3)
    # DataFrame column targeting
    assert df_data.mean(series='B') == pytest.approx(6.0)

def test_median(arr_1d, arr_nan, df_data):
    # Even length array
    assert arr_1d.median() == 4.5
    # Odd length array
    arr_odd = represent([1, 3, 5])
    assert arr_odd.median() == 3.0
    # Skip NA handling
    assert arr_nan.median() == 4.0
    # DataFrame column targeting
    assert df_data.median(series='C') == 6.0
    # All NaNs returns NaN
    all_nans = represent([np.nan, np.nan])
    assert math.isnan(all_nans.median())

def test_mode(arr_1d, arr_nan, df_data):
    # Standard mode
    assert arr_1d.mode() == 4.0
    # Multimodal (returns first mode)
    multi = represent([1, 1, 2, 2, 3])
    assert multi.mode() == 1.0
    # Skip NA handling
    assert arr_nan.mode() == 2.0  # 2, 4, 8 all appear once, returns first
    # DataFrame column targeting
    assert df_data.mode(series='A') == 1.0
    # Empty array after dropping NaNs
    all_nans = represent([np.nan])
    assert math.isnan(all_nans.mode())

def test_variance(arr_1d, arr_nan, df_data):
    # Population variance (default)
    assert arr_1d.variance() == pytest.approx(4.5)
    # Sample variance
    assert arr_1d.variance(sample=True) == pytest.approx(5.142, rel=1e-3)
    # Zero variance
    flat = represent([5, 5, 5])
    assert flat.variance() == 0.0
    # Skip NA handling
    assert arr_nan.variance() == pytest.approx(6.222, rel=1e-3)
    # DataFrame column targeting
    assert df_data.variance(series='B') == pytest.approx(8.0)

def test_std(arr_1d, arr_nan, df_data):
    # Population std
    assert arr_1d.std() == pytest.approx(2.121, rel=1e-3)
    # Sample std
    assert arr_1d.std(sample=True) == pytest.approx(2.267, rel=1e-3)
    # Zero std
    flat = represent([5, 5, 5])
    assert flat.std() == 0.0
    # Skip NA handling
    assert arr_nan.std() == pytest.approx(2.494, rel=1e-3)
    # DataFrame column targeting
    assert df_data.std(series='B') == pytest.approx(2.828, rel=1e-3)

def test_mad(arr_1d, arr_nan, df_data):
    # Standard MAD
    assert arr_1d.mad() == pytest.approx(1.5)
    # Zero MAD
    flat = represent([5, 5, 5])
    assert flat.mad() == 0.0
    # Skip NA handling
    assert arr_nan.mad() == pytest.approx(2.0)
    # DataFrame column targeting
    assert df_data.mad(series='A') == pytest.approx(1.2)
    # Edge case (single value)
    single = represent([10])
    assert single.mad() == 0.0

def test_percentile(arr_1d, arr_nan, df_data):
    # 0th percentile (min)
    assert arr_1d.percentile(0) == 2.0
    # 50th percentile (median)
    assert arr_1d.percentile(50) == 4.5
    # 100th percentile (max)
    assert arr_1d.percentile(100) == 9.0
    # Out of bounds raises ValueError
    with pytest.raises(ValueError):
        arr_1d.percentile(-5)
    # DataFrame column targeting
    assert df_data.percentile(25, series='C') == 4.0

def test_quantile(arr_1d, arr_nan, df_data):
    # 0.0 quantile
    assert arr_1d.quantile(0.0) == 2.0
    # 0.5 quantile
    assert arr_1d.quantile(0.5) == 4.5
    # 1.0 quantile
    assert arr_1d.quantile(1.0) == 9.0
    # Out of bounds raises ValueError
    with pytest.raises(ValueError):
        arr_1d.quantile(1.5)
    # Skip NA handling
    assert arr_nan.quantile(0.5) == 4.0

def test_iqr(arr_1d, arr_nan, df_data):
    # Standard IQR
    assert arr_1d.iqr() == pytest.approx(1.5)
    # Zero IQR
    flat = represent([5, 5, 5, 5])
    assert flat.iqr() == 0.0
    # Skip NA handling
    assert arr_nan.iqr() == pytest.approx(3.0)
    # DataFrame column targeting
    assert df_data.iqr(series='A') == pytest.approx(2.0)
    # Narrow distribution
    narrow = represent([1, 2, 2, 2, 3])
    assert narrow.iqr() == pytest.approx(0.0)

def test_min_max_range(arr_1d, arr_nan, df_data):
    # Note: Grouped to save space, testing 5 attributes across min/max/range
    # Standard min
    assert arr_1d.min() == 2.0
    # Standard max
    assert arr_1d.max() == 9.0
    # Standard range
    assert arr_1d.range() == 7.0
    # Skip NA for range
    assert arr_nan.range() == 6.0
    # DataFrame column targeting
    assert df_data.range(series='C') == 8.0

def test_sem(arr_1d, arr_nan, df_data):
    # Standard SEM
    assert arr_1d.sem() == pytest.approx(0.801, rel=1e-3)
    # Skip NA handling
    assert arr_nan.sem() == pytest.approx(2.027, rel=1e-3)
    # DataFrame column targeting
    assert df_data.sem(series='A') == pytest.approx(0.707, rel=1e-3)
    # Too few elements for SEM (returns nan)
    single = represent([5])
    assert math.isnan(single.sem())
    # Zero variance = Zero SEM
    flat = represent([5, 5, 5])
    assert flat.sem() == 0.0

def test_corr(arr_1d, df_data):
    # 1D array always returns 1.0
    assert arr_1d.corr() == 1.0
    # Perfect positive correlation (A vs B)
    corr_matrix = df_data.corr()
    assert corr_matrix.loc['A', 'B'] == pytest.approx(1.0)
    # Perfect negative correlation (A vs C)
    assert corr_matrix.loc['A', 'C'] == pytest.approx(-1.0)
    # Uses Spearman method correctly
    spearman = df_data.corr(method='spearman')
    assert spearman.loc['A', 'B'] == pytest.approx(1.0)
    # Matrix symmetry (A vs B == B vs A)
    assert corr_matrix.loc['A', 'B'] == corr_matrix.loc['B', 'A']

def test_summary(arr_1d, df_data):
    # 1D array returns dict
    summ_1d = arr_1d.summary()
    assert isinstance(summ_1d, dict)
    # Dict contains expected keys
    assert 'mean' in summ_1d and 'sem' in summ_1d
    # Values are calculated correctly inside summary
    assert summ_1d['mean'] == pytest.approx(5.0)
    # DataFrame returns a pandas DataFrame
    summ_df = df_data.summary()
    assert isinstance(summ_df, pd.DataFrame)
    # DataFrame targets column correctly if specified
    summ_col = df_data.summary(series='A')
    assert summ_col['mean'] == 3.0