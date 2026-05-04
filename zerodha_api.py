import os
from kiteconnect import KiteConnect

# ---------------- KITE CLIENT ----------------
def get_kite():
    return KiteConnect(api_key=os.getenv("API_KEY"))


# ---------------- SAVE TOKEN TO RAILWAY ENV ----------------
def save_token_env(token):
    # NOTE: Railway env cannot be updated dynamically via code
    # so we return token to store manually once OR via deploy panel
    return token


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
        "message": "COPY THIS TOKEN → ADD IN RAILWAY ENV VARIABLE: ACCESS_TOKEN"
    }


# ---------------- GET TOKEN ----------------
def get_token():
    return os.getenv("ACCESS_TOKEN")


# ---------------- MARKET STATUS ----------------
def is_market_open():
    from datetime import datetime, time

    now = datetime.now().time()
    return time(9, 15) <= now <= time(15, 30)


# ---------------- LIVE PRICE ----------------
def get_ltp(symbol):

    try:
        token = get_token()

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
