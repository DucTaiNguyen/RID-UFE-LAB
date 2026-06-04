from core.data_loader import load_btc
from core.rift_score import compute_rift
from core.plot import plot_metrics

def run():
    prices = load_btc()
    score = compute_rift(prices)

    print(score)
    plot_metrics(score)

if __name__ == "__main__":
    run()
