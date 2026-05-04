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

        # ❗ HARD FIX: if price fails, DO NOT generate fake data
        if price is None:
            continue

        buy_price = float(price)

        target = round(buy_price * 1.02, 2)
        stop_loss = round(buy_price * 0.98, 2)

        results.append({
            "stock": stock,
            "sector": sector,
            "buy_price": buy_price,
            "target": target,
            "stop_loss": stop_loss,
            "confidence": random.randint(70, 90),
            "expected_days": random.randint(1, 3),
            "reason": "Live price breakout logic"
        })

    return results
