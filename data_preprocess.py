import pandas as pd

# Replace with your actual Excel file path
file_path = 'data/SNP_result normal.xlsx'
# The column name for which you want to remove duplicates
column_name = 'SNP id'

# Read the Excel file
df = pd.read_excel(file_path)

# Ensure the 'EUR', 'ASW', and 'AFR' columns are treated as floats
df[['EUR', 'ASW', 'AFR']] = df[['EUR', 'ASW', 'AFR']].astype(float)

# Transform values where 'AFR' is greater than 'EUR'
df.loc[df['AFR'] > df['EUR'], ['EUR', 'ASW', 'AFR']] = 1 - df.loc[df['AFR'] > df['EUR'], ['EUR', 'ASW', 'AFR']]

# Remove rows where the difference between 'EUR' and 'AFR' is less than 0.1
df = df[~((df['EUR'] - df['AFR']).abs() <= 0.1)]

# Remove duplicate rows based on 'SNP id' column
df = df.drop_duplicates(subset=[column_name], keep='first')

# Remove rows where 'AFR' is greater than 'ASW'
df = df[~(df['AFR'] >= df['ASW'])]

# Save the modified DataFrame back to Excel
df.to_excel('processed_' + file_path, index=False)
