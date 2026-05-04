from fastapi import FastAPI
from signals import generate_signals

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Stock Signal API Running"}

@app.get("/signals")
def get_signals():
    return generate_signals()

@app.get("/predict/{stock}")
def predict(stock: str):
    return {
        "stock": stock,
        "prediction": "Bullish",
        "target_move": "2-5%",
        "confidence": "70%"
    }