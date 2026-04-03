# src/stat/themes.py

try:
    from rich import box
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

THEMES = {
    "cyan": {
        "rich": {
            "header": "bold cyan",
            "index": "cyan",
            "row": "white",
            "box_style": "ROUNDED"
        },
        "plot": {
            "primary": "#00FFFF",  # Cyan
            "secondary": "#E0FFFF", # Light Cyan
            "accent": "#008B8B",    # Dark Cyan
            "bg": "white",
            "grid": True,
            "sns_style": "darkgrid"
        }
    },
    "ocean": {
        "rich": {
            "header": "bold dodger_blue1",
            "index": "deep_sky_blue1",
            "row": "light_cyan1",
            "box_style": "ROUNDED"
        },
        "plot": {
            "primary": "#1E90FF",  # DodgerBlue
            "secondary": "#00BFFF", # DeepSkyBlue
            "accent": "#E0FFFF",    # LightCyan
            "bg": "#F0F8FF",        # AliceBlue
            "grid": True,
            "sns_style": "darkgrid"
        }
    },
    "forest": {
        "rich": {
            "header": "bold spring_green3",
            "index": "green3",
            "row": "pale_green1",
            "box_style": "HEAVY"
        },
        "plot": {
            "primary": "#00FF7F",  # SpringGreen
            "secondary": "#00CD00", # Green3
            "accent": "#98FB98",    # PaleGreen
            "bg": "#F5FFFA",        # MintCream
            "grid": True,
            "sns_style": "whitegrid"
        }
    },
    "sunset": {
        "rich": {
            "header": "bold hot_pink",
            "index": "orange1",
            "row": "light_goldenrod1",
            "box_style": "DOUBLE"
        },
        "plot": {
            "primary": "#FF69B4",  # HotPink
            "secondary": "#FFA500", # Orange
            "accent": "#FAFAD2",    # LightGoldenrodYellow
            "bg": "#FFF0F5",        # LavenderBlush
            "grid": True,
            "sns_style": "darkgrid"
        }
    },
    "mono": {
        "rich": {
            "header": "bold white on grey27",
            "index": "grey70",
            "row": "grey93",
            "box_style": "ASCII"
        },
        "plot": {
            "primary": "#444444",  # Dark Grey
            "secondary": "#888888", # Grey
            "accent": "#CCCCCC",    # Light Grey
            "bg": "white",
            "grid": True,
            "sns_style": "ticks"
        }
    },
    "default": {
        "rich": {
            "header": "bold white on grey27",
            "index": "grey70",
            "row": "grey93",
            "box_style": "ASCII"
        },
        "plot": {
            "primary": "#333333",
            "secondary": "#666666",
            "accent": "#999999",
            "bg": "white",
            "grid": True,
            "sns_style": "whitegrid"
        }
    }
}

def get_rich_box(box_name):
    if not HAS_RICH:
        return None
    box_map = {
        "ROUNDED": box.ROUNDED,
        "HEAVY": box.HEAVY,
        "DOUBLE": box.DOUBLE,
        "ASCII": box.ASCII,
        "SQUARE": box.SQUARE
    }
    return box_map.get(box_name, box.SQUARE)
