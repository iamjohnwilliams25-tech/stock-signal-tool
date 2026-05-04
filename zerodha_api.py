import os
from kiteconnect import KiteConnect

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

kite = KiteConnect(api_key=API_KEY)

ACCESS_TOKEN = None


def generate_token(request_token: str):
    global ACCESS_TOKEN

    try:
        data = kite.generate_session(
            request_token,
            api_secret=API_SECRET
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

        data = kite.ltp(f"NSE:{symbol}")
        return data[f"NSE:{symbol}"]["last_price"]

    except Exception:
        return None