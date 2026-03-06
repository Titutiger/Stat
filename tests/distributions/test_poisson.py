import numpy as np
import src.stat as stat

# Poisson: If a server crashes 2 times a day on average (lam=2),
# what is the chance it crashes exactly 4 times today?
server = stat.Poisson(lam=2)
print(f"Chance of 4 crashes: {server.pmf(4):.4f}") # Output: 0.0902
