import requests
import re

# ===== CONFIGURARE =====
TELEGRAM_TOKEN = "8426859153:AAHKp2b5KqjFdpZV0TnFsk62cqU3pmzX6GQ"
CHAT_ID = "5982074126"
URL = "https://altex.ro/laptop-apple-macbook-pro-14-mx2h3ro-a-apple-m4-pro-14-2-liquid-retina-xdr-24gb-ssd-512gb-16-core-gpu-macos-sequoia-space-black-tastatura-layout-int/cpd/LAPMX2H3ROA/"

# ===== FUNCTII =====
def get_price():
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(URL, headers=headers, timeout=10)
    match = re.search(r"(\d{1,3}(?:\.\d{3})*,\d{2})\s*lei", r.text)
    if match:
        return match.group(1)
    return None

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text}, timeout=10)

# ===== MAIN =====
price = get_price()
if price:
    send_telegram_message(f"💻 Preț Macbook pe Altex: {price}")
else:
    send_telegram_message("⚠️ Nu am putut obține prețul de la Altex.")
