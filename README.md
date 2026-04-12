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

## Project Details

* **Version:** v0.1.2-alpha
* **Python:** 3.12+
* **Core Dependencies:** `numpy`, `pandas`, `scipy`
* **Testing Framework:** `pytest`

---

## The Vision

`Stat` is designed to be a hybrid statistical modeling engine. 
It bridges the gap between descriptive, observational data and abstract, 
standalone probability models. Future iterations will introduce a fully 
symbolic mathematics core, allowing for automatic derivation of likelihoods, 
gradients, and diagnostics.

---

## Project Architecture and QoL Features

The library is built using a highly scalable mixin architecture, 
separating data representation from mathematical operations.

QoL Features:
- **Elegance:** The API is designed to be intuitive and easy to use.
- **Teaching Value:** Each function comes with clear documentation.
    and use cases.
- **Easy Migration:** Makes it easy to migrate from numpy or pandas.

---

## Installation

> Currently, stat is not on pip, however, I am trying to change that soon.

---
## Quick Start

Basic initialization requires importing the package and passing your data 
into the `represent()` function. This acts as the gateway to the `Stat` engine, 
similar to `np.array()`.

### Init
```python
import src.stat as stat

# Automatically converts lists to optimized NumPy arrays under the hood
data = stat.represent([4, 8, 6, 5, 3, 8])

print(data.mean())
>>> 5.6667
```

---

### Discrete Distributions

Includes `Binomial`, `Poisson`, `Geometric`, and `NegativeBinomial`.

```python
# Vectorized PMF for a Binomial distribution
coin = stat.Binomial(n=10, p=0.5)
print(coin.pmf([3, 4, 5])) 

```

---

### Foundational Probability (`prob.py`)

Handles core probability theorems and discrete expectations.

```python
from src.stat.prob import Prob

outcomes = [100_000, 40_000, -20_000]
probabilities = [0.20, 0.50, 0.30]

print(Prob.expected_value(outcomes, probabilities))
>>> 34000.00

```
---

For more detailed information, visit the [docs](docs)

---

## Testing

This project utilizes `pytest` to ensure mathematical accuracy across the engine.
To run the test suite, simply navigate to the root directory and execute:

```bash
pytest -v
```

---

## License

This project is under the MIT License

---

## Asset Files:

 
- `insurance.csv` is downloaded from [kaggle](https://www.kaggle.com/datasets/mirichoi0218/insurance?resource=download)
- `Multi_Cuisine_Recipe_Dataset.csv` is downloaded from [kaggle](https://www.kaggle.com/datasets/sonalshinde123/multi-cuisine-recipe-dataset)



---

## Roadmap

*For advanced feature planning, see [FUTURE.md](future.txt).*

### Upcoming Features

* **Regression Module:** Linear, Logistic, and GLMs.
* **Symbolic Engine:** Auto-differentiation, symbolic likelihood derivation, and automatic MLE solving.
* **Graphers:** Graphs for certain functions (including Regression)

---

*Developed by Titutiger*

