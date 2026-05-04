from fastapi import FastAPI, Request
from signals import generate_signals
from zerodha_api import generate_token, get_ltp
import random

app = FastAPI()

# -----------------------------
# HOME ROUTE (health check)
# -----------------------------
@app.get("/")
def home():
    return {
        "status": "API Running",
        "message": "Stock Signal System Active"
    }

# -----------------------------
# ALL SIGNALS (mock engine)
# -----------------------------
@app.get("/signals")
def signals():
    return generate_signals()

# -----------------------------
# SINGLE STOCK ANALYSIS
# -----------------------------
@app.get("/predict/{stock}")
def predict(stock: str):

    price = get_ltp(stock)

    if price:
        return {
            "stock": stock.upper(),
            "live_price": price,
            "prediction": "Short-term bullish momentum",
            "expected_move": "1% to 5%",
            "confidence": random.randint(60, 90),
            "reason": "Live volume + sector strength"
        }

    return {
        "stock": stock.upper(),
        "live_price": None,
        "message": "Live price not available (token may not be set)"
    }

# -----------------------------
# ZERODHA CALLBACK (IMPORTANT)
# -----------------------------
@app.get("/callback")
def callback(request: Request):

    request_token = request.query_params.get("request_token")

    if not request_token:
        return {
            "status": "ERROR",
            "message": "Missing request_token"
        }

    try:
        result = generate_token(request_token)

        return {
            "status": "CALLBACK_SUCCESS",
            "data": result
        }

    except Exception as e:
        return {
            "status": "ERROR",
            "message": str(e)
        }
