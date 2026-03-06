import numpy as np
import src.stat as stat

# Generate 5 random variables from a Gamma distribution
g = stat.Gamma(alpha=2, beta=1)
print(f"Random Variates: {g.rvs(size=5)}")
