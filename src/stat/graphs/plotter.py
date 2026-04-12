# src/stat/graphs/plotter.py

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from ..themes import THEMES

def plot_stat(data, is_df, is_1d, theme_name="default", title=None, columns=None, kind=None, **kwargs):
    """Displays graphs using matplotlib and seaborn with enhanced logic and theme support."""
    theme_cfg = THEMES.get(theme_name, THEMES["default"])["plot"]
    
    # Set style and context
    sns.set_theme(style=theme_cfg["sns_style"])
    plt.rcParams['axes.facecolor'] = theme_cfg.get("bg", "white")
    plt.rcParams['figure.facecolor'] = theme_cfg.get("bg", "white")
    
    # Extract common kwargs (popping them so they don't cause 'multiple values' errors in seaborn)
    figsize = kwargs.pop("figsize", (10, 6))
    color = kwargs.pop("color", theme_cfg["primary"])
    palette = kwargs.pop("palette", "viridis")
    hue = kwargs.pop("hue", None)
    
    fig, ax = plt.subplots(figsize=figsize)
    
    if is_df:
        # 1. Handle Column Selection
        if columns:
            if isinstance(columns, str):
                columns = [columns]
            
            # Case-insensitive mapping
            col_map = {str(c).lower(): c for c in data.columns}
            matched_cols = []
            for tc in columns:
                if str(tc).lower() in col_map:
                    matched_cols.append(col_map[str(tc).lower()])
                else:
                    print(f"Warning: Column '{tc}' not found.")
            
            if not matched_cols:
                print("No valid columns selected to plot.")
                return
            plot_df = data[matched_cols]
        else:
            plot_df = data

        # 2. Determine Plot Kind if not specified
        if kind is None:
            numeric_cols = plot_df.select_dtypes(include=[np.number]).columns
            cat_cols = plot_df.select_dtypes(exclude=[np.number]).columns
            
            if len(plot_df.columns) == 1:
                kind = "hist" if plot_df.columns[0] in numeric_cols else "count"
            elif len(plot_df.columns) == 2:
                if len(numeric_cols) == 2:
                    kind = "scatter"
                elif len(numeric_cols) == 1 and len(cat_cols) == 1:
                    kind = "box"
                else:
                    kind = "count" # Fallback for two categoricals
            else:
                kind = "hist" # Fallback for many columns

        # 3. Execute Plotting Logic
        try:
            if kind == "scatter":
                x, y = plot_df.columns[:2]
                sns.scatterplot(data=data, x=x, y=y, hue=hue, palette=palette, ax=ax, **kwargs)
                if not title: title = f"{x} vs {y}"
                
            elif kind == "hist":
                sns.histplot(data=plot_df, kde=True, palette=palette, ax=ax, **kwargs)
                if not title: title = "Distribution Plot"
                
            elif kind == "kde":
                sns.kdeplot(data=plot_df, palette=palette, ax=ax, **kwargs)
                if not title: title = "Density Plot"
                
            elif kind == "box":
                if len(plot_df.columns) >= 2:
                    # Prefer Categorical on X, Numeric on Y
                    cats = plot_df.select_dtypes(exclude=[np.number]).columns
                    nums = plot_df.select_dtypes(include=[np.number]).columns
                    x = cats[0] if len(cats) > 0 else plot_df.columns[0]
                    y = nums[0] if len(nums) > 0 else plot_df.columns[1]
                    
                    local_hue = hue
                    local_kwargs = kwargs.copy()
                    if local_hue is None:
                        local_hue = x
                        if 'legend' not in local_kwargs:
                            local_kwargs['legend'] = False
                            
                    sns.boxplot(data=data, x=x, y=y, hue=local_hue, palette=palette, ax=ax, **local_kwargs)
                else:
                    sns.boxplot(data=plot_df, palette=palette, ax=ax, **kwargs)
                if not title: title = "Box Plot"
                
            elif kind == "violin":
                if len(plot_df.columns) >= 2:
                    cats = plot_df.select_dtypes(exclude=[np.number]).columns
                    nums = plot_df.select_dtypes(include=[np.number]).columns
                    x = cats[0] if len(cats) > 0 else plot_df.columns[0]
                    y = nums[0] if len(nums) > 0 else plot_df.columns[1]
                    
                    local_hue = hue
                    local_kwargs = kwargs.copy()
                    if local_hue is None:
                        local_hue = x
                        if 'legend' not in local_kwargs:
                            local_kwargs['legend'] = False
                            
                    sns.violinplot(data=data, x=x, y=y, hue=local_hue, palette=palette, ax=ax, **local_kwargs)
                else:
                    sns.violinplot(data=plot_df, palette=palette, ax=ax, **kwargs)
                if not title: title = "Violin Plot"

            elif kind == "count":
                x = plot_df.columns[0]
                local_hue = hue
                local_kwargs = kwargs.copy()
                if local_hue is None:
                    local_hue = x
                    if 'legend' not in local_kwargs:
                        local_kwargs['legend'] = False
                sns.countplot(data=data, x=x, hue=local_hue, palette=palette, ax=ax, **local_kwargs)
                if not title: title = f"Count of {x}"
                
            elif kind == "heatmap":
                corr = plot_df.select_dtypes(include=[np.number]).corr()
                sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax, **kwargs)
                if not title: title = "Correlation Heatmap"
            
            else:
                print(f"Unknown plot kind: {kind}")
                return

        except Exception as e:
            print(f"Error generating plot: {e}")
            return

    else:
        # 1D Data (Numpy or List)
        kind = kind or "hist"
        if kind == "hist":
            sns.histplot(data, kde=True, color=color, ax=ax, **kwargs)
        elif kind == "box":
            sns.boxplot(x=data, color=color, ax=ax, **kwargs)
        elif kind == "violin":
            sns.violinplot(x=data, color=color, ax=ax, **kwargs)
        elif kind == "kde":
            sns.kdeplot(data, color=color, ax=ax, **kwargs)
        if not title: title = "1D Data Plot"

    ax.set_title(title or "Stat Plot")
    if theme_cfg.get("grid", True):
        ax.grid(True, linestyle='--', alpha=0.6)
        
    plt.tight_layout()
    plt.show()
