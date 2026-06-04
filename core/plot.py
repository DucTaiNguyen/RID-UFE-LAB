import matplotlib.pyplot as plt

def plot_prices(prices):
    plt.plot(prices)
    plt.title("BTC Price")
    plt.show()

def plot_metrics(score):
    plt.bar(score.keys(), score.values())
    plt.title("RIFT Metrics")
    plt.show()
