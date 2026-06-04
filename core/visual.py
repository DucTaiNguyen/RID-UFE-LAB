import matplotlib
matplotlib.use("Agg")  # quan trọng: không GUI

import matplotlib.pyplot as plt
import os


def save_plots(prices, entropy_series, exp_path):

    os.makedirs(exp_path, exist_ok=True)

    # ======================
    # PRICE FIGURE
    # ======================
    plt.figure()
    plt.plot(prices)
    plt.title("Bitcoin Price Dynamics")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.tight_layout()
    plt.savefig(f"{exp_path}/price.png")
    plt.close()

    # ======================
    # ENTROPY FIGURE
    # ======================
    plt.figure()
    plt.plot(entropy_series)
    plt.title("Information Entropy Over Time")
    plt.xlabel("Time")
    plt.ylabel("Entropy")
    plt.tight_layout()
    plt.savefig(f"{exp_path}/entropy.png")
    plt.close()

    # ======================
    # SUMMARY
    # ======================
    with open(f"{exp_path}/visual.txt", "w") as f:
        f.write("HEADLESS VISUAL MODE\n")
        f.write(f"price_points={len(prices)}\n")
        f.write(f"entropy_points={len(entropy_series)}\n")
