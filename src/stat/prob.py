# prob.py

from utils import _conv

def fact(obj: int) -> float:
    if not isinstance(obj, int) or obj < 0:
        raise ValueError("`obj` must be a non-negative natural number.")
    if obj == 1 or obj == 0:
        return float(obj)

    return float(obj * fact(obj - 1))

def perm(n: int, r: int) -> float:
    """
    This gets the total permutations of a group.
    Using the formula: nCr, where `n` is the total size of the group and r is the number of selections.
    It means, from n, select r or from 10 select any 3.
    """
    return float(
        fact(n) / (fact(r) * fact(n - r))
    )

def comb(n: int, r: int) -> float:
    return float(
        fact(n) / (fact(r) * fact(n - r))
    )