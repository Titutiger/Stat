import src.stat as stat

import pandas as pd


pd_df = pd.read_csv('assets/medical_trials.csv')

df = stat.represent(pd_df)


print(df)