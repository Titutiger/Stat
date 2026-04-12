# Inferential Statistics

Inferential statistics allow you to make predictions or inferences about a population based on a sample of data. These methods are available on any `Stat` object.

## Hypothesis Testing

All hypothesis tests return a dictionary containing the test statistic, the p-value, and other relevant metadata.

#### `.t_test(popmean=0, other=None, paired=False, series=None, other_series=None, skipna=True)`
Performs one-sample, two-sample, or paired t-tests.

- **`popmean`**: The expected population mean (for one-sample tests).
- **`other`**: Another `Stat` object or array-like for two-sample tests.
- **`paired`**: Set to `True` for a paired t-test (requires samples of equal length).
- **`series`**: The column name to use if the object is a DataFrame.
- **`other_series`**: The column name to use from the `other` object if it is a DataFrame.
- **`skipna`**: If `True`, removes `NaN` values before calculation.

**Usage:**
```python
# One-sample T-test
data.t_test(popmean=100)

# Independent Two-sample T-test
group1.t_test(other=group2)

# Paired T-test
before.t_test(other=after, paired=True)
```

---

### `.z_test(popmean=0, popstd=None, series=None, skipna=True)`
Performs a one-sample Z-test. If the population standard deviation (`popstd`) is not provided, the sample standard deviation is used as an approximation (valid for large samples).

- **`popmean`**: The expected population mean.
- **`popstd`**: The known population standard deviation.
- **`series`**: The column name to use if the object is a DataFrame.

**Usage:**
```python
data.z_test(popmean=50, popstd=5)
```

---

### `.anova(*others, series=None, other_series=None, skipna=True)`
Performs a one-way Analysis of Variance (ANOVA) to compare the means of three or more groups.

- **`*others`**: One or more `Stat` objects or array-likes to compare against.
- **`series`**: The column name to use from the calling object.
- **`other_series`**: A list of column names for each corresponding object in `others`.

**Usage:**
```python
group1.anova(group2, group3)
```

---

### `.chisquare(expected=None, series=None, skipna=True)`
Performs a Chi-Square Goodness of Fit test.

- **`expected`**: A list of expected frequencies. If `None`, it assumes a uniform distribution.
- **`series`**: The column name to use if the object is a DataFrame.

**Usage:**
```python
# Test if a die is fair (observed frequencies in 'data')
data.chisquare(expected=[10, 10, 10, 10, 10, 10])
```
