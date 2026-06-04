import yfinance as yf
import numpy as np

def load_asset(
    ticker="BTC-USD",
    period="1y"
):
    df = yf.download(
        ticker,
        period=period,
        auto_adjust=True,
        progress=False
    )

    close = df["Close"]

    prices = np.asarray(close).reshape(-1)

    return prices.astype(float)
