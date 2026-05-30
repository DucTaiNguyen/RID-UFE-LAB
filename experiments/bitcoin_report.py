import math

price = 73970.0

log_price = math.log(price)

with open("results.txt", "w") as f:
    f.write(f"Bitcoin Price: {price}\n")
    f.write(f"Log Price: {log_price:.4f}\n")

print("Report generated")
