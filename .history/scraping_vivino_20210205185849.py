import requests
import pandas as pd

r = requests.get(
    "https://www.vivino.com/api/explore/explore",
    params={
        "currency_code": "US",
        "min_rating": "1",
        "page": 1,
        "price_range_max": "500",
        "price_range_min": "0",
    },
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"
    },
)

for record in r.json()["explore_vintage"]["matches"]:
    name = record["vintage"]["wine"]["winery"]["name"]

results = [
    (
        t["vintage"]["wine"]["winery"]["name"],
        f'{t["vintage"]["wine"]["name"]} {t["vintage"]["year"]}',
        t["vintage"]["statistics"]["ratings_average"],
        t["vintage"]["statistics"]["ratings_count"],
    )
    for t in r.json()["explore_vintage"]["matches"]
]
dataframe = pd.DataFrame(results, columns=["Winery", "Wine", "Rating", "num_review"])

print(dataframe)
