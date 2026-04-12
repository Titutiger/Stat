# Descriptive Statistics

These methods are available on any `Stat` object and are used to summarize and describe the features of a dataset.

## Central Tendency

### `.mean(method="arithmetic", series=None, skipna=True)`
- **`method`**: `"arithmetic"`, `"geometric"`, or `"harmonic"`.
- **Niche**: Use `harmonic` for rates (like speed or price-to-earnings) and `geometric` for compound growth or returns.
- **Usage**: `data.mean(method="harmonic")`

### `.median(series=None, skipna=True)`
- **Niche**: Best for skewed data (like salaries) where the mean is misleading.
- **Usage**: `data.median()`

### `.mode(series=None, skipna=True)`
- **Niche**: Identifies the most common value. Returns the first mode if the data is multimodal.
- **Usage**: `data.mode()`

---

## Dispersion (Spread)

### `.variance(sample=False, series=None, skipna=True)`
- **`sample`**: Set to `True` for sample variance (Bessel's correction, $n-1$).
- **Usage**: `data.variance(sample=True)`

### `.std(sample=False, series=None, skipna=True)`
- **Niche**: Standard deviation is the square root of variance, providing spread in the same units as the data.
- **Usage**: `data.std()`

### `.sem(series=None, skipna=True)`
- **Niche**: Standard Error of the Mean. Measures how far the sample mean is likely to be from the population mean.
- **Usage**: `data.sem()`

### `.mad(series=None, skipna=True)`
- **Niche**: Mean Absolute Deviation. More robust to outliers than standard deviation.
- **Usage**: `data.mad()`

### `.iqr(series=None, skipna=True)`
- **Niche**: Interquartile Range ($Q_3 - Q_1$). Ideal for identifying the "middle 50%" and outlier detection.
- **Usage**: `data.iqr()`

### `.min(series=None, skipna=True)`
- **Niche**: The smallest value in the dataset.
- **Usage**: `data.min()`

### `.max(series=None, skipna=True)`
- **Niche**: The largest value in the dataset.
- **Usage**: `data.max()`

### `.range(series=None, skipna=True)`
- **Niche**: The difference between the maximum and minimum values.
- **Usage**: `data.range()`

---

## Quantiles and Percentiles

### `.percentile(q, series=None, skipna=True)`
- **`q`**: The percentile rank to find (between 0 and 100).
- **Usage**: `data.percentile(95)` (95th percentile)

### `.quantile(q, series=None, skipna=True)`
- **`q`**: The quantile rank to find (between 0.0 and 1.0).
- **Usage**: `data.quantile(0.75)` (equivalent to the 75th percentile)

---

## Shape and Distribution

### `.skewness(series=None, skipna=True, sample=True)`
- **`sample`**: Set to `True` (default) for sample skewness (Fisher-Pearson coefficient).
- **Niche**: Measures asymmetry. Positive = right tail, Negative = left tail.
- **Usage**: `data.skewness()`

### `.kurtosis(series=None, skipna=True, sample=True)`
- **`sample`**: Set to `True` (default) for sample excess kurtosis.
- **Niche**: Measures "tailedness." High kurtosis means more outliers than a normal distribution.
- **Usage**: `data.kurtosis()`

---

## Relationships and Structure

### `.corr(method="pearson")`
- **`method`**: `"pearson"`, `"spearman"`, or `"kendall"`.
- **Niche**: Use `spearman` for non-linear but monotonic relationships.
- **Usage**: `df_stat.corr(method="spearman")`

### `.groupby(by, operation="mean")`
- **Niche**: Essential for categorical analysis (e.g., "Find the mean battery life FOR EACH machine model").
- **Usage**: `data.groupby(by="MachineType", operation="median")`

### `.summary()`
- **Niche**: A "one-stop shop" that returns all key statistics as a dictionary (1D) or DataFrame (structured).
- **Usage**: `data.summary()`
