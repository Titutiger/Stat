# src/stat/utils/parsers.py
import src.stat.core as core


def from_grouped(frequency_dict: dict):
    """
    Expands grouped frequency data (e.g., {"10-20": 3}) into a Stat object.
    """
    unpacked_data = []

    for class_range, frequency in frequency_dict.items():
        # Split "10-20" into 10 and 20
        lower, upper = class_range.split('-')
        midpoint = (float(lower) + float(upper)) / 2.0

        # Add midpoint 'frequency' times
        unpacked_data.extend([midpoint] * frequency)

    # Return via the core factory function
    return core.represent(unpacked_data)