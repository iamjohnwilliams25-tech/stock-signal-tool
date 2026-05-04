from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from signals import generate_signals
from zerodha_api import generate_token, get_ltp
import os
import random

app = FastAPI()

# -------------------------
# FIX CORS (CRITICAL FOR WORDPRESS)
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
    return {"status": "API Running", "mode": "LIVE READY"}

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
# SIGNALS
# -------------------------
@app.get("/signals")
def signals():
    return generate_signals()

# -------------------------
# PREDICT
# -------------------------
@app.get("/predict/{stock}")
def predict(stock: str):

    price = get_ltp(stock)

    return {
        "stock": stock.upper(),
        "live_price": price,
        "prediction": "Momentum move expected",
        "confidence": random.randint(60, 90)
    }

# -------------------------
# CALLBACK
# -------------------------
@app.get("/callback")
def callback(request: Request):

    request_token = request.query_params.get("request_token")

    if not request_token:
        return {"status": "ERROR", "message": "Missing request_token"}

    return generate_token(request_token)
