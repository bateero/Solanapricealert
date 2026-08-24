import os
import time
import requests

BOT_TOKEN =8091102984:AAGuba8Y2JbZvnehwGKF3k4Pfs1RxK-WFk0
CHANNEL = "@solanaalertprice"

def get_sol_price():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "solana",
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }

    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()

    data = response.json()["solana"]

    return data["usd"], data.get("usd_24h_change", 0)


def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHANNEL,
        "text": message,
        "parse_mode": "HTML"
    }

    response = requests.post(url, json=payload, timeout=15)
    response.raise_for_status()


def main():
    while True:
        try:
            price, change = get_sol_price()

            emoji = "🟢" if change >= 0 else "🔴"

            message = f"""
🟣 <b>SOLANA PRICE UPDATE</b>

💰 <b>SOL:</b> ${price:,.2f}

{emoji} <b>24H:</b> {change:+.2f}%

📡 <b>Source:</b> CoinGecko
⏱ <b>Update:</b> Every 5 minutes

⚡ @solanaalertprice
"""

            send_telegram(message)
            print("Update sent:", price)

        except Exception as e:
            print("Error:", e)

        time.sleep(300)


if __name__ == "__main__":
    main()8091102984:AAGuba8Y2JbZvnehwGKF3k4Pfs1RxK-WFk0
