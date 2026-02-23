# utils

import numpy as np
import math
from typing import Any

def _conv(obj: Any) -> np.ndarray:
    try:
        return np.asarray(obj, dtype=float)
    except Exception:
        raise ValueError("Cannot convert to numpy array.")

#=================================================================
