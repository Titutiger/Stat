# core.py

from utils import _conv
import numpy as np
import math

def mean(arr: np.ndarray, type_: str) -> float | None:
    if not isinstance(arr, np.ndarray):
        arr = _conv(arr)

    if arr.ndim != 1:
        raise ValueError("`arr` must be in 1D.")

    n = len(arr)
    type_ = type_.lower()

    if type_ in ['a', 'ari', 'arithmetic']:
        return float(sum(arr) / n)

    elif type_ in ['g', 'geo', 'geometric']:
        if (arr<0).sum() > 0:
            raise ValueError('Negative values will break geometric mean.')

        return float(np.power(math.prod(arr), 1/n))

    elif type_ in ['h', 'har', 'harmonic']:
        return float(n / np.sum(1/arr))


    else:
        raise ValueError('Enter a valid type of mean.')

    return None

if __name__ == '__main__':
    arr = np.array([1, 2, 3, 4, 5])
    mean(arr, '')