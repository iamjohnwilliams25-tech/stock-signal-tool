import os
from kiteconnect import KiteConnect

# ---------------- ALWAYS FRESH CLIENT ----------------
def get_kite():

    api_key = os.getenv("API_KEY")
    kite = KiteConnect(api_key=api_key)

    return kite


# ---------------- GET LIVE PRICE (NO STATE DEPENDENCY) ----------------
def get_ltp(symbol):

    try:
        kite = get_kite()

        access_token = os.getenv("ACCESS_TOKEN")

        if not access_token:
            return None

        kite.set_access_token(access_token)

        data = kite.ltp(f"NSE:{symbol}")

        key = f"NSE:{symbol}"

        return float(data[key]["last_price"])

    except Exception as e:
        print("LTP ERROR:", e)
        return None


# ---------------- MARKET STATUS FIX ----------------
def is_market_open():

    from datetime import datetime, time

    now = datetime.now().time()

    return time(9, 15) <= now <= time(15, 30)
