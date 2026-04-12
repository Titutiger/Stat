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

---

## `Stat` (Class)

The core engine of the library. It inherits from `DescriptiveMixin`, giving it access to all statistical operations.

### Key Properties
- `tag`: The origin of the data (e.g., 'numpy', 'dataframe').
- `is_df`: Boolean, true if the data is a Pandas DataFrame.
- `data`: The underlying data.
- `dim`: The number of **numeric** columns in the data.

### Internal Logic: The `_apply` pattern
Every statistical method (like `.mean()`) automatically works on:
1. **1D Data**: Returns a single float.
2. **DataFrames**: Calculates the statistic for every **numeric** column and returns a Series.
3. **Targeting**: Pass `series='column_name'` to calculate the statistic for just one column in a DataFrame.

---

## Manipulators

### `.select(*cols)`
Returns a new `Stat` object with only the specified columns.
- **`*cols`**: Column names or indices.
- **Usage**: `data.select('Age', 'Salary')`

### `.filter_types(keep='numeric')`
Filters the DataFrame to keep only specific types of columns.
- **`keep`**:
    - `'numeric'`, `'num'`, `'n'`: Keep only numeric columns.
    - `'categorical'`, `'cat'`, `'c'`, `'non_numeric'`, `'nn'`: Keep only non-numeric columns.
    - `'all'`: Keep everything.
- **Usage**: `data.filter_types(keep='nn')`

### `.transform(col, mapping)`
Replaces specific values in a DataFrame column.
- **`col`**: The column name to transform.
- **`mapping`**: A list of pairs `['OldValue', 'NewValue', ...]`.
- **Usage**: `data.transform('Gender', ['M', 1, 'F', 0])`

### `.frequencies(series)`
Returns the counts of all unique elements in a categorical column.
- **Usage**: `data.frequencies('Country')`

### `.count_value(col, target)`
Returns the count of a specific value in a column.
- **Usage**: `data.count_value('Status', 'Success')`

### `.crosstab(index, columns, margins=False)`
Computes a frequency matrix of two categorical columns.
- **`index`**: Column for rows.
- **`columns`**: Column for columns.
- **`margins`**: Add row/column subtotals.
- **Usage**: `data.crosstab('Region', 'ProductType', margins=True)`

---

## Data Visualization & Plotting

The `Stat` object provides high-level plotting capabilities powered by `seaborn` and `matplotlib`.

### `.plot(columns=None, kind=None, theme=None, title=None, **kwargs)`
- **`columns` (str | list, optional)**: Specify which columns to plot.
- **`kind` (str, optional)**: Force a specific plot type:
    - `'scatter'`, `'hist'`, `'kde'`, `'box'`, `'violin'`, `'count'`, `'heatmap'`.
- **`theme` (str, optional)**: Set the color theme (e.g., `'ocean'`, `'sunset'`, `'forest'`).
- **`title` (str, optional)**: Custom title for the plot.
- **`**kwargs`**: Passed directly to Seaborn (e.g., `hue`, `bins`).

---

## Visual Representation (Terminal)

### `.show(title='Stat Object', theme=None, max_rows=20, max_columns=None, width=None, columns=None)`
Displays the data as a formatted table in the terminal using `rich`.

- **`title`**: Table title.
- **`theme`**: Color palette (`'cyan'`, `'ocean'`, `'forest'`, `'sunset'`, `'default'`).
- **`max_rows`**: Maximum rows to display. Use `'all'` or `'*'` for everything.
- **`max_columns`**: Maximum columns to display.
- **`width`**: Table width (integer or `'*'`).
- **`columns`**: List of specific columns to show.

**Example:**
```python
s.show(theme="sunset", max_rows=10)
```
