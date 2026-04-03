import pandas as pd

data = [
    # Core Operations (Descriptive)
    {"name": "mean", "description": "Calculates arithmetic, geometric, or harmonic mean of the data."},
    {"name": "median", "description": "Calculates the median (50th percentile) of the dataset."},
    {"name": "mode", "description": "Calculates the most frequent value in the dataset."},
    {"name": "variance", "description": "Calculates the variance (sample or population) of the data."},
    {"name": "std", "description": "Calculates the standard deviation of the data."},
    {"name": "mad", "description": "Calculates the Mean Absolute Deviation (MAD) from the median."},
    {"name": "percentile", "description": "Calculates the q-th percentile of the data (0-100)."},
    {"name": "quantile", "description": "Calculates the q-th quantile of the data (0.0-1.0)."},
    {"name": "iqr", "description": "Calculates the Interquartile Range (IQR)."},
    {"name": "sem", "description": "Calculates the Standard Error of the Mean (SEM)."},
    {"name": "corr", "description": "Calculates the correlation matrix between columns (Pearson, Kendall, Spearman)."},
    {"name": "frequencies", "description": "Returns counts of unique values in a categorical column."},
    {"name": "groupby", "description": "Groups data by a categorical column and performs statistical operations."},
    {"name": "skewness", "description": "Calculates the skewness (asymmetry) of the dataset."},
    {"name": "kurtosis", "description": "Calculates the excess kurtosis (tailedness) of the dataset."},
    {"name": "min", "description": "Returns the minimum value in the dataset."},
    {"name": "max", "description": "Returns the maximum value in the dataset."},
    {"name": "range", "description": "Calculates the range (max - min) of the dataset."},
    {"name": "summary", "description": "Generates a comprehensive statistical breakdown of all columns."},
    {"name": "show", "description": "Displays data using beautiful themed Rich tables in the terminal."},
    {"name": "plot", "description": "Displays graphs using Matplotlib/Seaborn with theme support."},

    # Inferential Statistics
    {"name": "t_test", "description": "Performs one-sample, two-sample, or paired T-tests."},
    {"name": "z_test", "description": "Performs a one-sample Z-test."},
    {"name": "anova", "description": "Performs a one-way ANOVA across multiple groups."},
    {"name": "chisquare", "description": "Performs Chi-Square Goodness of Fit test."},

    # Probability Functions (Prob class)
    {"name": "Prob.combinations", "description": "Calculates nCr (combinations)."},
    {"name": "Prob.permutations", "description": "Calculates nPr (permutations)."},
    {"name": "Prob.bayes", "description": "Calculates conditional probability using Bayes' Theorem."},
    {"name": "Prob.expected_value", "description": "Calculates the expected value of a discrete random variable."},
    {"name": "Prob.binomial_pmf", "description": "Calculates the exact PMF for a Binomial distribution."},

    # Workflows
    {"name": "standard_eda", "description": "Automated EDA pipeline (summary, correlations, warnings)."},
    {"name": "remove_outliers", "description": "Detects and removes outliers using the IQR method."},

    # Symbolic Utilities
    {"name": "EquationSolver.solve", "description": "Symbolically solves algebraic equations for a missing variable."},

    # Distributions (Common methods)
    {"name": "pdf", "description": "Probability Density Function for continuous distributions."},
    {"name": "pmf", "description": "Probability Mass Function for discrete distributions."},
    {"name": "cdf", "description": "Cumulative Distribution Function (P(X <= x))."},
    {"name": "ppf", "description": "Percent Point Function (Inverse CDF)."},
    {"name": "rvs", "description": "Generates random samples from a distribution."},
    {"name": "entropy", "description": "Calculates the differential entropy of a distribution."}
]

df_functions = pd.DataFrame(data)