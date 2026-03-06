import numpy as np
import src.stat as stat

# Vectorized probabilities of a Chi-Square distribution
chi = stat.ChiSquare(df=4)
print(f"CDF for values [1, 2, 3]: {chi.cdf([1, 2, 3])}")