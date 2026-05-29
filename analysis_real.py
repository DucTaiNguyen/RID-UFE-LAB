def compute_metrics(data):

    if data["price"] is None:
        return {
            "error": data.get("error", "no data"),
            "score": 0,
            "hypothesis": "DATA_UNAVAILABLE"
        }

    price = data["price"]

    signal = price / 100000
    noise = (price % 1000) / 1000

    score = signal - noise

    hypothesis = (
        "Market shows stable structure"
        if score > 0 else
        "Market instability detected"
    )

    return {
        "price": price,
        "signal": signal,
        "noise": noise,
        "score": score,
        "hypothesis": hypothesis
    }
