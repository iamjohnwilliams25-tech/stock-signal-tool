import os
from kiteconnect import KiteConnect

kite = None
ACCESS_TOKEN = None


# -----------------------------
# INIT CLIENT
# -----------------------------
def init_kite():
    global kite

    if kite is None:
        api_key = os.getenv("API_KEY")

        if not api_key:
            raise Exception("API_KEY missing")

        kite = KiteConnect(api_key=api_key)

    return kite


# -----------------------------
# STORE SESSION (CRITICAL FIX)
# -----------------------------
def set_session(token):
    global ACCESS_TOKEN, kite

    ACCESS_TOKEN = token

    kite = init_kite()
    kite.set_access_token(token)


def get_session():
    return ACCESS_TOKEN


# -----------------------------
# LOGIN CALLBACK
# -----------------------------
def generate_token(request_token):

    kite = init_kite()
    api_secret = os.getenv("API_SECRET")

    data = kite.generate_session(
        request_token,
        api_secret=api_secret
    )

    token = data["access_token"]

    set_session(token)

    return {
        "status": "SUCCESS",
        "access_token": token
    }


# -----------------------------
# LIVE PRICE (STRICT FIX)
# -----------------------------
def get_ltp(symbol):

    try:
        if not ACCESS_TOKEN:
            return None

        kite.set_access_token(ACCESS_TOKEN)

        data = kite.ltp(f"NSE:{symbol}")

        key = f"NSE:{symbol}"

        if key not in data:
            return None

        return float(data[key]["last_price"])

    except Exception as e:
        print("LTP ERROR:", e)
        return None
