from fastapi import FastAPI, Request
from signals import generate_signals
from zerodha_api import generate_token, get_ltp
import random
import os

app = FastAPI()

# -------------------
# HOME
# -------------------
@app.get("/")
def home():
    return {"status": "API Working with Zerodha Setup Ready"}

# -------------------
# SIGNALS
# -------------------
@app.get("/signals")
def signals():
    return generate_signals()

# -------------------
# SEARCH
# -------------------
@app.get("/predict/{stock}")
def predict(stock: str):

    price = get_ltp(stock)

    if price:
        return {
            "stock": stock.upper(),
            "live_price": price,
            "prediction": "Bullish momentum",
            "expected_move": "1% to 5%",
            "confidence": random.randint(60, 88)
        }

    return {
        "stock": stock.upper(),
        "error": "Price not available yet"
    }

# -------------------
# CALLBACK (ZERODHA LOGIN)
# -------------------
@app.get("/callback")
def callback(request: Request):

    request_token = request.query_params.get("request_token")

    if not request_token:
        return {"error": "Missing request_token"}

    return generate_token(request_token)
