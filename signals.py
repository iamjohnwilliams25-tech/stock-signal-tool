import random
from datetime import datetime

def generate_signals():
    stocks = ["RELIANCE", "TATA_POWER", "HAL", "INFY", "TCS"]

    results = []

    for stock in stocks:
        buy = round(random.uniform(100, 3000), 2)
        target = round(buy * 1.02, 2)

        results.append({
            "stock": stock,
            "buy": buy,
            "target": target,
            "confidence": random.randint(60, 85),
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    return results
