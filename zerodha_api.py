import os
from kiteconnect import KiteConnect

kite = None
ACCESS_TOKEN = None

def init_kite():
    global kite

    if kite is None:
        api_key = os.getenv("API_KEY")

        if not api_key:
            raise Exception("API_KEY missing in environment")

        kite = KiteConnect(api_key=api_key)

    return kite


def generate_token(request_token: str):
    global ACCESS_TOKEN

    kite = init_kite()

    api_secret = os.getenv("API_SECRET")

    if not api_secret:
        return {"error": "API_SECRET missing"}

    data = kite.generate_session(
        request_token,
        api_secret=api_secret
    )

    ACCESS_TOKEN = data["access_token"]
    kite.set_access_token(ACCESS_TOKEN)

    return {
        "status": "SUCCESS",
        "access_token": ACCESS_TOKEN
    }


def get_ltp(symbol: str):
    try:
        if not ACCESS_TOKEN:
            return None

        kite = init_kite()

        data = kite.ltp(f"NSE:{symbol}")
        return data[f"NSE:{symbol}"]["last_price"]

    except Exception:
        return None
