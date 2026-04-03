import pandas as pd
from rich.console import Console
from rich.table import Table
from typing import Optional

def df_to_table(
    df: pd.DataFrame,
    title: str = "DataFrame",
    show_index: bool = True,
    index_name: str = "Index",
    theme: str = "default"
) -> Table:
    """
    Convert a pandas.DataFrame to a rich.table.Table with theme support.
    
    Themes:
        - default: Standard cyan/white
        - ocean: Blue/Teal/White
        - forest: Green/Yellow/White
        - sunset: Magenta/Orange/Yellow
        - mono: B&W grayscale
    """
    # src/stat/nb/t_rich.py

import pandas as pd
from rich.console import Console
from rich.table import Table
from typing import Optional
from ..themes import THEMES, get_rich_box

def df_to_table(
    df: pd.DataFrame,
    title: str = "DataFrame",
    show_index: bool = True,
    index_name: str = "Index",
    theme: str = "default"
) -> Table:
    """
    Convert a pandas.DataFrame to a rich.table.Table with theme support.
    """
    theme_cfg = THEMES.get(theme, THEMES["default"])["rich"]
    
    table = Table(
        title=title, 
        box=get_rich_box(theme_cfg["box_style"]),
        header_style=theme_cfg["header"]
    )
    
    if show_index:
        table.add_column(index_name, justify="right", style=theme_cfg["index"], no_wrap=True)
        
    for column in df.columns:
        table.add_column(str(column), style=theme_cfg["row"])
        
    for index, row in df.iterrows():
        row_values = [str(val) for val in row]
        if show_index:
            row_values.insert(0, str(index))
        table.add_row(*row_values)
        
    return table

if __name__ == "__main__":
    console = Console()
    
    # Sample data
    data = {
        "Name": ["Alice", "Bob", "Charlie", "David"],
        "Age": [25, 30, 35, 40],
        "City": ["New York", "London", "Paris", "Tokyo"],
        "Score": [88.5, 92.0, 79.5, 95.0]
    }
    df = pd.DataFrame(data)
    
    console.print("[bold underline]Pandas DataFrame Themes via Rich[/bold underline]\n")
    
    for theme_name in ["default", "ocean", "forest", "sunset", "mono"]:
        console.print(f"[bold]Theme: {theme_name}[/bold]")
        console.print(df_to_table(df, title=f"User Stats ({theme_name})", theme=theme_name))
        console.print("\n")
