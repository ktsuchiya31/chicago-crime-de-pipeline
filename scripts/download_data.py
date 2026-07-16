import requests
import pandas as pd
import os

url = "https://data.cityofchicago.org/resource/ijzp-q8t2.json"

params = {
    "$where": "year >= 2020",
    "$limit": 100000,
    "$order": "date DESC"
}

response = requests.get(url, params=params)
data = response.json()

df = pd.DataFrame(data)
print(df.shape)
print(df.dtypes)
print(df.head())

os.makedirs("include", exist_ok=True)
df.to_csv("include/chicago_crimes.csv", index=False)
print("saved to include/chicago_crimes.csv")