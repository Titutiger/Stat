# Workflows and Specialized Tools

These tools automate common data science tasks and provide low-level mathematical building blocks.

## Automated Workflows

### `standard_eda(data)`
- **Purpose**: Runs a complete Exploratory Data Analysis (EDA) pipeline.
- **Output**: Returns a dictionary with:
    - `Data_Type`: Source origin.
    - `Dimensions`: Shape of the data.
    - `Correlations`: Relationship matrix.
    - `Summary`: Full descriptive statistics.
    - `Automated_Warnings`: Flags columns with high skewness.
- **Niche**: Your "first step" after loading any new dataset.

### `remove_outliers(data, multiplier=1.5)`
- **Purpose**: Scans for outliers using the Tukey Fence (IQR) method and removes them.
- **Niche**: Essential for data cleaning to ensure extreme values don't bias your models.

---

## `Prob` (Utility Class)

A collection of core combinatorics and probability theorems.

### `.combinations(n, r)` (alias `.ncr`)
- **Niche**: Choosing items without replacement where order *does not* matter.

### `.permutations(n, r)` (alias `.npr`)
- **Niche**: Choosing items without replacement where order *does* matter.

### `.bayes(p_a, p_b_given_a, p_b)`
- **Niche**: Calculating "conditional probability" (e.g., probability of a disease given a positive test result).

### `.expected_value(values, probabilities)`
- **Niche**: Finding the long-term average of a discrete random variable.

---

## Data Loading Utilities

### `from_grouped(frequency_dict)`
- **Purpose**: Converts grouped data (e.g., `{"10-20": 5}`) into a standard `Stat` object by using range midpoints.
- **Niche**: Essential for analyzing summarized data from reports or older research where raw data isn't available.
