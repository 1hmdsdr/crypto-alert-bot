import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# تنظیم Alert آزمایشی
SYMBOL = "BTCUSDT"
TARGET_PRICE = 1  # برای تست تغییرش بده

# دریافت قیمت از Binance
url = f"https://api.binance.com/api/v3/ticker/price?symbol={SYMBOL}"

response = requests.get(url)
data = response.json()

current_price = float(data["price"])

print(f"Current {SYMBOL} price: {current_price}")

# بررسی شرط Alert
if current_price >= TARGET_PRICE:

    message = (
        f"🚨 ALERT!\n\n"
        f"{SYMBOL} reached your target price.\n\n"
        f"Current Price: {current_price}"
    )

    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(telegram_url, data=payload)

    print("Alert sent.")

else:
    print("Target price not reached.")
