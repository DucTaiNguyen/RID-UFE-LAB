import numpy as np

np.random.seed(42)

prices = np.cumsum(np.random.randn(200) * 10 + 30000)

returns = np.diff(np.log(prices))

window = 10
volatility = np.array([
    np.std(returns[i-window:i])
    for i in range(window, len(returns))
])

future_returns = np.abs(returns[window:])

corr = np.corrcoef(volatility, future_returns)[0, 1]

with open("results.txt", "w") as f:
    f.write(f"correlation={corr}\n")

print("DONE:", corr)
