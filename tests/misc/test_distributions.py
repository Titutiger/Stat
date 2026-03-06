import pandas as pd
import src.stat as stat


# The textbook example you provided
marks_data = {
    "10-20": 3,
    "20-30": 2,
    "30-40": 4
}

# Pass it to the unpacker
grouped_stats = stat.from_grouped(marks_data)
# chagnge the __init__()s

print(grouped_stats)
# Output: Stat(tag='ordered', data=[15. 15. 15. 25. 25. 35. 35. 35. 35.])

# Now all your math works perfectly!
print(f"Mean: {grouped_stats.mean()}")
# Output: Mean: 26.11111111111111