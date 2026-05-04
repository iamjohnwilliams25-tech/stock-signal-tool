import os
from kiteconnect import KiteConnect

kite = None
ACCESS_TOKEN = None

def init_kite():
    global kite

    if kite is None:
        api_key = os.getenv("API_KEY")
        kite = KiteConnect(api_key=api_key)

    return kite


def generate_token(request_token):

    kite = init_kite()

    api_secret = os.getenv("API_SECRET")

    data = kite.generate_session(
        request_token,
        api_secret=api_secret
    )

    global ACCESS_TOKEN
    ACCESS_TOKEN = data["access_token"]
    kite.set_access_token(ACCESS_TOKEN)

    return {
        "status": "SUCCESS",
        "access_token": ACCESS_TOKEN
    }


def get_ltp(symbol):
    try:
        if not ACCESS_TOKEN:
            return None

        kite = init_kite()
        data = kite.ltp(f"NSE:{symbol}")
        return data[f"NSE:{symbol}"]["last_price"]

    except:
        return None
