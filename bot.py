import os
import requests
from datetime import datetime, timezone

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL = "@solanaalertprice"


def get_sol_price():
    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids": "solana",
        "vs_currencies": "usd",
        "include_24hr_change": "true",
        "include_market_cap": "true",
        "include_24hr_vol": "true",
        "include_24hr_high": "true",
        "include_24hr_low": "true",
    }

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()

    return response.json()["solana"]


def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHANNEL,
        "text": message,
        "parse_mode": "HTML",
    }

    response = requests.post(url, json=data, timeout=20)
    response.raise_for_status()


def main():
    sol = get_sol_price()

    price = sol["usd"]
    change = sol.get("usd_24h_change", 0)
    market_cap = sol.get("usd_market_cap", 0)
    volume = sol.get("usd_24h_vol", 0)
    high = sol.get("usd_24h_high", 0)
    low = sol.get("usd_24h_low", 0)

    emoji = "🟢" if change >= 0 else "🔴"

    updated = datetime.now(timezone.utc).strftime("%H:%M UTC")

    message = f"""
🟣 <b>SOLANA PRICE UPDATE</b>

💰 <b>SOL:</b> ${price:,.2f}

{emoji} <b>24H:</b> {change:+.2f}%

🔺 <b>24H High:</b> ${high:,.2f}
🔻 <b>24H Low:</b> ${low:,.2f}

💎 <b>Market Cap:</b> ${market_cap / 1_000_000_000:.2f}B
📊 <b>24H Volume:</b> ${volume / 1_000_000_000:.2f}B

🕐 <b>Updated:</b> {updated}

⚡ @solanaalertprice
"""

    send_telegram(message)


if __name__ == "__main__":
    main()
