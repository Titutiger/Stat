import pandas as pd
import src.stat as stat
from src.stat.prob import Prob

# ==============================================================================
# PART 1: INGESTION & DESCRIPTIVE STATISTICS
# ==============================================================================

# We receive raw sensor data from the manufacturing floor for 1,000 batteries.
# (Simulating a small sample of the dataset here for readability)
manufacturing_data = pd.DataFrame({
    'Battery_Life_Hours': [48.2, 50.1, 45.5, 49.8, 51.2, 47.9, 46.5, 50.5, 48.8, 49.1],
    'Factory_Temp_C':     [22.1, 21.8, 24.5, 22.0, 21.5, 23.1, 23.8, 21.9, 22.4, 22.2],
    'Humidity_Pct':       [45.0, 44.2, 55.1, 46.0, 43.5, 50.2, 52.0, 44.8, 46.5, 45.8],
    'Machine_ID':         ['M1', 'M1', 'M2', 'M1', 'M1', 'M2', 'M2', 'M1', 'M1', 'M1']
})



# 1. Convert the raw data into a Stat object
# Note: It will automatically ignore the string column ('Machine_ID')!
batch_stats = stat.represent(manufacturing_data)

batch_stats.show()

print("--- BATCH SUMMARY ---")
# Get a bird's-eye view of the manufacturing consistency
print(batch_stats.summary())

# Specifically isolate the mean and standard deviation of the battery life
mean_life = batch_stats.mean(series='Battery_Life_Hours')
std_life = batch_stats.std(sample=True, series='Battery_Life_Hours')

print(f"\nAverage Battery Life: {mean_life:.2f} hours")
print(f"Standard Deviation: {std_life:.2f} hours")


# ==============================================================================
# PART 2: CORRELATION & ROOT CAUSE ANALYSIS
# ==============================================================================

# Is the factory temperature causing the batteries to degrade?
# We use the correlation matrix to find relationships between variables.


print("\n--- FACTORY CONDITION CORRELATIONS ---")
corr_matrix = batch_stats.corr(method='pearson')
print(corr_matrix)
# Insight: If the correlation between Factory_Temp_C and Battery_Life_Hours
# is highly negative (e.g., -0.85), we can definitively tell the engineering
# team that a hotter factory floor produces worse batteries.


# ==============================================================================
# PART 3: PROBABILITY DISTRIBUTIONS & WARRANTY FORECASTING
# ==============================================================================

# The finance department wants to offer a "Guaranteed Battery Life" warranty.
# If a battery fails before the warranty time, we replace it for free.
# We only want to replace a maximum of 1% of batteries to stay profitable.

# 1. We model the battery life as a Normal Distribution using our sample stats
battery_model = stat.Normal(mu=mean_life, sigma=std_life)

# 2. We use the PPF (Inverse CDF) to find the exact hour mark corresponding
# to the bottom 1% (0.01) of the distribution.

warranty_cutoff = battery_model.ppf(0.01)

print("\n--- WARRANTY CALCULATION ---")
print(f"To ensure only 1% replacements, set the warranty at: {warranty_cutoff:.2f} hours")

# 3. A customer complains that their watch only lasted 44 hours.
# What was the probability of getting a watch this bad or worse?
prob_bad_watch = battery_model.cdf(44.0)
print(f"Probability of a battery lasting <= 44 hours: {prob_bad_watch * 100:.2f}%")


# ==============================================================================
# PART 4: DISCRETE RISK MODELING (SHIPPING)
# ==============================================================================

# We are shipping a massive pallet of 5,000 smartwatches.
# Historically, the defect rate across the entire supply chain is 0.5% (p = 0.005).
# The buyer will reject the entire shipment if there are more than 35 defective units.

# 1. We model this discrete scenario using the Binomial distribution
shipment_model = stat.Binomial(n=5000, p=0.005)

# 2. We use the CDF to find the probability of having 35 OR FEWER defects.
# If P(X <= 35) is very high, the shipment is safe.
prob_safe_shipment = shipment_model.cdf(35)

print("\n--- LOGISTICS RISK ---")
print(f"Probability the buyer accepts the shipment: {prob_safe_shipment * 100:.2f}%")


# ==============================================================================
# PART 5: BUSINESS DECISION via EXPECTED VALUE
# ==============================================================================

# To fix the factory temperature issue, the engineering team proposes a $50,000
# HVAC upgrade. We model the financial outcomes of this upgrade over the next year:
# - 60% chance it perfectly stabilizes temp: Saves $120,000 in defect costs.
# - 30% chance it moderately helps: Saves $40,000.
# - 10% chance it does nothing: Saves $0.

outcomes = [120_000, 40_000, 0]
probabilities = [0.60, 0.30, 0.10]

# Calculate the expected savings of the HVAC system
expected_savings = Prob.expected_value(outcomes, probabilities)
net_roi = expected_savings - 50_000

print("\n--- BUSINESS DECISION: HVAC UPGRADE ---")
print(f"Expected Savings: ${expected_savings:,.2f}")
print(f"Net ROI (Subtracting $50k cost): ${net_roi:,.2f}")

if net_roi > 0:
    print("Conclusion: Approve the HVAC upgrade.")
else:
    print("Conclusion: Reject the HVAC upgrade.")