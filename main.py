import os

print("Crypto Alert Bot started successfully!")

bot_token = os.getenv("BOT_TOKEN")

if bot_token:
    print("BOT_TOKEN loaded successfully.")
else:
    print("BOT_TOKEN not found.")
