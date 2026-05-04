from fastapi import FastAPI, Request
from kiteconnect import KiteConnect
import os
from signals import generate_signals

app = FastAPI()

# ----------------------------
# BASIC TEST ROUTE
# ----------------------------
@app.get("/")
def home():
    return {"status": "Stock Signal API Running"}

# ----------------------------
# SIGNALS (LIVE DATA LATER)
# ----------------------------
@app.get("/signals")
def signals():
    return generate_signals()

# ----------------------------
# ZERODHA CALLBACK
# ----------------------------
@app.get("/callback")
def callback(request: Request):
    request_token = request.query_params.get("request_token")

    if not request_token:
        return {"error": "Missing request_token"}

    kite = KiteConnect(api_key=os.getenv("API_KEY"))

    data = kite.generate_session(
        request_token,
        api_secret=os.getenv("API_SECRET")
    )

    access_token = data["access_token"]

    return {
        "message": "Token generated successfully",
        "access_token": access_token
    }