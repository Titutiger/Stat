import src.stat as stat
import pandas as pd
import numpy as np

# Create sample data
data = {
    "Age": [25, 30, 35, 40, 45, 50, 55, 60],
    "Salary": [50000, 55000, 60000, 65000, 70000, 75000, 80000, 85000]
}
df = pd.DataFrame(data)
s = stat.represent(df)

# Test different themes
themes = ["ocean", "forest", "sunset", "mono"]

print("Testing Show and Plot with various themes...")

for t in themes:
    print(f"\n--- Theme: {t} ---")
    s.show(theme=t)
    # Note: s.plot() will open a window and pause execution until closed if not handled.
    # For a CLI environment, we just show that the method exists.
    print(f"Plot method available for theme '{t}': s.plot(theme='{t}')")

# 1D data test
s1d = stat.represent(np.random.normal(0, 1, 100))
print("\n--- 1D Data (Sunset) ---")
s1d.show(theme="sunset")
