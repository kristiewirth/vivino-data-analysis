import pprint as pprint

import pandas as pd
import requests

df = pd.DataFrame(columns=["wine", "rating", "price"])

# Ridiculous number so I can scrape as many pages as possible!
for page_num in range(999999999999999999999999999):
    r = requests.get(
        "https://www.vivino.com/api/explore/explore",
        params={
            "currency_code": "US",
            "min_rating": "1",
            "page": page_num,
            "price_range_max": "200",
            "price_range_min": "1",
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
df.to_csv("vivino-ratings.csv")

##################################################

df['rounded_price'] = round(df['price'], 0)
