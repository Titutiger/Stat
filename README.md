# Welcome to Stat
###### A program made for statistics using python. ~ Titutiger

## Project details:
> Version: 1.0.0
> 
> Python: 3.12
> 
> Libraries:
> - numpy
> - pandas
> - math
> - typing

Currently, the following files have
the following functionality:
> core.py
> - includes core statistics.
> 
> prob.py
> - includes functions to aid with probability.
> 
> utils.py
> - currently contains an equation solver.

___

## Init:
Basic initialization:
```python
from src.stat.core import Stat

data = Stat([array])
```
> ###### Converts [array] -> np.ndarray

Example:
```python
data = Stat([4, 8, 6, 5, 3, 8])
```

## Core Operations:
___
###### For 1D arrays*
___
```python
# mean:
print(round(data.mean(), 4))
>>> 5.667
```
> Herein `data.mean()` takes 1 argument `method: str`
> wherein it's default value is `arithmetic`.
> 
> `data.mean()` can accept:
> `(a)rithmetic`, `(g)eometric` and `(h)armonic`.

```python
print(round(data.mean('g'), 4))
>>> 5.3343

print(round(data.mean('h'), 4))
>>> 5.0
```
___
```python
# median
print(round(data.median(), 4))
>>> 5.5
```
> Herein `data.median` has 1 argument
> `return_index: bool` which is set to `False`.
> 
> If true:
>```python
> print(round(data.median(True), 4))
> >>> {'index': (3,2), 'value': 5.5}
>```

___
```python
print(round(data.mode(), 4))
>>> 8.0

print(round(data.range(), 4))
>>> 5.0
```
___
`__add__()`:
```python
import src.stat.core as Stat

a = Stat([1, 2, 3, 4])
b = Stat([5, 6, 7, 8])

print(a + b)
>>> [1. 2. 3. 4. 5. 6. 7. 8.]

```

`.shape`
```python
import src.stat.core as Stat

a = Stat([1, 3, 2])
print(a.shape)
>>> (3,)
```
___
###### For pd.DataFrame*
___

```python
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
```
Core Operations:
```python
print(df.mean(method='g'))
>>> Age          34.267338
>>> Salary    58405.843101
>>> dtype: float64

# Mean/func of specific column:
print(df.mean('a', 'age'))
>>> 35.0

# and the same ...

print(df.summary())
>>>            mean   median    variance          std    min    max  range
>>> Age        35.0     35.0        50.0     7.071068     25     45     20
>>> Salary  58800.0  58000.0  47360000.0  6881.860214  50000  70000  20000
# Summary can also accept specified columns.
```

___

Future Updates:
- [ ] Support NaNs
- swap w/ np.nanmean() n othrs...
- [ ] Adding `.quantile()` and `.iqr()` interquartile range 
- [ ] Distribution shapes: skewness n kurtosis
- [ ] `.corr()` correlation matrix btwn columns
- [ ] `.sem()` std error mean
- [ ] `.mad()` median absolute deviation

___

~ Titutiger