import pandas as pd
from src.stat.core import Stat

data = {
    'Employee': ['Alice', 'Bob', 'Charlie',
                 'Diana', 'Evan'],
    'Age': [25, 30, 35, 40, 45],
    'Salary': [50_000, 54_000, 62_000, 70_000, 58_000]
}
df = pd.DataFrame(data)

# init with pd.DataFrame:
df = Stat(df)

print(df.summary())
print(df.mean(method='g'))
