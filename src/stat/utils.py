# utils

import numpy as np
import math
from typing import Any

def _conv(obj: Any) -> np.ndarray:
    try: return np.asarray(obj, dtype=float)
    except Exception: raise ValueError("Cannot convert to numpy array.")

def _cond(arr: Any) -> bool:
    if arr.ndim != 1: raise ValueError("`arr` must be in 1D.")
    else: return True # can be deleted but let it be there for now


#=================================================================
