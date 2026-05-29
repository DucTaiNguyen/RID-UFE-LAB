from data_real import fetch_bitcoin_data
from analysis_real import compute_metrics
from paper_real import generate_latex

data = fetch_bitcoin_data()
metrics = compute_metrics(data)

file = generate_latex(metrics)

print("Generated:", file)
