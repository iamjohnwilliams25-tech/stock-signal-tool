import os
import datetime
from kiteconnect import KiteConnect

kite = None
ACCESS_TOKEN = None

# ---------------- CACHE STORAGE ----------------
LAST_KNOWN_PRICES = {}


# ---------------- INIT ----------------
def init_kite():
    global kite

    if kite is None:
        api_key = os.getenv("API_KEY")
        kite = KiteConnect(api_key=api_key)

    return kite


# ---------------- SESSION ----------------
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


# ---------------- MARKET STATUS ----------------
def is_market_open():

    now = datetime.datetime.now().time()

    start = datetime.time(9, 15)
    end = datetime.time(15, 30)

    return start <= now <= end


# ---------------- LIVE PRICE + CACHE ----------------
def get_ltp(symbol):

    global LAST_KNOWN_PRICES

    try:
        if not ACCESS_TOKEN:
            return LAST_KNOWN_PRICES.get(symbol)

        kite = init_kite()
        kite.set_access_token(ACCESS_TOKEN)

        data = kite.ltp(f"NSE:{symbol}")
        key = f"NSE:{symbol}"

        price = float(data[key]["last_price"])

        # SAVE TO CACHE
        LAST_KNOWN_PRICES[symbol] = price

        return price

    except Exception as e:
        print("LTP ERROR:", e)

        # fallback → return cached value
        return LAST_KNOWN_PRICES.get(symbol)
