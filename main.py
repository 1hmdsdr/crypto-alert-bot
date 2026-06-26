import requests

SYMBOL = "BTCUSDT"

url = f"https://api.binance.com/api/v3/ticker/price?symbol={SYMBOL}"

response = requests.get(url)

print(response.text)
