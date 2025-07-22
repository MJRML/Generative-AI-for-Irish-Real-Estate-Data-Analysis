import pandas as pd
df = pd.read_csv('data/daft_housing_data.csv')

print(df["Number of Bedrooms"].unique())