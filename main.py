@app.get("/predict/{stock}")
def predict(stock: str):
    return {
        "stock": stock,
        "prediction": "Bullish short-term momentum",
        "expected_move": "1-5%",
        "confidence": random.randint(60, 85)
    }
