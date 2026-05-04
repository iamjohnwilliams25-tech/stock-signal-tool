from zerodha_api import get_ltp

@app.get("/signals")
def signals():

    stocks = [
        ("TATA_POWER", "Power"),
        ("NTPC", "Power"),
        ("HAL", "Defence"),
        ("BEL", "Defence"),
        ("TCS", "AI"),
        ("INFY", "AI"),
        ("RELIANCE", "Energy")
    ]

    results = []

    for stock, sector in stocks:

        price = get_ltp(stock)

        # ❗ STILL SHOW ROW EVEN IF NULL
        results.append({
            "stock": stock,
            "sector": sector,
            "buy_price": price if price else "NO DATA",
            "target": (round(price * 1.02, 2) if price else "NO DATA"),
            "stop_loss": (round(price * 0.98, 2) if price else "NO DATA"),
            "market_status": "LIVE" if price else "NO DATA FROM ZERODHA"
        })

    return results
