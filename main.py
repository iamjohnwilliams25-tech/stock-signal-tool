from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from zerodha_api import get_ltp, is_market_open

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- SIGNALS ----------------
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

        # ❗ If even cache is empty, skip
        if price is None:
            continue

        results.append({
            "stock": stock,
            "sector": sector,
            "buy_price": price,
            "target": round(price * 1.02, 2),
            "stop_loss": round(price * 0.98, 2),
            "market_status": "LIVE" if is_market_open() else "CLOSED (CACHED)",
        })

    return results


@app.get("/price/{symbol}")
def price(symbol: str):

    price = get_ltp(symbol)

    return {
        "symbol": symbol,
        "price": price,
        "market_open": is_market_open()
    }
