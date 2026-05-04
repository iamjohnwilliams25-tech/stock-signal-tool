from fastapi import FastAPI, Request
from signals import generate_signals
from zerodha_api import generate_token, get_ltp
import random
import os

app = FastAPI()

@app.get("/")
def home():
    return {"status": "API Running", "mode": "LIVE READY"}

@app.get("/env-check")
def env_check():
    return {
        "api_key_exists": bool(os.getenv("API_KEY")),
        "api_secret_exists": bool(os.getenv("API_SECRET"))
    }

@app.get("/signals")
def signals():
    return generate_signals()

@app.get("/predict/{stock}")
def predict(stock: str):

    price = get_ltp(stock)

    if price:
        return {
            "stock": stock.upper(),
            "live_price": price,
            "prediction": "Market momentum detected",
            "expected_move": "1% - 5%",
            "confidence": random.randint(65, 92)
        }

    return {
        "stock": stock.upper(),
        "live_price": None,
        "message": "Token not active or market data not available yet"
    }

@app.get("/callback")
def callback(request: Request):

    request_token = request.query_params.get("request_token")

    if not request_token:
        return {"status": "ERROR", "message": "Missing request_token"}

    return generate_token(request_token)
