# Probability Distributions

Probability distributions model how data values are distributed in a population.

## Common Interface

All distribution objects share these methods:
- **`.mean()`**: Returns the expected value.
- **`.variance()`**: Returns the variance.
- **`.rvs(size=1)`**: Generates random variates (samples) from the distribution.

---

## Continuous Distributions

Use **`.pdf(x)`** (Probability Density Function) and **`.cdf(x)`** (Cumulative Distribution Function).

### `Normal(mu=0.0, sigma=1.0)`
- **Niche**: The "Gaussian" distribution. Standard model for natural phenomena.
- **Key Method**: `.ppf(q)` (Percent Point Function/Inverse CDF) is used to find critical values (e.g., "What value represents the 95th percentile?").

### `Exponential(lam=1.0)`
- **Niche**: Models the time between independent events (e.g., time between server crashes).

### `Gamma(alpha, beta)`
- **Niche**: Flexible distribution for positive-only data (e.g., rainfall, insurance claims).

### `TDistribution(df)`
- **Niche**: "Student's T." Essential for small sample sizes where the standard deviation is unknown.

---

## Discrete Distributions

Use **`.pmf(k)`** (Probability Mass Function) and **`.cdf(k)`**.

### `Binomial(n, p)`
- **Niche**: Models the number of "successes" in `n` independent trials (e.g., number of heads in 10 coin flips).

### `Poisson(lam)`
- **Niche**: Models the number of events in a fixed interval of time or space (e.g., emails per hour).

### `Geometric(p)`
- **Niche**: Models the number of trials needed to get the *first* success.

### `NegativeBinomial(r, p)`
- **Niche**: Models the number of *failures* before the $r$-th success.
