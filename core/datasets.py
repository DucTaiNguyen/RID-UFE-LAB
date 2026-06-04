import numpy as np

def get_datasets():

    np.random.seed(42)

    btc = np.cumsum(np.random.normal(0, 1, 400))
    eth = np.cumsum(np.random.normal(0, 1.1, 400))
    gold = np.cumsum(np.random.normal(0, 0.5, 400))

    noise = np.random.normal(0, 1, 400)

    return {
        "BTC": btc,
        "ETH": eth,
        "GOLD": gold,
        "NOISE": noise
    }
