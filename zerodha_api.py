import os
from kiteconnect import KiteConnect


# ---------------- INIT ----------------
def get_kite():
    return KiteConnect(api_key=os.getenv("API_KEY"))


# ---------------- TOKEN FROM RAILWAY ENV ----------------
def get_token():
    return os.getenv("ACCESS_TOKEN")


# ---------------- LOGIN CALLBACK ----------------
def generate_token(request_token):

    kite = get_kite()
    api_secret = os.getenv("API_SECRET")

    data = kite.generate_session(
        request_token,
        api_secret=api_secret
    )

    token = data["access_token"]

    return {
        "status": "SUCCESS",
        "access_token": token,
        "message": "COPY THIS → /set-token/{token}"
    }


# ---------------- LIVE PRICE ----------------
def get_ltp(symbol):

    try:
        token = get_token()

        if not token:
            return None

        kite = get_kite()
        kite.set_access_token(token)

        data = kite.ltp(f"NSE:{symbol}")

        return float(data[f"NSE:{symbol}"]["last_price"])

    except Exception as e:
        print("LTP ERROR:", e)
        return None
