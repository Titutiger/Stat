# utils

import numpy as np

def mean(data: list | tuple, _type='array') -> float | None:
    if _type == 'array':
        return round(sum(data) / len(data), 3)
    return None

def std_dev(data: list | tuple, _type) -> float:
    if _type == 'sample':
        n = len(data)
        if n < 2:
            raise ValueError("At least two data points required.")

        m = sum(data) / n
        variance = sum((x - m) ** 2 for x in data)

        return round((variance / (n - 1 if _type == 'sample' else n)) ** 0.5, 3)


if __name__ == '__main__':
    print(mean([81, 93, 98, 89, 88]))
    print(std_dev([81, 93, 98, 89, 88], _type='sample'))