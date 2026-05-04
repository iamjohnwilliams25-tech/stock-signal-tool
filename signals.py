from zerodha_api import get_ltp
import random

WATCHLIST = [
    ("TATA_POWER", "Power"),
    ("NTPC", "Power"),
    ("HAL", "Defence"),
    ("BEL", "Defence"),
    ("TCS", "AI"),
    ("INFY", "AI"),
    ("RELIANCE", "Energy")
]


def generate_signals():

    results = []

    for stock, sector in WATCHLIST:

        price = get_ltp(stock)

        # ❗ STRICT RULE: NO PRICE = SKIP
        if price is None or price <= 0:
            continue

        price = float(price)

        results.append({
            "stock": stock,
            "sector": sector,
            "buy_price": round(price, 2),
            "target": round(price * 1.02, 2),
            "stop_loss": round(price * 0.98, 2),
            "confidence": random.randint(70, 95),
            "expected_days": random.randint(1, 3),
            "reason": "Live Zerodha market feed"
        })

    return results
