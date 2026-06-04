from core.loop import run_loop

def evaluate_all(datasets):

    results = {}

    for name, series in datasets.items():

        history = run_loop(series, iterations=5)

        acc = sum(h["accepted"] for h in history) / len(history)

        results[name] = acc

    return results
