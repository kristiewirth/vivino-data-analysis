import pprint as pprint

import pandas as pd
import requests
import seaborn as sns
import numpy as np

df = pd.DataFrame(columns=["wine", "rating", "price"])

r = requests.get(
    "https://www.vivino.com/api/explore/explore",
    params={
        "currency_code": "US",
        "min_rating": "1",
        "page": 1,
        "price_range_max": "100",
        "price_range_min": "9",
        "order_by": "price",
        "order": "asc",
    },
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"
    },
)

for record in r.json()["explore_vintage"]["matches"]:
    try:
        wine = record["vintage"]["name"]
        rating = record["vintage"]["statistics"]["ratings_average"]
        price = record["price"]["amount"]
        df = df.append(
            pd.DataFrame(
                [[wine, rating, price]], columns=["wine", "rating", "price"]
            )
        )
    except Exception:
        pass

df.reset_index(inplace=True, drop=True)
df.sort_values(by="price", ascending=True, inplace=True)
df.to_csv("vivino-ratings.csv")

############################################################

df = pd.read_csv("vivino-ratings.csv")

# Graphing
sns.regplot(data=df, x="price", y="rating")

# Making summary df
df["rounded_price"] = 5 * round(df["price"].astype("int") / 5)
rounded_ratings_df = (
    pd.DataFrame(df.groupby("rounded_price")["rating"].mean())
    .sort_values(by="rounded_price", ascending=True)
    .reset_index(drop=False)
)
rounded_ratings_df["rounded_rating"] = round(rounded_ratings_df["rating"], 2)

# Calculating increases in ratings over time
previous = 0
diffs = []
for i, row in rounded_ratings_df.iterrows():
    if previous == 0:
        diffs.append(0)
    else:
        diff = row["rating"] - previous
        diffs.append(diff)
    previous = row["rating"]
rounded_ratings_df["increase_in_rating"] = diffs

rounded_ratings_df.drop("rating", axis=1, inplace=True)