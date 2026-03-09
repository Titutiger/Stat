import src.stat as stat
import numpy as np

# ---------------------------------------------------------
# Case 1: Server Reliability (Exponential & Poisson)
# ---------------------------------------------------------
# A server has an average uptime of 1000 hours between crashes.
# Mean = 1/lam = 1000  => lam = 0.001 (crashes per hour)

uptime_model = stat.Exponential(lam=0.001)

# What is the probability it lasts *at least* 1500 hours?
# P(X > 1500) = 1 - CDF(1500)
prob_long_uptime = 1 - uptime_model.cdf(1500)
print(f"Prob(Uptime > 1500 hrs): {prob_long_uptime * 100:.2f}%")

# Now, we model crashes per day (24 hours). 
# lam_day = 0.001 * 24 = 0.024 crashes/day.
crash_counts = stat.Poisson(lam=0.024)

# What is the chance of NO crashes in a 24-hour period?
# P(X = 0)
prob_no_crashes = crash_counts.pmf(0)
print(f"Prob(No crashes today): {prob_no_crashes * 100:.2f}%")

# ---------------------------------------------------------
# Case 2: Marketing Conversion (Geometric)
# ---------------------------------------------------------
# A sales team knows that 5% of cold calls result in a meeting.
# p = 0.05

meeting_model = stat.Geometric(p=0.05)

# On average, how many calls until the first meeting?
print(f"Avg calls for first success: {meeting_model.mean():.1f}")

# What is the probability it takes more than 50 calls to get the first meeting?
# P(X > 50) = 1 - CDF(50)
prob_high_effort = 1 - meeting_model.cdf(50)
print(f"Prob(Need > 50 calls): {prob_high_effort * 100:.2f}%")

# ---------------------------------------------------------
# Case 3: Quality Control (Negative Binomial)
# ---------------------------------------------------------
# A factory produces circuit boards with a 10% defect rate. 
# They need 3 defective boards to analyze for root cause.
# p = 0.1, r = 3

defect_model = stat.NegativeBinomial(r=3, p=0.1)

# What is the probability of seeing exactly 10 FAILURES (good boards) 
# before the 3rd defective one?
prob_10_failures = defect_model.pmf(10)
print(f"Prob(10 good boards before 3rd defect): {prob_10_failures * 100:.2f}%")
