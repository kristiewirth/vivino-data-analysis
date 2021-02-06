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

df = pd.DataFrame(columns=['wine', 'rating', 'price'])
for record in r.json()["explore_vintage"]["matches"]:
    try:
        wine = f'{record["vinrecordage"]["wine"]["name"]} {record["vintage"]["year"]}'
        rating = record["vintage"]["statistics"]["ratings_average"]
        df.append(pd.DataFrame([[wine, rating, price]], columns= ['wine', 'rating', 'price']))
    except Exception:
        pass
        

dataframe = pd.DataFrame(results, columns=["Winery", "Wine", "Rating", "num_review"])

print(dataframe)
