import pprint as pprint

import numpy as np
import pandas as pd
import requests
import seaborn as sns
from matplotlib import pyplot
from scipy.optimize import curve_fit

df = pd.DataFrame(columns=["wine", "rating", "price"])

for price_min in np.arange(9, 99, 10):
    for page_num in np.arange(10, 1000, 10):
        r = requests.get(
            "https://www.vivino.com/api/explore/explore",
            params={
                "currency_code": "US",
                "min_rating": "1",
                "page": str(page_num),
                "price_range_max": "100",
                "price_range_min": str(price_min),
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
sns.lineplot(data=df, x="price", y="rating")

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
        diffs.append(round(diff, 2))
    previous = row["rating"]
rounded_ratings_df["increase_in_rating"] = diffs

rounded_ratings_df.drop("rating", axis=1, inplace=True)

# define the true objective function
def objective(x, a, b, c, d, e, f):
    return (a * x) + (b * x ** 2) + (c * x ** 3) + (d * x ** 4) + (e * x ** 5) + f


# choose the input and output variables
x, y = df["price"], df["rating"]
# curve fit
popt, _ = curve_fit(objective, x, y)
# summarize the parameter values
a, b, c, d, e, f = popt
# plot input vs output
pyplot.scatter(x, y, color="pink")
# define a sequence of inputs between the smallest and largest known inputs
x_line = np.arange(min(x), max(x), 1)
# calculate the output for the range
y_line = objective(x_line, a, b, c, d, e, f)
# create a line plot for the mapping function
pyplot.plot(x_line, y_line, "--", color="black")
pyplot.xlabel("Price")
pyplot.ylabel("Rating")
pyplot.title("Comparing ratings of wines vs pricing")
pyplot.savefig('graph_trendline.png',facecolor=fig.get_facecolor(), edgecolor='none')
pyplot.show()


import ruptures as rpt
points = np.array(df["price"])
model = "rbf"
algo = rpt.Pelt(model=model).fit(points)
result = algo.predict(pen=10)
rpt.display(points, result, figsize=(10, 6))
plt.title("Change Point Detection: Pelt Search Method")
plt.show()

