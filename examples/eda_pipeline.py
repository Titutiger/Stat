import pandas as pd
import numpy as np
import src.stat as stat

# ---------------------------------------------------------
# 1. Simulate Raw, Messy Data
# ---------------------------------------------------------
# Imagine we have sensor data with some extreme outliers (errors)
data = pd.DataFrame({
    'temperature': [20.1, 20.2, 19.9, 20.5, 100.0, 19.8, 20.3, -50.0, 20.1, 20.2],
    'pressure':    [101.3, 101.5, 101.2, 101.4, 500.0, 101.1, 101.6, 10.0, 101.3, 101.4],
    'status':      ['OK', 'OK', 'OK', 'OK', 'ERR', 'OK', 'OK', 'ERR', 'OK', 'OK']
})

print("--- Step 1: Automated EDA ---")
# Run the built-in EDA pipeline
eda_results = stat.standard_eda(data)

print(f"Data Origin: {eda_results['Data_Type']}")
print(f"Warnings: {eda_results['Automated_Warnings']}")
print("\nFull Summary Statistics:")
print(eda_results['Summary'])

# ---------------------------------------------------------
# 2. Automated Outlier Removal
# ---------------------------------------------------------
print("\n--- Step 2: Cleaning Data ---")
# The EDA flagged high skewness. Let's remove the outliers.
# This uses the Tukey Fence method (1.5 * IQR)
clean_results = stat.remove_outliers(data)

print(f"Original Rows: {clean_results['Original_Shape'][0]}")
print(f"Cleaned Rows:  {clean_results['Cleaned_Shape'][0]}")
print(f"Outliers Removed: {clean_results['Outliers_Removed']}")

# Get the new Stat object from the results
clean_stat = clean_results['Cleaned_Data']

print("\n--- Step 3: Post-Cleaning Analysis ---")
# Now look at the mean again - it should be much more sensible
print(f"Original Temp Mean: {stat.represent(data).mean(series='temperature'):.2f}")
print(f"Cleaned Temp Mean:  {clean_stat.mean(series='temperature'):.2f}")

# Check correlations on the clean data
print("\nCleaned Correlation Matrix:")
print(clean_stat.corr())
