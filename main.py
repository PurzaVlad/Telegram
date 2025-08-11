import requests
import time
from bs4 import BeautifulSoup

# ===== CONFIGURARE =====
TELEGRAM_TOKEN = "8426859153:AAHKp2b5KqjFdpZV0TnFsk62cqU3pmzX6GQ"
CHAT_ID = "5982074126"

# Link-uri produs (trebuie să fie exact configurația dorită)
URLS = {
    "Altex": "https://altex.ro/laptop-apple-macbook-pro-14-mx2h3ro-a-apple-m4-pro-14-2-liquid-retina-xdr-24gb-ssd-512gb-16-core-gpu-macos-sequoia-space-black-tastatura-layout-int/cpd/LAPMX2H3ROA/",
}
# ===== FUNCTII =====
def get_price_altex(url):
    """Returnează prețul de pe Altex."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        page = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(page.text, "html.parser")

        # caută prețul
        price_tag = soup.find("span", class_="Price-int")
        frac_tag = soup.find("sup", class_="Price-dec")
        if price_tag:
            lei = price_tag.get_text(strip=True).replace(".", "")
            bani = frac_tag.get_text(strip=True) if frac_tag else "00"
            return float(f"{lei}.{bani}")
    except Exception as e:
        print(f"[EROARE] Altex: {e}")
    return None

def send_telegram_message(text):
    """Trimite un mesaj pe Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print(f"[EROARE] Trimitere Telegram: {e}")

# ===== MAPARE FUNCTII =====
SCRAPERS = {
    "Altex": get_price_altex,
}

# ===== LOOP PRINCIPAL =====
if __name__ == "__main__":
    while True:
        best_price = None
        best_vendor = None

        for vendor, url in URLS.items():
            scraper = SCRAPERS.get(vendor)
            if scraper:
                price = scraper(url)
                if price:
                    print(f"{vendor}: {price:.2f} lei")
                    if best_price is None or price < best_price:
                        best_price = price
                        best_vendor = vendor
                else:
                    print(f"{vendor}: Preț indisponibil")

        if best_price:
            message = f"💻 Macbook: {best_vendor} - {best_price:.2f} lei"
            send_telegram_message(message)
            print("[Trimis]", message)
        else:
            send_telegram_message("⚠️ Nu am putut găsi prețurile acum.")
            print("[INFO] Nu s-au găsit prețuri.")

        time.sleep(600)
