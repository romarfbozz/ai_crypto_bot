import os
import time
import requests
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = "7384247990:AAEBad20wB0R30DNaORfwL3u5x8mtuz_MEU"
CHAT_ID = "891146043"
URL = "https://www.tradingview.com/ideas/btc/"

POSITIVE = ["long", "bullish", "breakout", "pump", "buy"]
NEGATIVE = ["short", "bearish", "dump", "crash", "sell"]

seen = set()

def send(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}
    r = requests.post(url, data=payload)
    if not r.ok:
        print(f"🚨 Telegram API error: {r.status_code} · {r.text}")

def fetch():
    try:
        r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
        print("Статус TradingView:", r.status_code)
        soup = BeautifulSoup(r.text, "html.parser")
        ideas = soup.select("a.tv-widget-idea__title")
        print("Найдено идей:", len(ideas))

        for idea in ideas:
            title = idea.get_text(strip=True)
            link = "https://www.tradingview.com" + idea["href"]
            if link in seen:
                print("✅ Уже видел:", title)
                continue

            label = (
                "🟢 Лонг" if any(w in title.lower() for w in POSITIVE) else
                "🔴 Шорт" if any(w in title.lower() for w in NEGATIVE) else
                "🟡 Нейтрально"
            )
            msg = f"{label} — <b>{title}</b>\n{link}"
            send(msg)
            print("🟦 Отправлено:", title)
            seen.add(link)

    except Exception as e:
        print("🚨 Ошибка парсинга:", e)

if __name__ == "__main__":
    print("🤖 ИИ-бот запущен")
    send("✅ Бот стартовал!")  # проверка отправки
    while True:
        fetch()
        time.sleep(300)  # 5 минут
