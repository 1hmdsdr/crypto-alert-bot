import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

coin_id = "bitcoin"

url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"

response = requests.get(url)

print("CoinGecko response:")
print(response.text)

data = response.json()

current_price = data["bitcoin"]["usd"]

print("Current price:", current_price)

telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

payload = {
    "chat_id": CHAT_ID,
    "text": f"🚀 Test Alert\n\nBTC Price: ${current_price}"
}

telegram_response = requests.post(telegram_url, data=payload)

print("Telegram response:")
print(telegram_response.text)
