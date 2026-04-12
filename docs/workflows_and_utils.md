# Workflows and Specialized Tools

These tools automate common data science tasks and provide low-level mathematical building blocks.

## Automated Workflows

### `standard_eda(data)`
- **Purpose**: Runs a complete Exploratory Data Analysis (EDA) pipeline.
- **Output**: Returns a dictionary with:
    - `Data_Type`: Source origin (e.g., 'numpy', 'dataframe').
    - `Dimensions`: Shape of the data (rows, columns).
    - `Correlations`: Relationship matrix (for DataFrames).
    - `Summary`: Full descriptive statistics for all numeric columns.
    - `Automated_Warnings`: Flags columns with high skewness (absolute value > 1.0).
- **Niche**: Your "first step" after loading any new dataset.

### `remove_outliers(data, series=None, multiplier=1.5)`
- **Purpose**: Scans for outliers using the Tukey Fence (IQR) method and removes them.
- **Parameters**:
    - `series`: The specific column to check in a DataFrame. If `None`, all numeric columns are checked.
    - `multiplier`: The IQR multiplier (default 1.5).
- **Output**: Returns a dictionary containing the original and cleaned shapes, the count of removed items, and the new cleaned `Stat` object.
- **Niche**: Essential for cleaning datasets where extreme values might bias statistical results.

---

## `Prob` (Utility Class)

A collection of core combinatorics and probability theorems.

### `.combinations(n, r)` (alias `.ncr`)
- **Purpose**: Calculates the number of ways to choose `r` items from `n` items where order *does not* matter.
- **Example**: `Prob.combinations(5, 2)` returns `10`.

### `.permutations(n, r)` (alias `.npr`)
- **Purpose**: Calculates the number of ways to choose `r` items from `n` items where order *does* matter.
- **Example**: `Prob.permutations(5, 2)` returns `20`.

### `.bayes(p_a, p_b_given_a, p_b)`
- **Purpose**: Calculates $P(A|B) = [P(B|A) * P(A)] / P(B)$.
- **Example**: `Prob.bayes(0.01, 0.99, 0.05)` (Prob. of disease given a positive test).

### `.expected_value(values, probabilities)`
- **Purpose**: Calculates the long-term average ($E[X]$) of a discrete random variable.
- **Example**: `Prob.expected_value([1, 2, 3], [0.2, 0.5, 0.3])` returns `2.1`.

---

## Data Loading Utilities

### `from_grouped(frequency_dict)`
- **Purpose**: Converts grouped data (range midpoints and frequencies) into a standard `Stat` object.
- **Example**:
```python
# Represents 5 items between 10-20 and 2 items between 20-30
data = from_grouped({"10-20": 5, "20-30": 2})

# Internal calculation: (15.0 * 5) + (25.0 * 2) ...
data.show()
```
- **Niche**: Essential for analyzing summarized data from reports or research where raw data isn't available.
