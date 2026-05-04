import os
from kiteconnect import KiteConnect

kite = None
ACCESS_TOKEN = None


def init_kite():
    global kite

    if kite is None:
        api_key = os.getenv("API_KEY")

        if not api_key:
            return None

        kite = KiteConnect(api_key=api_key)

    return kite


def generate_token(request_token: str):
    global ACCESS_TOKEN

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

        ACCESS_TOKEN = data["access_token"]
        kite.set_access_token(ACCESS_TOKEN)

        return {
            "status": "SUCCESS",
            "access_token": ACCESS_TOKEN
        }

    except Exception as e:
        return {
            "status": "ERROR",
            "message": str(e)
        }


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
