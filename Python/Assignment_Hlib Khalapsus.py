from pathlib import Path
import shutil
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Tasks 1 and 2 — Use of loops and lists 

cities = ["Vienna", "Paris", "London", "Tokyo"]
# We want to calculate the amount of characters in names of each of the cities in this list  
city_lengths = []
for city in cities:
    print(f"City: {city}")
    city_lengths.append(len(city)) 
print("\nLengths of city names:", city_lengths)


# Task 5 - Read hotels-vienna.csv data, fix missing values and boolean-like variables

file_path = Path("hotels-vienna-raw.csv")
df = pd.read_csv(file_path, na_values=["", " ", "NA", "N/A", "na", "null", "None", "-"])
true_vals = {"yes", "y", "true", "t", "1"}
false_vals = {"no", "n", "false", "f", "0"}
# Fix boolean-like variables
for col in df.columns:
    if df[col].dtype == "object":
        s = df[col].astype(str).str.lower().str.strip()
        if s.isin(true_vals | false_vals).mean() > 0.8:
            df[col] = s.map({**{t: True for t in true_vals},
                             **{f: False for f in false_vals}}).astype("boolean")
# Fix missing values
for col in df.columns:
    if pd.api.types.is_numeric_dtype(df[col]):
        df[col] = df[col].fillna(df[col].median())
    elif pd.api.types.is_bool_dtype(df[col]):
        df[col] = df[col].fillna(False)
# Save the data in a new CSV file
df.to_csv("hotels-vienna-clean.csv", index=False)


# Task 6 - Sort the data

df = pd.read_csv("hotels-vienna-clean.csv")
# We keep only the variables that are essential for our analysis
keep_vars = [
    "hotel_id", "country", "city_actual", "distance",
    "price", "city", "stars", "accommodation_type"
]
df = df[keep_vars]
# We only keep the observations that are located in Vienna and are hotels
df = df[df["city_actual"] == "Vienna"]
df = df[df["accommodation_type"] == "Hotel"]
# We only keep 3 and 4 star hotels
df = df[(df["stars"] >= 3) & (df["stars"] <= 4)]
# In addition, we drop the outliers from the data
df = df[(df["price"] < 1000) & (df["distance"] < 8)]
# Safe the sorted data
df.to_csv("hotels-vienna-clean-sorted.csv", index=False)


# Task 8 - Create summary statistics tables
df = pd.read_csv("hotels-vienna-clean-sorted.csv")
summary = (
    df.groupby("stars")["price"]
      .agg(["mean", "median", "min", "max", "std", "count"])
      .assign(skew=df.groupby("stars")["price"].skew())
      .rename(columns={"count": "n"})
      .reset_index()
)
# Export as PNG
fig, ax = plt.subplots(figsize=(8, 2 + 0.4 * len(summary)))
ax.axis("off")
table = ax.table(
    cellText=summary.round(2).values,
    colLabels=summary.columns,
    loc="center"
)
table.auto_set_font_size(False)
table.set_fontsize(10)
plt.title("Summary Statistics: Price by Stars", fontsize=12, weight="bold", pad=10)
plt.tight_layout()
plt.savefig("summary_price_by_stars.png", dpi=300, bbox_inches="tight")
plt.close()


# Task 9 - Create histograms 
df = pd.read_csv("hotels-vienna-clean-sorted.csv")
# Distribution of price
plt.figure(figsize=(8, 5))
plt.hist(df["price"], bins=30, edgecolor="black")
plt.title("Distribution of Hotel Prices in Vienna")
plt.xlabel("Price (EUR)")
plt.ylabel("Number of Hotels")
plt.tight_layout()
plt.savefig("hist_price.png", dpi=300)
plt.close()