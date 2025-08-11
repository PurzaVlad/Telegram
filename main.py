import requests
import re
import time

# ===== CONFIGURARE =====
TELEGRAM_TOKEN = "8426859153:AAHKp2b5KqjFdpZV0TnFsk62cqU3pmzX6GQ"
CHAT_ID = "5982074126"
URL = "https://altex.ro/laptop-apple-macbook-pro-14-mx2h3ro-a-apple-m4-pro-14-2-liquid-retina-xdr-24gb-ssd-512gb-16-core-gpu-macos-sequoia-space-black-tastatura-layout-int/cpd/LAPMX2H3ROA/"

def get_price():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        r = requests.get(URL, headers=headers, timeout=10)
        # Încearcă mai multe pattern-uri
        patterns = [
            r"(\d{1,3}(?:\.\d{3})*,\d{2})\s*lei",
            r"(\d{1,3}(?:\.\d{3})*)\s*lei",
            r'"price"[^>]*>(\d{1,3}(?:\.\d{3})*)',
            r'class="[^"]*price[^"]*"[^>]*>(\d{1,3}(?:\.\d{3})*)'
        ]
        for pattern in patterns:
            match = re.search(pattern, r.text, re.IGNORECASE)
            if match:
                return match.group(1)
        return None
    except:
        return None

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

# ===== MAIN LOOP =====
while True:
    price = get_price()
    if price:
        send_telegram_message(f"💻 Preț Macbook: {price} lei")
    else:
        send_telegram_message("⚠️ Nu pot obține prețul")
    
    time.sleep(3600)  # Așteaptă 1 oră
