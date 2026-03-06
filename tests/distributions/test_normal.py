import numpy as np
import src.stat as stat

# Find the exact 95th percentile (PPF) of a Normal Distribution
norm = stat.Normal(mu=100, sigma=15)
print(f"95th Percentile: {norm.ppf(0.95):.2f}")
# Output: 124.67
