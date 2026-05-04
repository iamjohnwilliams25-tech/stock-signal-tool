from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from zerodha_api import get_ltp, generate_token

app = FastAPI()

# ---------------- CORS (WORDPRESS FIX) ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- HOME ----------------
@app.get("/")
def home():
    return {"status": "API Running"}

# ---------------- SET TOKEN (IMPORTANT FIX) ----------------
@app.get("/set-token/{token}")
def set_token(token: str):
    os.environ["ACCESS_TOKEN"] = token
    return {"status": "TOKEN SET SUCCESSFULLY"}

# ---------------- PRICE CHECK ----------------
@app.get("/price/{symbol}")
def price(symbol: str):

    price = get_ltp(symbol)

    return {
        "symbol": symbol,
        "price": price,
        "status": "LIVE" if price else "NO TOKEN / NO DATA"
    }

# ---------------- SIGNALS (NO BLANK EVER) ----------------
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

        if price:
            results.append({
                "stock": stock,
                "sector": sector,
                "buy_price": price,
                "target": round(price * 1.02, 2),
                "stop_loss": round(price * 0.98, 2),
                "status": "LIVE"
            })
        else:
            results.append({
                "stock": stock,
                "sector": sector,
                "buy_price": "NO DATA",
                "target": "NO DATA",
                "stop_loss": "NO DATA",
                "status": "NO TOKEN OR MARKET CLOSED"
            })

    return results
