# src/stat/workflows/workflow.py

import src.stat.core as core
from typing import Any, Dict

import numpy as np
import pandas as pd

def standard_eda(data: Any) -> Dict[str, Any]:
    """
    Runs a standard exploratory data analysis (EDA) pipeline.
    Calculates summaries, correlations, and flags anomalous shapes.
    """
    st_data = core.represent(data)
    summary_data = st_data.summary()
    correlations = st_data.corr() if st_data.is_df else "N/A (1D Data)"
    warnings = {}
    if st_data.is_df:
        for column in summary_data.index:
            skew_val = summary_data.loc[column, 'skewness']
            if abs(skew_val) > 1.0:
                warnings[column] = f'Highly skewed ({skew_val:.2f})'
    else:
        skew_val = summary_data.get('skewness', 0)
        if abs(skew_val) > 1.0:
            warnings['1D_Array'] = f'Highly skewed ({skew_val:.2f})'

    return {
        'Data_Type': st_data.tag,
        'Dimensions': st_data.shape,
        'Correlations': correlations,
        'Summary': summary_data,
        'Automated_Warnings': warnings if warnings else "None"
    }

def remove_outliers(data: Any, series: str = None, multiplier: float = 1.5) -> Dict[str, Any]:
    """
    Scans the dataset for outliers using the IQR method and removes them.
    For DataFrames, it drops the entire row if an outlier is found in the target column(s).
    """
    st_data = core.represent(data)
    original_shape = st_data.shape

    if st_data.is_df:
        df = st_data.data.copy()
        # If no series is specified, check all numeric columns
        columns_to_check = [series] if series else df.select_dtypes(include=[np.number]).columns

        # Start with a mask where NO rows are outliers
        outlier_mask = pd.Series(False, index=df.index)

        for col in columns_to_check:
            # Calculate the Tukey Fences using your engine!
            q1 = st_data.percentile(25, series=col)
            q3 = st_data.percentile(75, series=col)
            iqr_val = q3 - q1

            lower_bound = q1 - (multiplier * iqr_val)
            upper_bound = q3 + (multiplier * iqr_val)

            # Find outliers in this specific column
            col_outliers = (df[col] < lower_bound) | (df[col] > upper_bound)
            # Combine it with our master mask
            outlier_mask = outlier_mask | col_outliers

        # Keep only the rows that are NOT outliers
        clean_df = df[~outlier_mask]
        clean_stat = core.represent(clean_df)

    else:  # It's a 1D Array
        arr = st_data.data
        q1 = st_data.percentile(25)
        q3 = st_data.percentile(75)
        iqr_val = q3 - q1

        lower_bound = q1 - (multiplier * iqr_val)
        upper_bound = q3 + (multiplier * iqr_val)

        # Filter the array
        clean_arr = arr[(arr >= lower_bound) & (arr <= upper_bound)]
        clean_stat = core.represent(clean_arr)

    # Calculate how many rows/items were dropped
    removed_count = original_shape[0] - clean_stat.shape[0]

    return {
        "Original_Shape": original_shape,
        "Cleaned_Shape": clean_stat.shape,
        "Outliers_Removed": removed_count,
        "Cleaned_Data": clean_stat  # We return a new Stat object!
    }