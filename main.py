import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

print("BOT_TOKEN exists:", BOT_TOKEN is not None)
print("CHAT_ID:", CHAT_ID)

SYMBOL = "BTCUSDT"

url = f"https://api.bybit.com/v5/market/tickers?category=spot&symbol={SYMBOL}"

response = requests.get(url)

print("Bybit response:")
print(response.text)

data = response.json()

current_price = float(data["result"]["list"][0]["lastPrice"])

print("Current price:", current_price)

telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

payload = {
    "chat_id": CHAT_ID,
    "text": f"Test message\n{SYMBOL}: {current_price}"
}

telegram_response = requests.post(telegram_url, data=payload)

print("Telegram response:")
print(telegram_response.text)
