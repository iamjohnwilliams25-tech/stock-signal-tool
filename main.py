from fastapi import FastAPI, Request
import os
import random

from signals import generate_signals
from zerodha_api import generate_token, get_ltp

app = FastAPI()

# -------------------------
# HOME
# -------------------------
@app.get("/")
def home():
    return {
        "status": "API Running",
        "message": "Stock Signal System Active"
    }

# -------------------------
# ENV CHECK (IMPORTANT DEBUG)
# -------------------------
@app.get("/env-check")
def env_check():
    return {
        "api_key_exists": bool(os.getenv("API_KEY")),
        "api_secret_exists": bool(os.getenv("API_SECRET"))
    }

# -------------------------
# SIGNALS
# -------------------------
@app.get("/signals")
def signals():
    return generate_signals()

# -------------------------
# SEARCH / PREDICT
# -------------------------
@app.get("/predict/{stock}")
def predict(stock: str):

    price = get_ltp(stock)

    return {
        "stock": stock.upper(),
        "live_price": price,
        "prediction": "Short-term momentum",
        "expected_move": "1% - 5%",
        "confidence": random.randint(60, 90)
    }

# -------------------------
# ZERODHA CALLBACK
# -------------------------
@app.get("/callback")
def callback(request: Request):

    request_token = request.query_params.get("request_token")

    if not request_token:
        return {"status": "ERROR", "message": "Missing request_token"}

    result = generate_token(request_token)

    return result
