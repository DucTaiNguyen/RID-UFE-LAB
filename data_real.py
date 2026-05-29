import requests

def fetch_bitcoin_data():

    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()

        data = r.json()

        price = float(data["price"])

        return {
            "price": price,
            "source": "binance"
        }

    except Exception as e:
        return {
            "price": None,
            "error": str(e),
            "source": "binance_failed"
        }
