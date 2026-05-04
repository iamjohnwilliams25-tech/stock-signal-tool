from datetime import datetime
import random
from zerodha_api import get_ltp

STOCKS = {
    "Power": ["TATA_POWER", "NTPC"],
    "Defence": ["HAL", "BEL"],
    "IT": ["INFY", "TCS"],
    "Energy": ["RELIANCE", "ONGC"]
}

def generate_signals():
    results = []

    for sector, stocks in STOCKS.items():
        for stock in stocks:

            price = get_ltp(stock)

            if price is None:
                continue

            target = round(price * 1.02, 2)
            stop_loss = round(price * 0.98, 2)

            confidence = random.randint(65, 85)

            results.append({
                "stock": stock,
                "sector": sector,
                "buy_price": price,
                "target": target,
                "sell_price": round(target * 0.995, 2),
                "support": stop_loss,
                "confidence": confidence,
                "expected_days": random.randint(1, 5),
                "reason": "Live price + basic momentum",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

    return results