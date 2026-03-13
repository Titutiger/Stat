import pytest
import numpy as np
import pandas as pd
import src.stat as stat

def test_z_test():
    # One-sample Z-test
    # Data with mean 10, std 2. Test against popmean 9.
    data = [8, 9, 10, 11, 12] # mean 10, sample std 1.58
    s = stat.represent(data)
    res = s.z_test(popmean=9, popstd=1.58)
    
    assert res['method'] == "One-sample Z-test"
    assert res['statistic'] > 0
    assert 'p_value' in res

def test_t_test_one_sample():
    data = [10, 12, 9, 11, 10] # mean 10.4
    s = stat.represent(data)
    res = s.t_test(popmean=10)
    
    assert res['method'] == "One-sample T-test"
    assert res['df'] == 4
    assert 'statistic' in res
    assert 'p_value' in res

def test_t_test_two_sample():
    group1 = [10, 12, 9, 11, 10]
    group2 = [14, 15, 13, 16, 14]
    s1 = stat.represent(group1)
    s2 = stat.represent(group2)
    
    res = s1.t_test(other=s2)
    assert res['method'] == "Independent Two-sample T-test"
    assert res['df'] == 8
    assert res['p_value'] < 0.05

def test_t_test_paired():
    before = [10, 12, 9, 11, 10]
    after = [12, 14, 11, 13, 12]
    s_before = stat.represent(before)
    s_after = stat.represent(after)
    
    res = s_before.t_test(other=s_after, paired=True)
    assert res['method'] == "Paired T-test"
    assert res['df'] == 4
    assert res['p_value'] < 0.05

def test_anova():
    g1 = [10, 12, 11]
    g2 = [20, 22, 21]
    g3 = [30, 32, 31]
    s1 = stat.represent(g1)
    
    res = s1.anova(g2, g3)
    assert res['method'] == "One-way ANOVA"
    assert res['p_value'] < 0.01

def test_chisquare_gof():
    # Observed frequencies: 20, 30
    # Expected: 25, 25
    data = [0]*20 + [1]*30
    s = stat.represent(data)
    res = s.chisquare(expected=[25, 25])
    
    assert res['method'] == "Chi-Square Goodness of Fit"
    assert res['statistic'] == pytest.approx(2.0) # (20-25)^2/25 + (30-25)^2/25 = 25/25 + 25/25 = 2

def test_dataframe_integration():
    df = pd.DataFrame({
        'A': [10, 12, 11, 13, 12],
        'B': [15, 17, 16, 18, 17]
    })
    s = stat.represent(df)
    
    # T-test on column A
    res_a = s.t_test(popmean=10, series='A')
    assert res_a['statistic'] > 0
    
    # Two-sample T-test between A and B
    res_ab = s.t_test(other=s, series='A', other_series='B')
    assert res_ab['method'] == "Independent Two-sample T-test"
    assert res_ab['p_value'] < 0.05
