import os
import json
from kiteconnect import KiteConnect

TOKEN_FILE = "token.json"


# ---------------- TOKEN STORAGE ----------------
def save_token(token):
    with open(TOKEN_FILE, "w") as f:
        json.dump({"access_token": token}, f)


def load_token():
    try:
        with open(TOKEN_FILE, "r") as f:
            data = json.load(f)
            return data.get("access_token")
    except:
        return None


# ---------------- KITE INIT ----------------
def get_kite():
    api_key = os.getenv("API_KEY")
    return KiteConnect(api_key=api_key)


# ---------------- LOGIN CALLBACK ----------------
def generate_token(request_token):

    kite = get_kite()
    api_secret = os.getenv("API_SECRET")

    data = kite.generate_session(
        request_token,
        api_secret=api_secret
    )

    token = data["access_token"]

    save_token(token)

    return {
        "status": "SUCCESS",
        "access_token": token
    }


# ---------------- MARKET STATUS ----------------
def is_market_open():
    from datetime import datetime, time

    now = datetime.now().time()

    return time(9, 15) <= now <= time(15, 30)


# ---------------- LIVE PRICE (NO FAKE DATA) ----------------
def get_ltp(symbol):

    try:
        token = load_token()

        if not token:
            return None

        kite = get_kite()
        kite.set_access_token(token)

        data = kite.ltp(f"NSE:{symbol}")

        key = f"NSE:{symbol}"

        return float(data[key]["last_price"])

    except Exception as e:
        print("LTP ERROR:", e)
        return None
