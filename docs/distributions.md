# Probability Distributions

Probability distributions model how data values are distributed in a population.

## Common Interface

All distribution objects share these methods:
- **`.mean()`**: Returns the expected value.
- **`.variance()`**: Returns the variance.
- **`.rvs(size=1)`**: Generates random variates (samples) from the distribution.

---

## Continuous Distributions

Continuous distributions represent variables that can take any value within a range. They use:
- **`.pdf(x)`**: Probability Density Function.
- **`.cdf(x)`**: Cumulative Distribution Function.
- **`.ppf(q)`**: Percent Point Function (Inverse CDF), used to find critical values.

### `Normal(mu=0.0, sigma=1.0)`
- **Niche**: The "Gaussian" distribution. Standard model for natural phenomena.
- **Mean**: $\mu$
- **Variance**: $\sigma^2$

### `Exponential(lam=1.0)`
- **Niche**: Models the time between independent events (e.g., time between server crashes).
- **Mean**: $1 / \lambda$
- **Variance**: $1 / \lambda^2$

### `Gamma(alpha, beta)`
- **Niche**: Flexible distribution for positive-only data (e.g., rainfall, insurance claims).
- **Mean**: $\alpha / \beta$
- **Variance**: $\alpha / \beta^2$

### `Beta(alpha, beta)`
- **Niche**: Models probabilities or proportions (constrained between 0 and 1).
- **Mean**: $\alpha / (\alpha + \beta)$
- **Variance**: $(\alpha\beta) / [(\alpha+\beta)^2(\alpha+\beta+1)]$

### `TDistribution(df)`
- **Niche**: "Student's T." Essential for small sample sizes where the population standard deviation is unknown.
- **Mean**: $0$ (for $df > 1$)
- **Variance**: $df / (df - 2)$ (for $df > 2$)

### `ChiSquare(df)`
- **Niche**: Used in hypothesis testing (e.g., test of independence). Special case of Gamma.
- **Mean**: $df$
- **Variance**: $2df$

**Usage Example:**
```python
from src.stat.distributions import Normal

# Initialize a standard normal distribution
dist = Normal(mu=0, sigma=1)

# Find the probability that X <= 1.96
p = dist.cdf(1.96)  # ~0.975

# Find the 95th percentile
val = dist.ppf(0.95)
```

---

## Discrete Distributions

Discrete distributions represent variables that take on distinct, separate values. They use:
- **`.pmf(k)`**: Probability Mass Function.
- **`.cdf(k)`**: Cumulative Distribution Function.

### `Binomial(n, p)`
- **Niche**: Models the number of "successes" in `n` independent trials (e.g., number of heads in 10 coin flips).
- **Mean**: $np$
- **Variance**: $np(1-p)$

### `Poisson(lam)`
- **Niche**: Models the number of events in a fixed interval of time or space (e.g., emails per hour).
- **Mean**: $\lambda$
- **Variance**: $\lambda$

### `Geometric(p)`
- **Niche**: Models the number of trials needed to get the *first* success.
- **Mean**: $1/p$
- **Variance**: $(1-p)/p^2$

### `NegativeBinomial(r, p)`
- **Niche**: Models the number of *failures* before the $r$-th success.
- **Mean**: $r(1-p)/p$
- **Variance**: $r(1-p)/p^2$

**Usage Example:**
```python
from src.stat.distributions import Binomial

# 10 flips of a fair coin
coin_flips = Binomial(n=10, p=0.5)

# Probability of getting exactly 5 heads
prob_5 = coin_flips.pmf(5)

# Probability of getting 3 or fewer heads
prob_3_or_less = coin_flips.cdf(3)
```
