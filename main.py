import pandas as pd
import plotly.express as px
import json


do = [1,2,3,4,5,6,7]


if 1 in do:
    input("Show unique addresses")
    
    csv_filename = "normalized_address-count.csv"  
    df = pd.read_csv(csv_filename)

    df["Date(UTC)"] = pd.to_datetime(df["Date(UTC)"])


    df["Daily Change"] = df["Value"].diff()


    df.to_csv("logged_changes.csv", index=False)


    fig1 = px.line(df, x="Date(UTC)", y="Value", title="Value Over Time",
                markers=True, labels={"Value": "Total Value", "Date(UTC)": "Date"},
                hover_data={"Date(UTC)": "|%Y-%m-%d", "Value": ":,"})


    fig2 = px.line(df, x="Date(UTC)", y="Daily Change", title="Daily Change in Value",
                markers=True, labels={"Daily Change": "users", "Date(UTC)": "Date"},
                hover_data={"Date(UTC)": "|%Y-%m-%d", "Daily Change": ":,"})


    fig1.show()
    fig2.show()



if 2 in do:
    input("Show daily active users")

    csv_filename = "daily-active-eth-address.csv"
    df = pd.read_csv(csv_filename)

    
    df["Date(UTC)"] = pd.to_datetime(df["Date(UTC)"])

    
    df["Total Active Users"] = df["Unique Address Total Count"]
    df["Receive"] = df["Unique Address Receive Count"]
    df["Sent"] = df["Unique Address Sent Count"]

    
    df_melted = df.melt(id_vars=["Date(UTC)"], 
                        value_vars=["Total Active Users", "Receive", "Sent"],
                        var_name="Metric", 
                        value_name="Value")

    
    fig = px.line(df_melted, x="Date(UTC)", y="Value", color="Metric", 
                title="Daily Unique User Addresses",
                markers=True, labels={"Value": "tokens", "Date(UTC)": "Date"},
                hover_data={"Date(UTC)": "|%Y-%m-%d", "Value": ":,"})

    fig.show()


if 3 in do:
    input("Show daily tokens (coins)")

    csv_filename = "daily-active-token-address.csv"
    df = pd.read_csv(csv_filename)

    
    df["Date(UTC)"] = pd.to_datetime(df["Date(UTC)"])

    
    df["Total Tokens interacted with"] = df["Unique Address Total Count"]

    
    df_melted = df.melt(id_vars=["Date(UTC)"], 
                        value_vars=["Total Tokens interacted with"],
                        var_name="Metric", 
                        value_name="Value")

    
    fig = px.line(df_melted, x="Date(UTC)", y="Value", color="Metric", 
                title="Daily Active Token Addresses",
                markers=True, labels={"Value": "Daily Change", "Date(UTC)": "Date"},
                hover_data={"Date(UTC)": "|%Y-%m-%d", "Value": ":,"})

    fig.show()


if 4 in do:
    input("New Contracts")

    csv_filename = "deployed-contracts.csv"
    df = pd.read_csv(csv_filename)

    
    df["Date(UTC)"] = pd.to_datetime(df["Date(UTC)"])

    
    df["contracts"] = df["No. of Deployed Contracts"]

    
    df["Total Count"] = df["contracts"].fillna(0).cumsum()

    
    df_melted = df.melt(id_vars=["Date(UTC)"], 
                        value_vars=["contracts", "Total Count"],
                        var_name="Metric", 
                        value_name="Value")

    
    fig = px.line(df_melted, x="Date(UTC)", y="Value", color="Metric", 
                title="Daily and Total Deployed Contracts",
                markers=True, labels={"Value": "Contracts", "Date(UTC)": "Date"},
                hover_data={"Date(UTC)": "|%Y-%m-%d", "Value": ":,"})

    fig.show()



if 5 in do:
    input("Exchange transactions")

    csv_filename = "exchange-txns.csv"
    df = pd.read_csv(csv_filename)

    
    df["Date(UTC)"] = pd.to_datetime(df["Date(UTC)"])

    
    df["txns"] = df["Value"]

    
    df_melted = df.melt(id_vars=["Date(UTC)"], 
                        value_vars=["txns"],
                        var_name="Metric", 
                        value_name="Txn Count")

    
    fig = px.line(df_melted, x="Date(UTC)", y="Txn Count", color="Metric", 
                title="Daily Exchange Txns",
                markers=True, labels={"Txn Count": "txns", "Date(UTC)": "Date"},
                hover_data={"Date(UTC)": "|%Y-%m-%d", "Txn Count": ":,"})

    fig.show()


if 6 in do:
    input("Token Transactions (Total / not unique)")

    csv_filename = "token-txns.csv"
    df = pd.read_csv(csv_filename)

    
    df["Date(UTC)"] = pd.to_datetime(df["Date(UTC)"])

    
    df["txns"] = df["Transactions"]

    
    df["Total txns"] = df["txns"].fillna(0).cumsum()

    
    df_melted = df.melt(id_vars=["Date(UTC)"], 
                        value_vars=["txns", "Total txns"],
                        var_name="Metric", 
                        value_name="Value")

    
    fig = px.line(df_melted, x="Date(UTC)", y="Value", color="Metric", 
                title="Total (non unique) Transactions marked 'Token'",
                markers=True, labels={"Value": "Contracts", "Date(UTC)": "Date"},
                hover_data={"Date(UTC)": "|%Y-%m-%d", "Value": ":,"})

    fig.show()


if 7 in do:
    input("Transactions")

    csv_filename = "tx-growth.csv"
    df = pd.read_csv(csv_filename)

    
    df["Date(UTC)"] = pd.to_datetime(df["Date(UTC)"])

    
    df["txns"] = df["Transactions"]

    
    df["Total txns"] = df["txns"].fillna(0).cumsum()

    
    df_melted = df.melt(id_vars=["Date(UTC)"], 
                        value_vars=["txns", "Total txns"],
                        var_name="Metric", 
                        value_name="Value")

    
    fig = px.line(df_melted, x="Date(UTC)", y="Value", color="Metric", 
                title="Total Transactions Daily",
                markers=True, labels={"Value": "Contracts", "Date(UTC)": "Date"},
                hover_data={"Date(UTC)": "|%Y-%m-%d", "Value": ":,"})

    fig.show()



input("Show top stats / actors")
with open('most.json', 'r') as file:
    data = json.load(file)

print(json.dumps(data, indent=4))

