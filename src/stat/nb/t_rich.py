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
    # Define theme palettes
    themes = {
        "default": {
            "header": "bold cyan",
            "index": "cyan",
            "row": "white",
            "box_style": "ROUNDED" # Default rich box
        },
        "ocean": {
            "header": "bold dodger_blue1",
            "index": "deep_sky_blue1",
            "row": "light_cyan1",
            "box_style": "ROUNDED"
        },
        "forest": {
            "header": "bold spring_green3",
            "index": "green3",
            "row": "pale_green1",
            "box_style": "HEAVY"
        },
        "sunset": {
            "header": "bold red",
            "index": "orange1",
            "row": "light_goldenrod1",
            "box_style": "DOUBLE"
        },
        "mono": {
            "header": "bold white on grey27",
            "index": "grey70",
            "row": "grey93",
            "box_style": "ASCII"
        }
    }
    
    selected_theme = themes.get(theme, themes["default"])
    
    # Import box styles dynamically if needed
    from rich import box
    box_map = {
        "ROUNDED": box.ROUNDED,
        "HEAVY": box.HEAVY,
        "DOUBLE": box.DOUBLE,
        "ASCII": box.ASCII
    }
    
    table = Table(
        title=title, 
        box=box_map.get(selected_theme["box_style"]) if selected_theme["box_style"] else box.SQUARE,
        header_style=selected_theme["header"]
    )
    
    if show_index:
        table.add_column(index_name, justify="right", style=selected_theme["index"], no_wrap=True)
        
    for column in df.columns:
        table.add_column(str(column), style=selected_theme["row"])
        
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
