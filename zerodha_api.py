import os
from kiteconnect import KiteConnect

kite = None
ACCESS_TOKEN = None


# -----------------------------
# INIT KITE CLIENT
# -----------------------------
def init_kite():
    global kite

    if kite is None:
        api_key = os.getenv("API_KEY")

        if not api_key:
            return None

        kite = KiteConnect(api_key=api_key)

    return kite


# -----------------------------
# STORE TOKEN (SAFE MEMORY)
# -----------------------------
def set_token(token):
    global ACCESS_TOKEN
    ACCESS_TOKEN = token


def get_token():
    return ACCESS_TOKEN


# -----------------------------
# GENERATE TOKEN AFTER LOGIN
# -----------------------------
def generate_token(request_token: str):

    try:
        kite = init_kite()

        if kite is None:
            return {"status": "ERROR", "message": "API_KEY missing in environment"}

        api_secret = os.getenv("API_SECRET")

        if not api_secret:
            return {"status": "ERROR", "message": "API_SECRET missing in environment"}

        data = kite.generate_session(
            request_token,
            api_secret=api_secret
        )

        global ACCESS_TOKEN
        ACCESS_TOKEN = data["access_token"]
        kite.set_access_token(ACCESS_TOKEN)

        set_token(ACCESS_TOKEN)

        return {
            "status": "SUCCESS",
            "access_token": ACCESS_TOKEN
        }

    except Exception as e:
        return {
            "status": "ERROR",
            "message": str(e)
        }


# -----------------------------
# LIVE PRICE (SAFE)
# -----------------------------
def get_ltp(symbol: str):

    try:
        if not ACCESS_TOKEN:
            return None

        kite = init_kite()

        if not kite:
            return None

        data = kite.ltp(f"NSE:{symbol}")
        return data[f"NSE:{symbol}"]["last_price"]

    except:
        return None
