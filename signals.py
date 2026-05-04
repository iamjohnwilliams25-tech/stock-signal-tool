import random
from datetime import datetime

STOCKS = {
    "Power": ["TATA_POWER", "NTPC"],
    "Defence": ["HAL", "BEL"],
    "IT": ["INFY", "TCS"],
    "Energy": ["RELIANCE", "ONGC"],
    "AI": ["COFORGE", "TCS"]
}

def generate_signals():
    results = []

    for sector, stocks in STOCKS.items():
        for stock in stocks:

            buy = round(random.uniform(100, 3000), 2)
            target = round(buy * random.uniform(1.01, 1.05), 2)
            stop_loss = round(buy * 0.97, 2)

            confidence = random.randint(60, 90)

            results.append({
                "stock": stock,
                "sector": sector,
                "buy_price": buy,
                "target": target,
                "stop_loss": stop_loss,
                "confidence": confidence,
                "expected_days": random.randint(1, 5),
                "reason": f"{sector} momentum + volume breakout",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

    return results
