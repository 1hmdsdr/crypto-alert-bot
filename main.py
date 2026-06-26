import os
import json
import time
import requests
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

MAX_RETRIES = 3
REQUEST_TIMEOUT = 15

print("===================================")
print("CRYPTO ALERT BOT STARTED")
print("Time:", datetime.utcnow())
print("===================================")

# خواندن مپ ارزها
with open("coin_mapping.json", "r") as file:
    coin_mapping = json.load(file)

# خواندن Alert ها
with open("alerts.json", "r") as file:
    alerts = json.load(file)

# خواندن تاریخچه
with open("triggered_alerts.json", "r") as file:
    triggered_alerts = json.load(file)

active_alerts = 0
triggered_count = 0

for alert in alerts:

    if not alert["active"]:
        continue

    active_alerts += 1

    symbol = alert["coin"].upper()

    if symbol not in coin_mapping:
        print(f"[WARNING] Unsupported coin: {symbol}")
        continue

    coin = coin_mapping[symbol]

    print(f"\nChecking {symbol}")

    current_price = None

    for attempt in range(1, MAX_RETRIES + 1):

        try:
            print(f"Attempt {attempt}...")

            url = (
                "https://api.coingecko.com/api/v3/simple/price"
                f"?ids={coin}&vs_currencies=usd"
            )

            response = requests.get(
                url,
                timeout=REQUEST_TIMEOUT
            )

            response.raise_for_status()

            data = response.json()

            current_price = data[coin]["usd"]

            print(f"{symbol} price: {current_price}")

            break

        except Exception as e:
            print(
                f"[ERROR] {symbol} "
                f"(Attempt {attempt}): {e}"
            )

            if attempt < MAX_RETRIES:
                print("Retrying in 5 seconds...")
                time.sleep(5)

    if current_price is None:
        print(
            f"[FAILED] Could not fetch "
            f"price for {symbol}"
        )
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

        print(f"[TRIGGERED] {symbol}")

        message = (
            f"🚨 CRYPTO ALERT 🚨\n\n"
            f"🪙 Coin: {symbol}\n"
            f"📈 Condition: "
            f"{alert['condition'].upper()}\n"
            f"🎯 Target Price: "
            f"${alert['target_price']}\n"
            f"💰 Current Price: "
            f"${current_price}\n"
            f"🏦 Source: CoinGecko\n"
            f"⏰ Time: "
            f"{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}"
        )

        telegram_url = (
            f"https://api.telegram.org/"
            f"bot{BOT_TOKEN}/sendMessage"
        )

        payload = {
            "chat_id": CHAT_ID,
            "text": message
        }

        try:
            telegram_response = requests.post(
                telegram_url,
                data=payload,
                timeout=REQUEST_TIMEOUT
            )

            telegram_response.raise_for_status()

            print(
                f"[SUCCESS] Telegram alert "
                f"sent for {symbol}"
            )

            alert["active"] = False

            triggered_alerts.append({
                "id": alert["id"],
                "coin": symbol,
                "condition": alert["condition"],
                "target_price": alert["target_price"],
                "triggered_price": current_price,
                "exchange": alert["exchange"],
                "triggered_at":
                    datetime.utcnow().strftime(
                        "%Y-%m-%d %H:%M:%S UTC"
                    )
            })

            triggered_count += 1

        except Exception as e:
            print(
                f"[ERROR] Failed to send "
                f"Telegram message: {e}"
            )

# ذخیره فایل‌ها

with open("alerts.json", "w") as file:
    json.dump(alerts, file, indent=4)

with open("triggered_alerts.json", "w") as file:
    json.dump(triggered_alerts, file, indent=4)

print("\n===================================")
print("BOT FINISHED")
print(f"Active alerts checked: {active_alerts}")
print(f"Triggered alerts: {triggered_count}")
print("===================================")
