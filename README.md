# Welcome to Stat

###### A program made for statistics using Python. ~ *Titutiger*

---

## 📌 Project Details

* **Version:** 1.0.0
* **Python:** 3.12+
* **Core Libraries:**
* `numpy`
* `pandas`
* `math`
* `typing`
* `scipy`

---
## Idea
A symbolic + numeric statistical modeling engine
that automatically derives likelihoods, gradients, and diagnostics.
---

### File Structure

Currently, the module is divided into the following files based on functionality:

* **`core.py`** — Includes the core descriptive statistics logic and the main `Stat` class.
* **`prob.py`** — Includes functions to aid with probability calculations.
* **`utils.py`** — Currently contains an equation solver.

---

## Initialization

Basic initialization requires importing the `Stat` class and passing in your data.

```python
from src.stat.core import Stat

# Initializes and converts the list -> np.ndarray under the hood
data = Stat([4, 8, 6, 5, 3, 8])

```

---

## Core Operations

### 1D Arrays (Lists / NumPy)

**Mean**
The `mean()` method takes one argument, `method: str`, which defaults to `'arithmetic'`. It also accepts `'g'` (geometric) and `'h'` (harmonic).

```python
# Arithmetic (Default)
print(round(data.mean(), 4))
>>> 5.6667

# Geometric
print(round(data.mean('g'), 4))
>>> 5.3343

# Harmonic
print(round(data.mean('h'), 4))
>>> 5.0

```

**Median**
The `median()` method includes a `return_index: bool` argument (defaults to `False`).

```python
print(round(data.median(), 4))
>>> 5.5

# If return_index is set to True:
print(data.median(True))
>>> {'index': (3, 2), 'value': 5.5}

```

**Mode & Range**

```python
print(round(data.mode(), 4))
>>> 8.0

print(round(data.range(), 4))
>>> 5.0

```

**Magic Methods & Properties**
The `Stat` class supports operator overloading for simple combinations and includes properties for data inspection.

```python
from src.stat.core import Stat

a = Stat([1, 2, 3, 4])
b = Stat([5, 6, 7, 8])

# __add__()
print(a + b)
>>> [1. 2. 3. 4. 5. 6. 7. 8.]

# .shape property
print(a.shape)
>>> (4,)

```

---

### Pandas DataFrames

`Stat` seamlessly handles multi-dimensional tabular data when initialized with a `pd.DataFrame`.

```python
import pandas as pd
from src.stat.core import Stat

data = {
    'Employee': ['Alice', 'Bob', 'Charlie', 'Diana', 'Evan'],
    'Age': [25, 30, 35, 40, 45],
    'Salary': [50_000, 54_000, 62_000, 70_000, 58_000]
}
df = pd.DataFrame(data)

# Init with pd.DataFrame:
df = Stat(df)

```

**DataFrame Operations**
Operations automatically apply to all numeric columns unless a specific column is targeted.

```python
# Geometric mean of all numeric columns
print(df.mean(method='g'))
>>> Age          34.267338
>>> Salary    58405.843101
>>> dtype: float64

# Function applied to a specific column (case-insensitive)
print(df.mean(method='a', series='age'))
>>> 35.0

```

**The Summary Method**
Generates a comprehensive statistical breakdown. The summary can also be filtered by passing a specific column to the `series` argument.

```python
print(df.summary())
>>>            mean   median    variance          std    min    max  range
>>> Age        35.0     35.0        50.0     7.071068     25     45     20
>>> Salary  58800.0  58000.0  47360000.0  6881.860214  50000  70000  20000

```

---

## Roadmap & Future Updates

Basic:
* [x] Support NaNs (Swap w/ `np.nanmean()` logic and skipna integrations)
* [x] Add `.quantile()` and `.iqr()` (Interquartile Range)
* [x] Add `.mad()` (Median Absolute Deviation)
* [ ] Distribution shapes: Skewness and Kurtosis
* [x] Add `.corr()` for a correlation matrix between columns
* [x] Add `.sem()` for Standard Error of the Mean
* [ ] Performance:
* vectorized operations
* numpy-backed arrays
* Numba KIT
* [ ] Stability:
* log-likelihood implementations
* avoid catastrophic cancellation
* stable variance formulae
* stable CDF computations
* [x] Add all discrete distributions:
* binomial, poisson, geometric, negative binomail
* [x] Add all continuous distributions:
* normal, exponential, gamma, beta, t-distribution, chi-square
* Each distribution should support: pdf, cdf, rvs, ppf, mean, variance, entropy
* and vectorized input support.
* [ ] tests: z-test, t-test, chi-square test, ANOVA
* power analysis and effect size computation.
* [ ] regression: linear, logistic, regularization, GLMs
* [ ] differentiation:
* symbolic derivation of likelihood functions, automatic MLE solving,
* symbolic to numeric conversion, auto differentiation.
* Stat + symbolic math!!!!!!!!!!!!!!!!!!!!

Advanced:
* [ ] Comparison tables:
* against SciPy
* [ ] Packaging:
* semantic versioning
* proper wheels
* [ ] Models:
```python
model = LinearModel(...)
model.diagnose()
```
* multicollinearity detection,
* residual analysis
* heteroscedasticity tests
* influence measures
* [ ] Bayesian Module
* conjugate priors, posterior computation, MCMC sampling
* Gibbs sampling, variational inference.
* [ ] Time Series
* AR, MA, ARIMA, Forecast intervals, seasonality detection
* [ ] Uncertainty Propogation
* Taylor expansion
* Monte Carlo simulation


---

---
# Prob
`Prob` is like `stat` but instead of statistics,
it handles probability.

## Initialization
Basic initialization requires importing
the `Prob` class and passing in your daya.

```python
from src.stat.prob import Prob

outcomes = [100_000, 40_000, -20_000]
probabilities = [0.20, 0.50, 0.30]
```

### `E(X) or expected value`:
```python
ev = Prob.expected_value(outomes, probabilities)
>>> 34,000.00
```

### `Binomial P.M.F (probability mass function)`:
```python
bpmf = Prob.binomial_pmf(n=20, k=2, p=0.05)
>>> 0.1887
```



---

*~ Titutiger*

---