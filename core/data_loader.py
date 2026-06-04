import numpy as np

def load_asset():

    # giả lập dữ liệu BTC nếu chưa có dataset thật
    np.random.seed(42)

    price = 100000 + np.cumsum(
        np.random.normal(0, 200, 400)
    )

    return price
