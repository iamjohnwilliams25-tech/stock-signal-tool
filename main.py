from fastapi import FastAPI
from zerodha_api import get_ltp, is_market_open

app = FastAPI()


@app.get("/signals")
def signals():

    stocks = [
        ("TATA_POWER", "Power"),
        ("NTPC", "Power"),
        ("HAL", "Defence"),
        ("BEL", "Defence"),
        ("TCS", "AI"),
        ("INFY", "AI"),
        ("RELIANCE", "Energy")
    ]

    results = []

    for stock, sector in stocks:

        price = get_ltp(stock)

        results.append({
            "stock": stock,
            "sector": sector,
            "buy_price": price if price else "WAITING TOKEN",
            "target": (round(price * 1.02, 2) if price else "WAIT"),
            "stop_loss": (round(price * 0.98, 2) if price else "WAIT"),
            "status": "LIVE" if price else "NO TOKEN / NO DATA"
        })

    return results
