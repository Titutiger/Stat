# Core Stat Object

The `Stat` object is the primary data container in the library. It is designed to act as a bridge between raw data (lists, numpy arrays) and complex statistical analysis.

## `represent(data)` (Factory Function)

The `represent` function is the recommended way to create a `Stat` object. It automatically tags the data source and prepares it for analysis.

### Usage
```python
import src.stat as stat

# From a list
data = stat.represent([1, 2, 3, 4, 5])

# From a Pandas DataFrame
import pandas as pd
df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
st_df = stat.represent(df)
```

### Niche
Use `represent` instead of calling `Stat()` directly to benefit from "auto-tagging." This allows workflows like `standard_eda` to automatically know if they are dealing with a 1D array or a structured DataFrame.

---

## `Stat` (Class)

The core engine of the library. It inherits from `DescriptiveMixin`, giving it access to all statistical operations.

### Key Properties
- `tag`: The origin of the data (e.g., 'numpy', 'dataframe').
- `is_df`: Boolean, true if the data is a Pandas DataFrame.
- `data`: The underlying cleaned data (numeric columns only).

### Internal Logic: The `_apply` pattern
The `Stat` object uses an internal `_apply` method. This means every statistical method (like `.mean()`) automatically works on:
1. **1D Data**: Returns a single float.
2. **DataFrames**: Calculates the statistic for every numeric column and returns a Series.
3. **Targeting**: You can pass `series='column_name'` to calculate the statistic for just one column in a DataFrame.

---

## Visual Representation

The `Stat` object supports enhanced terminal display using the `rich` library. This is purely for visualization; the underlying data remains a Pandas DataFrame or NumPy array.

### `show(title='Stat Object',theme=None)`
Displays the data as a formatted table in the terminal.

- **`theme` (str, optional)**: Specify a color palette. If not provided, it uses the object's `theme` property (defaulting to "default").

### Available Themes
| Theme     | Description | Colors |
|:----------| :--- | :--- |
| `cyan`    | Standard clean look | Cyan / White |
| `ocean`   | Marine aesthetic | Blue / Teal |
| `forest`  | Nature-inspired | Green / Yellow |
| `sunset`  | High contrast | Magenta / Orange |
| `default` | Grayscale / ASCII | White / Grey |

### Example
```python
s = stat.represent(my_dataframe)

# Default view
s.show()

# Change the default theme for this object
s.theme = "forest"
s.show()

# Override for a single call
s.show(theme="sunset")

```


