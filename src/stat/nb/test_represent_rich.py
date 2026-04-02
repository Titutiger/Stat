import pandas as pd
import numpy as np
import sys
import os

# Add src to path to import stat
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from src.stat.api import represent

def test_rich_representation():
    # 1. Create data
    data = {
        "Math": [85, 92, 78, 65, 88],
        "Science": [90, 88, 82, 70, 95]
    }
    df = pd.DataFrame(data)
    
    # 2. Wrap in Stat object
    s = represent(df)
    
    print("--- Testing Operations (Should be normal) ---")
    print(f"Mean Math: {s.mean(series='Math')}")
    print(f"Type of s.data: {type(s.data)}")
    
    print("\n--- Testing Default Show (Rich) ---")
    s.show()
    
    print("\n--- Testing Ocean Theme ---")
    s.show(theme="ocean")
    
    print("\n--- Testing Forest Theme ---")
    s.show(theme="forest")
    
    print("\n--- Testing Sunset Theme ---")
    s.show(theme="sunset")
    
    print("\n--- Testing Mono Theme ---")
    s.show(theme="mono")
    
    print("\n--- Testing Fallback (Setting theme to None manually) ---")
    original_theme = s.theme
    s.theme = None
    print(f"Repr when theme is None:\n{repr(s)}")
    s.theme = original_theme

if __name__ == "__main__":
    test_rich_representation()
