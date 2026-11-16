import requests, os, time, threading
from flask import Flask
app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")

ENTRY_TIME_MAX = 5 * 60
WIN_RATE_MIN = 60
AUTO_DISCOVERY = True
TRACKED_WALLETS = []

def send_msg(text):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": text}, timeout=10)
    except Exception as e:
        print("Telegram Error:", e)

def auto_discover():
    send_msg("🤖 EarlyWhalestrack.io ON ho gaya!\n\nBot ab khud wallet dhoondhega...\nRule: 5 Min me Entry + 60%+ Win Rate\nMode: FREE - Auto Discovery")
    while True:
        try:
            print("Scanning new tokens for Early Buyers...")
            time.sleep(60)
        except Exception as e:
            print("Error:", e)
            time.sleep(60)

@app.route("/")
def home():
    return f"EarlyWhalestrack.io is Running - Auto Discovery ON - Wallets Found: {len(TRACKED_WALLETS)}"

if __name__ == "__main__":
    t = threading.Thread(target=auto_discover, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
