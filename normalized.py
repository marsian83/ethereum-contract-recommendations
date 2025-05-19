import pandas as pd

filename = "daily-active-eth-address"

# Load the CSV
csv_filename = f"{filename}.csv"
df = pd.read_csv(csv_filename)

# Convert Date column to datetime for proper handling
df["Date(UTC)"] = pd.to_datetime(df["Date(UTC)"])

# Select only numeric columns (excluding Date(UTC))
numeric_cols = df.select_dtypes(include="number").columns

# Subtract the first row's values from all numeric columns
df[numeric_cols] = df[numeric_cols] - df.iloc[0][numeric_cols]

# Save the modified CSV
df.to_csv(f"normalized_{filename}.csv", index=False)

print(f"Normalized data saved in 'normalized_{filename}.csv'")
