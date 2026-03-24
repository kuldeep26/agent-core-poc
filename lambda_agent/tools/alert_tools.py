import requests
import os

WEBHOOK = os.environ.get("TEAMS_WEBHOOK")

def send_alert(message):
    requests.post(WEBHOOK, json={"text": message})
    return {"alert": "sent"}