import pandas as pd
import plotly.express as px

# Load the data
csv_filename = "normalized_address-count.csv"  # Change this if needed
df = pd.read_csv(csv_filename)

# Convert Date column to datetime
df["Date(UTC)"] = pd.to_datetime(df["Date(UTC)"])

# Calculate daily changes
df["Daily Change"] = df["Value"].diff()

# Log daily changes to a new CSV
df.to_csv("logged_changes.csv", index=False)

# Plot the values over time
fig1 = px.line(df, x="Date(UTC)", y="Value", title="Value Over Time",
               markers=True, labels={"Value": "Total Value", "Date(UTC)": "Date"},
               hover_data={"Date(UTC)": "|%Y-%m-%d", "Value": ":,"})

# Plot daily changes
fig2 = px.line(df, x="Date(UTC)", y="Daily Change", title="Daily Change in Value",
               markers=True, labels={"Daily Change": "Change", "Date(UTC)": "Date"},
               hover_data={"Date(UTC)": "|%Y-%m-%d", "Daily Change": ":,"})

# Show the interactive graphs
fig1.show()
fig2.show()

print("Daily changes logged in 'logged_changes.csv'")
