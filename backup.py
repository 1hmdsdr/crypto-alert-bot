import json
from datetime import datetime

# خواندن فایل‌ها
with open("alerts.json", "r") as file:
    alerts = json.load(file)

with open("triggered_alerts.json", "r") as file:
    history = json.load(file)

backup_data = {
    "created_at": datetime.utcnow().strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    ),
    "alerts": alerts,
    "history": history
}

filename = (
    "backups/backup_"
    + datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    + ".json"
)

with open(filename, "w") as file:
    json.dump(backup_data, file, indent=4)

print(f"Backup created: {filename}")
