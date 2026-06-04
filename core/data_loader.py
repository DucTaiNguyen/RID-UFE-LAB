import yfinance as yf

def load_btc():
    df = yf.download("BTC-USD", period="6mo", interval="1d")
    return df["Close"].values
