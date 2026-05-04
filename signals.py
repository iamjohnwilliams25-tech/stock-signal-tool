from zerodha_api import get_ltp, is_market_open

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

        # ❗ IMPORTANT: NEVER SKIP COMPLETELY
        if price is None:
            results.append({
                "stock": stock,
                "sector": sector,
                "buy_price": "NO DATA",
                "target": "NO DATA",
                "stop_loss": "NO DATA",
                "market_status": "NO DATA (CHECK ZERODHA)"
            })
            continue

        results.append({
            "stock": stock,
            "sector": sector,
            "buy_price": price,
            "target": round(price * 1.02, 2),
            "stop_loss": round(price * 0.98, 2),
            "market_status": "LIVE" if is_market_open() else "CLOSED (CACHED)"
        })

    return results
