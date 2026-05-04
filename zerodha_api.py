from kiteconnect import KiteConnect

API_KEY = "v4se78490za52f7m"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"

kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(ACCESS_TOKEN)

def get_ltp(symbol):
    try:
        data = kite.ltp(f"NSE:{symbol}")
        return data[f"NSE:{symbol}"]["last_price"]
    except:
        return None