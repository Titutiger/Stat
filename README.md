![Status](https://img.shields.io/badge/status-alpha-orange)

```commandline


██▄       ▄██████  ████████   ▄████▄   ████████ 
████▄    ███▒▒▒▒▒  ▒▒███▒▒▒  ███▒▒███  ▒▒███▒▒▒ 
██████▄  ███████▄    ███    ███    ███   ███    
██████▀  ▒▒▒▒▒███    ███    ██████████   ███    
████▀    ▀██████▀    ███    ███▒▒▒▒███   ███    
██▀       ▒▒▒▒▒▒     ▒▒▒    ▒▒▒    ▒▒▒   ▒▒▒    


┌────────────────────────────────────────────────────────────────────────┐
│ A symbolic and numerical statistical engine.                           │
│ A statistics and probability library built for python.                 │
└────────────────────────────────────────────────────────────────────────┘

                                                           ~ Titutiger
``` 


###### *A statistics and probability library built for Python.* ~ *Titutiger*

---

## 📌 Project Details

* **Version:** v0.1.2-alpha
* **Python:** 3.12+
* **Core Dependencies:** `numpy`, `pandas`, `scipy`
* **Testing Framework:** `pytest`

---

## 💡 The Vision

`Stat` is designed to be a hybrid statistical modeling engine. 
It bridges the gap between descriptive, observational data and abstract, 
standalone probability models. Future iterations will introduce a fully 
symbolic mathematics core, allowing for automatic derivation of likelihoods, 
gradients, and diagnostics.

---

## 🏗️ Project Architecture

The library is built using a highly scalable mixin architecture, 
separating data representation from mathematical operations.

---

## 🚀 Quick Start

Basic initialization requires importing the package and passing your data 
into the `represent()` function. This acts as the gateway to the `Stat` engine, 
similar to `np.array()`.

```python
import src.stat as stat

# Automatically converts lists to optimized NumPy arrays under the hood
data = stat.represent([4, 8, 6, 5, 3, 8])

print(data.mean())
>>> 5.6667
```

### 🎨 Data Visualization

`Stat` supports beautiful terminal-based data tables via `rich` and high-quality plots via `seaborn`.

#### Terminal Tables
```python
# Display with themes like "ocean", "sunset", "forest", or "cyan"
data.show(theme="ocean")
```

#### Statistical Plotting
The `.plot()` method automatically detects the best visualization based on your data:

```python
# 1D Data -> Automatic Histogram + KDE
data.plot() 

# 2D Numeric -> Automatic Scatter Plot
df.plot(columns=['bmi', 'charges'])

# Categorical vs Numeric -> Automatic Box Plot
df.plot(columns=['smoker', 'charges'])

# Categorical -> Automatic Count Plot
df.plot(columns=['region'])

# Correlation Heatmap
df.plot(kind='heatmap')
```

**Supported Plot Types (`kind`):**
- `scatter`: Relationship between two variables.
- `hist` / `kde`: Distribution analysis.
- `box` / `violin`: Statistical spread (great for comparing categories).
- `count`: Frequency of categorical values.
- `heatmap`: Correlation matrices.

You can further customize plots using `figsize`, `title`, `palette`, and `hue`.

---

## 🧮 Core Operations

### 1D Arrays & Descriptive Statistics

The `Stat` object supports a massive suite of descriptive statistics 
out of the box, cleanly handling `NaN` values and supporting sample vs. 
population toggles.

```python
# Averages (Arithmetic, Geometric, Harmonic)
print(data.mean(method='g'))
>>> 5.3343

# Spread & Shape
print(data.iqr())
>>> 3.25

print(data.sem()) # Standard Error of the Mean
>>> 0.881

```

### Pandas DataFrames & 2D Data

`Stat` seamlessly handles multi-dimensional tabular data when initialized 
with a `pd.DataFrame`. While it preserves all columns (including categorical data), 
it automatically targets numeric data for calculations to prevent 
string-parsing crashes.

```python
import pandas as pd
import src.stat as stat

df = pd.DataFrame({
    'PatientID': ['P001', 'P002', 'P003'],
    'Group': ['Control', 'Treatment', 'Control'],
    'Age': [25, 30, 35],
    'Salary': [50_000, 54_000, 62_000]
})

hr_stats = stat.represent(df)

# All columns are preserved in .data
print(hr_stats.data.columns)
>>> Index(['PatientID', 'Group', 'Age', 'Salary'], dtype='object')

# Calculations automatically target numeric columns
print(hr_stats.mean())
>>> Age          30.0
>>> Salary    55333.33
>>> dtype: float64

# show() hides non-numeric columns by default
hr_stats.show()

# Use non_numeric=True to see everything
hr_stats.show(non_numeric=True)

# Control the output size for large datasets
hr_stats.show(max_rows=10, max_columns=5)
hr_stats.show(max_rows='all') # Show all rows
```

**The Summary Method:** Generates a comprehensive statistical 
breakdown across all columns.

```python
print(hr_stats.summary())
>>>            mean   median   variance       std       sem  ...
>>> Age        35.0     35.0       50.0   7.07106   3.16227  ...
>>> Salary  58800.0  58000.0   47360000  6881.860  3077.661  ...

```

---

## 📈 Distributions Engine

The `distributions/` module features a robust suite of standalone 
mathematical models with full support for vectorized inputs via SciPy and NumPy.

### Continuous Distributions

Includes `Normal`, `Exponential`, `Gamma`, `Beta`, `TDistribution`, and `ChiSquare`. Each supports `.pdf()`, `.cdf()`, `.ppf()` (inverse CDF), `.rvs()` (random sampling), `.mean()`, `.variance()`, and `.entropy()`.

```python
# Find the exact 95th percentile of a Normal Distribution
norm = stat.Normal(mu=100, sigma=15)
print(f"95th Percentile: {norm.ppf(0.95):.2f}") 

```

### Discrete Distributions

Includes `Binomial`, `Poisson`, `Geometric`, and `NegativeBinomial`.

```python
# Vectorized PMF for a Binomial distribution
coin = stat.Binomial(n=10, p=0.5)
print(coin.pmf([3, 4, 5])) 

```

---

## 🎲 Foundational Probability (`prob.py`)

Handles core probability theorems and discrete expectations.

```python
from src.stat.prob import Prob

outcomes = [100_000, 40_000, -20_000]
probabilities = [0.20, 0.50, 0.30]

print(Prob.expected_value(outcomes, probabilities))
>>> 34000.00

```

---

## 🧪 Testing

This project utilizes `pytest` to ensure mathematical accuracy across the engine.
To run the test suite, simply navigate to the root directory and execute:

```bash
pytest -v
```

---

## Asset Files:

 
`insurance.csv` is downloaded from [kaggle](https://www.kaggle.com/datasets/mirichoi0218/insurance?resource=download)

`Multi_Cuisine_Recipe_Dataset.csv` is downloaded from [kaggle](https://www.kaggle.com/datasets/sonalshinde123/multi-cuisine-recipe-dataset)



---

## 🛣️ Roadmap

*For advanced feature planning, see `FUTURE.md`.*

### Completed Features ✅

* Seamless `NaN` handling and `np.nanmean()` logic.
* Robust spread metrics: `iqr()`, `mad()`, `sem()`.
* Distribution shape metrics: `skewness()`, `kurtosis()`.
* Feature relationship mapping via `.corr()`.
* Object-oriented discrete probability models (Binomial, Poisson, Geometric, Negative Binomial).
* Highly optimized, vectorized continuous probability models (Normal, Exponential, Gamma, Beta, T-Dist, Chi-Square).
* **Inferential Statistics:** Vectorized T-tests (one-sample, two-sample, paired), Z-tests, One-way ANOVA, and Chi-Square Goodness of Fit.

### Upcoming Features 🚀

* **Regression Module:** Linear, Logistic, and GLMs.
* **Symbolic Engine:** Auto-differentiation, symbolic likelihood derivation, and automatic MLE solving.
* **Graphers:** Graphs for certain functions (including Regression)

---

*Developed by Titutiger*

