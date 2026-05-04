from fastapi import FastAPI
from signals import generate_signals
import random

app = FastAPI()

# -------------------------
# HOME ROUTE
# -------------------------
@app.get("/")
def home():
    return {"status": "API Working"}

# -------------------------
# ALL SIGNALS
# -------------------------
@app.get("/signals")
def signals():
    return generate_signals()

# -------------------------
# SEARCH / PREDICT SINGLE STOCK
# -------------------------
@app.get("/predict/{stock}")
def predict(stock: str):

    return {
        "stock": stock.upper(),
        "prediction": "Short-term bullish momentum",
        "expected_move": "1% to 5%",
        "confidence": random.randint(60, 88),
        "reason": "Volume + sector strength"
    }
