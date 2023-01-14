import pandas as pd

MAX_MEDIAN_TIME_ON_MARKET = 45
MAX_MEDIAN_PRICE = 650000
MIN_INTERESTED_BUYERS = 500

# Load the CSV file
df = pd.read_csv("data/stats_house_buy_all.csv")

# Filter median_time_on_market < 60 days
# Replace the string "days" with an empty string in the "column_name" column
df["median_time_on_market"] = df["median_time_on_market"].str.replace(" days ", "")
df["median_time_on_market"] = pd.to_numeric(df["median_time_on_market"], errors="coerce")
df = df.dropna()
df = df[df["median_time_on_market"] < MAX_MEDIAN_TIME_ON_MARKET]

# Filter Median__price < 700000
df["Median__price"] = df["Median__price"].str.replace("$", "")
df["Median__price"] = df["Median__price"].str.replace(",","")
df["Median__price"] = pd.to_numeric(df["Median__price"], errors="coerce")
df = df.dropna()
df = df[df["Median__price"] <= MAX_MEDIAN_PRICE]

# Interested Buyers > 1000
df["interested"] = df["interested"].str.replace(" buyers ", "")
df["interested"] = pd.to_numeric(df["interested"], errors="coerce")
df = df.dropna()
filtered_df = df[df["interested"] > MIN_INTERESTED_BUYERS]

# Print the resulting DataFrame
print(filtered_df.sort_values(by="Median__price",ascending=True))
filtered_df.sort_values(by="Median__price",ascending=True).to_csv('output.csv')