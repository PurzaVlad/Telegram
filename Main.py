import requests
import time
from bs4 import BeautifulSoup

# ===== CONFIGURARE =====
TELEGRAM_TOKEN = "8426859153:AAHKp2b5KqjFdpZV0TnFsk62cqU3pmzX6GQ"
CHAT_ID = "5982074126"

# Link-uri produs (trebuie să fie exact configurația dorită)
URLS = {
    "eMAG": "https://www.emag.ro/laptop-macbook-pro-14-procesor-apple-m4-pro-cu-12-nuclee-gpu-cu-16-nuclee-24-gb-512-gb-ssd-argintiu-mx2e3mg-a/pd/D2ZMLRYBM/",
    "Altex": "https://altex.ro/laptop-apple-macbook-pro-14-inch-2024-m4-pro-12-core-cpu-16-core-gpu-24gb-512gb-ssd-macos-argintiu/cpd/LAPMX2E3RO/",
    "Flanco": "https://www.flanco.ro/laptop-apple-macbook-pro-14-inch-m4-pro-12-core-cpu-16-core-gpu-24gb-512gb-ssd-macos-argintiu.html",
    "iStyle": "https://www.istyle.ro/macbook-pro-14-inch-apple-m4-pro-cu-12-nuclee-cpu-si-16-nuclee-gpu-24gb-512gb-ssd-argintiu.html"
}

# ===== FUNCTII =====
def get_price(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        page = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(page.text, "html.parser")

        # caută orice text de tip "lei"
        text = soup.get_text()
        import re
        match = re.search(r"(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?)\s*lei", text)
        if match:
            price = match.group(1).replace(".", "").replace(",", ".")
            return float(price)
    except Exception as e:
        print(f"Eroare la {url}: {e}")
    return None

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=payload)

# ===== LOOP PRINCIPAL =====
while True:
    best_price = None
    best_vendor = None

    for vendor, url in URLS.items():
        price = get_price(url)
        if price:
            print(f"{vendor}: {price} lei")
            if best_price is None or price < best_price:
                best_price = price
                best_vendor = vendor

    if best_price:
        message = f"Macbook:{best_vendor}-{best_price:.2f} lei"
        send_telegram_message(message)
        print("Trimis:", message)
    else:
        send_telegram_message("Nu am putut găsi prețurile acum.")

    time.sleep(600)  # 10 minute
