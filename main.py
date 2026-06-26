import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

SYMBOL = "BTCUSDT"
TARGET_PRICE = 1  # فقط برای تست

# دریافت قیمت از Bybit
url = f"https://api.bybit.com/v5/market/tickers?category=spot&symbol={SYMBOL}"

response = requests.get(url)
data = response.json()

print(data)

current_price = float(data["result"]["list"][0]["lastPrice"])

print(f"Current price: {current_price}")

if current_price >= TARGET_PRICE:

    message = (
        f"🚨 ALERT!\n\n"
        f"{SYMBOL}\n"
        f"Current Price: {current_price}\n"
        f"Exchange: Bybit"
    )

    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(telegram_url, data=payload)

    print("Alert sent.")

else:
    print("Target not reached.")
