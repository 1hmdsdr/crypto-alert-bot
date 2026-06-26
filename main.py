import os
import json
import requests
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# خواندن مپ ارزها
with open("coin_mapping.json", "r") as file:
    coin_mapping = json.load(file)

# خواندن Alert ها
with open("alerts.json", "r") as file:
    alerts = json.load(file)

# خواندن تاریخچه
with open("triggered_alerts.json", "r") as file:
    triggered_alerts = json.load(file)

for alert in alerts:

    if not alert["active"]:
        continue

    symbol = alert["coin"].upper()

    if symbol not in coin_mapping:
        print(f"Unsupported coin: {symbol}")
        continue

    coin = coin_mapping[symbol]

    print(f"Checking {symbol}")

    try:
        url = (
            f"https://api.coingecko.com/api/v3/simple/price"
            f"?ids={coin}&vs_currencies=usd"
        )

        response = requests.get(url)
        data = response.json()

        current_price = data[coin]["usd"]

        print(f"{symbol}: {current_price}")

    except Exception as e:
        print(f"Error for {symbol}: {e}")
        continue

    should_trigger = False

    if (
        alert["condition"] == "above"
        and current_price >= alert["target_price"]
    ):
        should_trigger = True

    if (
        alert["condition"] == "below"
        and current_price <= alert["target_price"]
    ):
        should_trigger = True

    if should_trigger:

        message = (
            f"🚨 ALERT TRIGGERED\n\n"
            f"Coin: {symbol}\n"
            f"Condition: {alert['condition']}\n"
            f"Target Price: ${alert['target_price']}\n"
            f"Current Price: ${current_price}"
        )

        telegram_url = (
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        )

        payload = {
            "chat_id": CHAT_ID,
            "text": message
        }

        requests.post(
            telegram_url,
            data=payload
        )

        alert["active"] = False

        triggered_alerts.append({
            "id": alert["id"],
            "coin": symbol,
            "condition": alert["condition"],
            "target_price": alert["target_price"],
            "triggered_price": current_price,
            "exchange": alert["exchange"],
            "triggered_at": datetime.utcnow().strftime(
                "%Y-%m-%d %H:%M:%S UTC"
            )
        })

        print(f"Alert sent for {symbol}")

# ذخیره فایل ها
with open("alerts.json", "w") as file:
    json.dump(alerts, file, indent=4)

with open("triggered_alerts.json", "w") as file:
    json.dump(triggered_alerts, file, indent=4)
