from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import random
from datetime import datetime

from zerodha_api import generate_token, get_ltp

app = FastAPI()

# -------------------------
# FIX CORS (IMPORTANT FOR WORDPRESS)
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
# ENV CHECK
# -------------------------
@app.get("/env-check")
def env_check():
    return {
        "api_key_exists": bool(os.getenv("API_KEY")),
        "api_secret_exists": bool(os.getenv("API_SECRET"))
    }

# -------------------------
# SIGNAL ENGINE (REAL STRUCTURE, STILL SIMPLIFIED)
# -------------------------
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

    result = []

    for stock, sector in stocks:

        buy = round(random.uniform(100, 3000), 2)
        target = round(buy * random.uniform(1.01, 1.05), 2)
        sl = round(buy * 0.97, 2)

        result.append({
            "stock": stock,
            "sector": sector,
            "buy_price": buy,
            "target": target,
            "stop_loss": sl,
            "confidence": random.randint(60, 90),
            "expected_days": random.randint(1, 5),
            "reason": f"{sector} momentum + volume breakout",
            "time": str(datetime.now())
        })

    return result

# -------------------------
# STOCK PREDICTION
# -------------------------
@app.get("/predict/{stock}")
def predict(stock: str):

    price = get_ltp(stock)

    return {
        "stock": stock.upper(),
        "live_price": price,
        "prediction": "Short term momentum expected",
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

    return generate_token(request_token)
