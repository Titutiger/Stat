# src/stat/graphs/plotter.py

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from ..themes import THEMES

def plot_stat(data, is_df, is_1d, theme_name="default", title="Stat Plot", **kwargs):
    """Displays graphs using matplotlib and seaborn with theme support."""
    theme_cfg = THEMES.get(theme_name, THEMES["default"])["plot"]
    
    # Set style
    sns.set_style(theme_cfg["sns_style"])
    plt.rcParams['axes.facecolor'] = theme_cfg["bg"]
    plt.rcParams['figure.facecolor'] = theme_cfg["bg"]
    
    fig, ax = plt.subplots(figsize=kwargs.get("figsize", (10, 6)))
    
    color = theme_cfg["primary"]
    accent = theme_cfg["accent"]
    
    if is_df:
        # Allow selecting specific columns
        target_columns = kwargs.get("columns")
        if target_columns:
            if isinstance(target_columns, str):
                target_columns = [target_columns]
            
            # Case-insensitive column matching
            col_map = {str(c).lower(): c for c in data.columns}
            matched_cols = []
            for tc in target_columns:
                if str(tc).lower() in col_map:
                    matched_cols.append(col_map[str(tc).lower()])
                else:
                    print(f"Warning: Column '{tc}' not found.")
            
            if not matched_cols:
                print("No valid columns selected to plot.")
                return
            
            numeric_df = data[matched_cols].select_dtypes(include=[np.number])
        else:
            numeric_df = data.select_dtypes(include=[np.number])

        if numeric_df.empty:
            print("No numeric data to plot.")
            return
            
        if len(numeric_df.columns) == 2 and kwargs.get("kind") != "hist":
            sns.scatterplot(data=numeric_df, x=numeric_df.columns[0], y=numeric_df.columns[1], color=color, ax=ax)
            ax.set_title(f"{numeric_df.columns[0]} vs {numeric_df.columns[1]}")
        elif len(numeric_df.columns) == 1:
            kind = kwargs.get("kind", "hist")
            col_name = numeric_df.columns[0]
            if kind == "hist":
                sns.histplot(numeric_df[col_name], kde=True, color=color, ax=ax)
            elif kind == "box":
                sns.boxplot(x=numeric_df[col_name], color=color, ax=ax)
            elif kind == "violin":
                sns.violinplot(x=numeric_df[col_name], color=color, ax=ax)
            ax.set_xlabel(col_name)
        else:
            # Default to histogram/kde for multiple columns
            for i, col in enumerate(numeric_df.columns):
                sns.histplot(numeric_df[col], kde=True, label=col, color=sns.color_palette("husl", len(numeric_df.columns))[i], ax=ax, alpha=0.5)
            ax.legend()
    else:
        # 1D data
        kind = kwargs.get("kind", "hist")
        if kind == "hist":
            sns.histplot(data, kde=True, color=color, ax=ax)
        elif kind == "box":
            sns.boxplot(x=data, color=color, ax=ax)
        elif kind == "violin":
            sns.violinplot(x=data, color=color, ax=ax)
            
    ax.set_title(title)
    if theme_cfg["grid"]:
        ax.grid(True, linestyle='--', alpha=0.7)
        
    plt.tight_layout()
    plt.show()
