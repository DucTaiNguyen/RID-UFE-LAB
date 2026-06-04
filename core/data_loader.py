import requests
import numpy as np

def load_asset():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"

    params = {
        "vs_currency": "usd",
        "days": "1"
    }

    try:
        r = requests.get(url, params=params, timeout=10)
        data = r.json()

        prices = [p[1] for p in data["prices"]]

        return np.array(prices)

    except Exception as e:
        print("DATA LOAD ERROR:", e)

        # fallback (để system không crash)
        return np.array([70000.0])
