from __future__ import annotations

import numpy as np
import requests


COINGECKO_URL = (
    "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
)

MIN_PRICE_SAMPLES = 100


class DataLoadError(RuntimeError):
    """Raised when market data cannot be loaded or validated."""


def _validate_prices(prices: np.ndarray) -> np.ndarray:
    prices = np.asarray(prices, dtype=float).reshape(-1)
    prices = prices[np.isfinite(prices)]

    if len(prices) < MIN_PRICE_SAMPLES:
        raise DataLoadError(
            f"Insufficient price data: {len(prices)} samples "
            f"(minimum required: {MIN_PRICE_SAMPLES})."
        )

    if np.any(prices <= 0):
        raise DataLoadError(
            "Price series contains non-positive values."
        )

    if np.std(prices) == 0:
        raise DataLoadError(
            "Degenerate price series: all prices are identical."
        )

    return prices


def load_asset(
    days: int = 1,
    vs_currency: str = "usd",
    timeout: int = 30,
) -> np.ndarray:

    params = {
        "vs_currency": vs_currency,
        "days": days,
    }

    try:
        response = requests.get(
            COINGECKO_URL,
            params=params,
            timeout=timeout,
        )

        response.raise_for_status()
        payload = response.json()

    except requests.RequestException as exc:
        raise DataLoadError(
            f"CoinGecko request failed: {exc}"
        ) from exc

    except ValueError as exc:
        raise DataLoadError(
            "CoinGecko returned invalid JSON."
        ) from exc

    if not isinstance(payload, dict):
        raise DataLoadError(
            "Unexpected CoinGecko response format."
        )

    raw_prices = payload.get("prices")

    if not raw_prices:
        raise DataLoadError(
            "CoinGecko response does not contain price data."
        )

    try:
        prices = np.array(
            [float(item[1]) for item in raw_prices],
            dtype=float,
        )

    except (TypeError, ValueError, IndexError) as exc:
        raise DataLoadError(
            "Unable to parse CoinGecko price data."
        ) from exc

    return _validate_prices(prices)
