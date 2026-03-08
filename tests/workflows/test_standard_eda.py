import pandas as pd
import src.stat as stat

# Create our test data
test_data = pd.DataFrame({
    # A normal, symmetrical distribution of test scores
    'Normal_Scores': [50, 52, 48, 51, 49, 50, 53, 47, 51, 49],

    # Salaries at a startup: 9 regular employees and 1 CEO making $2.5M
    'Startup_Salaries': [60_000, 65_000, 62_000, 58_000, 61_000, 59_000, 63_000, 60_000, 64_000, 2_500_000]
})

# Run your powerful one-liner workflow!
print("Running Automated EDA Workflow...\n")
report = stat.standard_eda(test_data)

# Display the automated insights
print(f"📊 Data Dimensions: {report['Dimensions']}")
print("-" * 45)
print("🚨 AUTOMATED WARNINGS:")

# Format the warnings nicely
if isinstance(report['Automated_Warnings'], dict):
    for col, warning in report['Automated_Warnings'].items():
        print(f"   ⚠️ {col}: {warning}")
else:
    print(f"   ✅ {report['Automated_Warnings']}")

print("-" * 45)
print("\n📝 FULL SUMMARY (Key Metrics):")
# We will just print a few specific columns so it fits nicely in the terminal
print(report['Summary'][['mean', 'median', 'std', 'skewness', 'kurtosis']])