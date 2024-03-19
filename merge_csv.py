import os
import pandas as pd

# Path to the directory containing CSV files
csv_dir = 'data/credit/'

# Get a list of all CSV files in the directory
csv_files = [os.path.join(csv_dir, f) for f in os.listdir(csv_dir) if f.endswith('.csv')]

# Initialize an empty DataFrame to store the merged data
merged_df = pd.DataFrame()

# Iterate over each CSV file and merge its data into the merged DataFrame
for file in csv_files:
    # Read CSV file into DataFrame
    df = pd.read_csv(file)
    # Merge DataFrame with existing merged_df based on date column
    merged_df = pd.merge(merged_df, df, on='date', how='outer')

# Export the merged DataFrame to a new CSV file
merged_df.to_csv('merged.csv', index=False)
