from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from zerodha_api import generate_token, get_ltp, is_market_open, load_token

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

# ---------------- TOKEN STATUS ----------------
@app.get("/token-status")
def token_status():
    return {
        "token_exists": load_token() is not None
    }

# ---------------- PRICE TEST ----------------
@app.get("/price/{symbol}")
def price(symbol: str):

    price = get_ltp(symbol)

    return {
        "symbol": symbol,
        "price": price,
        "market_open": is_market_open()
    }

# ---------------- SIGNALS (NO FAKE DATA EVER) ----------------
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

        # ❗ NEVER SKIP → NEVER BLANK PAGE
        if price is None:
            results.append({
                "stock": stock,
                "sector": sector,
                "buy_price": "NO DATA",
                "target": "NO DATA",
                "stop_loss": "NO DATA",
                "status": "NO ZERODHA DATA"
            })
            continue

        results.append({
            "stock": stock,
            "sector": sector,
            "buy_price": price,
            "target": round(price * 1.02, 2),
            "stop_loss": round(price * 0.98, 2),
            "status": "LIVE" if is_market_open() else "CLOSED (CACHED)"
        })

    return results

# ---------------- ZERODHA CALLBACK ----------------
@app.get("/callback")
def callback(request: Request):

    request_token = request.query_params.get("request_token")

    if not request_token:
        return {"status": "ERROR"}

    return generate_token(request_token)
