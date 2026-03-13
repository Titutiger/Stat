# src/stat/inferential.py

import numpy as np
import scipy.stats as st
from typing import Union, Dict, Any, List


class InferentialMixin:
    """
    Contains hypothesis testing operations.
    Assumes the parent class has `self.data`, `self.is_df`, and `self._apply()`.
    """

    def t_test(self, popmean: float = 0, other: Any = None, paired: bool = False, 
               series: str = None, other_series: str = None, skipna: bool = True) -> Dict[str, Any]:
        """
        Performs one-sample, two-sample, or paired t-tests.
        """
        def _get_data(obj, col=None):
            if hasattr(obj, 'is_df') and obj.is_df:
                if col is None:
                    raise ValueError("Column name (series) must be specified for DataFrame.")
                col_map = {str(c).lower(): c for c in obj.data.columns}
                if col.lower() not in col_map:
                    raise ValueError(f"Column '{col}' not found.")
                data = obj.data[col_map[col.lower()]].values
            elif hasattr(obj, 'data'):
                data = obj.data
            else:
                data = np.asarray(obj)
            
            if skipna:
                data = data[~np.isnan(data)]
            return data

        # One-sample T-test
        if other is None:
            data = self._get_target_data(series, skipna)
            res = st.ttest_1samp(data, popmean)
            return {
                "statistic": float(res.statistic),
                "p_value": float(res.pvalue),
                "df": len(data) - 1,
                "method": "One-sample T-test"
            }

        # Two-sample or Paired T-test
        data1 = self._get_target_data(series, skipna)
        data2 = _get_data(other, other_series)

        if paired:
            if len(data1) != len(data2):
                raise ValueError("Paired t-test requires samples of equal length.")
            res = st.ttest_rel(data1, data2)
            method = "Paired T-test"
        else:
            res = st.ttest_ind(data1, data2)
            method = "Independent Two-sample T-test"

        return {
            "statistic": float(res.statistic),
            "p_value": float(res.pvalue),
            "df": len(data1) + len(data2) - 2 if not paired else len(data1) - 1,
            "method": method
        }

    def z_test(self, popmean: float = 0, popstd: float = None, series: str = None, skipna: bool = True) -> Dict[str, Any]:
        """
        Performs a one-sample Z-test.
        If popstd is not provided, sample standard deviation is used (Large Sample T-test approximation).
        """
        data = self._get_target_data(series, skipna)
        n = len(data)
        sample_mean = np.mean(data)
        
        sigma = popstd if popstd is not None else np.std(data, ddof=1)
        
        z_stat = (sample_mean - popmean) / (sigma / np.sqrt(n))
        p_val = 2 * (1 - st.norm.cdf(abs(z_stat)))
        
        return {
            "statistic": float(z_stat),
            "p_value": float(p_val),
            "method": "One-sample Z-test"
        }

    def anova(self, *others: Any, series: str = None, other_series: List[str] = None, skipna: bool = True) -> Dict[str, Any]:
        """
        Performs a one-way ANOVA across multiple groups.
        """
        groups = [self._get_target_data(series, skipna)]
        
        if other_series and len(other_series) != len(others):
            raise ValueError("Number of other_series must match number of other groups.")

        for i, other in enumerate(others):
            col = other_series[i] if other_series else None
            groups.append(self._extract_data(other, col, skipna))

        res = st.f_oneway(*groups)
        return {
            "statistic": float(res.statistic),
            "p_value": float(res.pvalue),
            "method": "One-way ANOVA"
        }

    def chisquare(self, expected: List[float] = None, series: str = None, skipna: bool = True) -> Dict[str, Any]:
        """
        Performs Chi-Square Goodness of Fit test.
        """
        data = self._get_target_data(series, skipna)
        # Assuming data contains observed frequencies or raw data to be counted
        observed, counts = np.unique(data, return_counts=True)
        
        res = st.chisquare(counts, f_exp=expected)
        return {
            "statistic": float(res.statistic),
            "p_value": float(res.pvalue),
            "df": len(counts) - 1,
            "method": "Chi-Square Goodness of Fit"
        }

    # Helper methods for internal data extraction
    def _get_target_data(self, series: str = None, skipna: bool = True) -> np.ndarray:
        if self.is_df:
            if series is None:
                raise ValueError("Series name must be provided for DataFrame.")
            col_map = {str(c).lower(): c for c in self.data.columns}
            if series.lower() not in col_map:
                raise ValueError(f"Column '{series}' not found.")
            data = self.data[col_map[series.lower()]].values
        else:
            data = self.data
        
        if skipna:
            data = data[~np.isnan(data)]
        return data

    def _extract_data(self, obj: Any, series: str = None, skipna: bool = True) -> np.ndarray:
        if hasattr(obj, 'is_df') and obj.is_df:
            if series is None:
                raise ValueError("Series name must be provided for DataFrame objects.")
            col_map = {str(c).lower(): c for c in obj.data.columns}
            if series.lower() not in col_map:
                raise ValueError(f"Column '{series}' not found.")
            data = obj.data[col_map[series.lower()]].values
        elif hasattr(obj, 'data'):
            data = obj.data
        else:
            data = np.asarray(obj)
            
        if skipna:
            data = data[~np.isnan(data)]
        return data
