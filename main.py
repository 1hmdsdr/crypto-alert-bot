import os
import json
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# خواندن Alertها
with open("alerts.json", "r") as file:
    alerts = json.load(file)

for alert in alerts:

    if not alert["active"]:
        continue

    coin = alert["coin"]

    url = (
        f"https://api.coingecko.com/api/v3/simple/price"
        f"?ids={coin}&vs_currencies=usd"
    )

    response = requests.get(url)
    data = response.json()

    current_price = data[coin]["usd"]

    print(f"{coin}: {current_price}")

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
            f"Coin: {coin}\n"
            f"Current Price: ${current_price}\n"
            f"Target: ${alert['target_price']}"
        )

        telegram_url = (
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        )

        payload = {
            "chat_id": CHAT_ID,
            "text": message
        }

        requests.post(telegram_url, data=payload)

        alert["active"] = False

# ذخیره وضعیت جدید
with open("alerts.json", "w") as file:
    json.dump(alerts, file, indent=4)
