import requests, os, time, threading
from flask import Flask
app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")

WHALE_WALLETS = [
    "7xKf...9pQ2",
    "8aLp...3mNq",
    "9zQw...1kLx",
]
seen = set()

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": msg})
    except:
        pass

def check_wallet(wallet):
    try:
        url = f"https://mainnet.helius-rpc.com/?api-key={HELIUS_API_KEY}"
        payload = {"jsonrpc":"2.0","id":1,"method":"getSignaturesForAddress","params":[wallet,{"limit":2}]}
        r = requests.post(url, json=payload, timeout=10).json()
        sigs = r.get("result", [])
        for s in sigs:
            sig = s.get("signature")
            if sig and sig not in seen:
                seen.add(sig)
                send_telegram(f"⚡ EARLY BUYER BOUGHT\n\nWallet: {wallet}\nNew Tx: {sig[:12]}...\nTime: Abhi-abhi")
    except:
        pass

def loop():
    while True:
        for w in WHALE_WALLETS:
            check_wallet(w)
        time.sleep(15)

def listen_start():
    last = 0
    while True:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates?offset={last+1}&timeout=10"
            res = requests.get(url, timeout=15).json()
            for u in res.get("result", []):
                last = u["update_id"]
                msg = u.get("message", {})
                if msg.get("text") == "/start":
                    send_telegram("⚡ Early Buyer Bot ON hai! Ab se Early Buyer ka signal yahi aayega.")
        except:
            pass
        time.sleep(2)

@app.route('/')
def home():
    return "Early Buyer Bot Running!"

if __name__ == "__main__":
    threading.Thread(target=loop, daemon=True).start()
    threading.Thread(target=listen_start, daemon=True).start()
    send_telegram("⚡ Early Buyer Bot Started on Render! Ab se signal aayega.")
    app.run(host="0.0.0.0", port=10000)
