from fastapi import FastAPI
from signals import generate_signals

app = FastAPI()

@app.get("/")
def home():
    return {"status": "API Running Successfully"}

@app.get("/signals")
def signals():
    return generate_signals()