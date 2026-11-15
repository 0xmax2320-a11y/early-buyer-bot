import requests
import time
import os
from flask import Flask

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=data)

@app.route('/')
def home():
    return "Early Buyer Bot is Running!"

if __name__ == "__main__":
    send_telegram("⚡ Early Buyer Bot Started on Render! Ab se signal aayega.")
    app.run(host="0.0.0.0", port=10000)
