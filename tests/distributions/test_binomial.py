import numpy as np
import src.stat as stat

# Binomial: If I flip a fair coin 10 times (n=10, p=0.5),
# what is the probability I get exactly 5 heads?
coin = stat.Binomial(n=10, p=0.5)
print(f"Chance of exactly 5 heads: {coin.pmf(5):.4f}") # Output: 0.2461
