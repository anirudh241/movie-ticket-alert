import os
import requests
from dotenv import load_dotenv

# Load secrets from .env
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not BOT_TOKEN:
    raise SystemExit("Error: Telegram bot token not found in .env")


def telegram_api(method, **params):
    """Call a Telegram Bot API method."""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"

    response = requests.post(
        url,
        json=params,
        timeout=15
    )

    try:
        data = response.json()
    except ValueError:
        raise RuntimeError("Telegram returned an invalid response.")

    if not response.ok or not data.get("ok"):
        raise RuntimeError(
            data.get("description", "Telegram API request failed")
        )

    return data["result"]


try:
    # Discover your personal chat ID if not configured yet.
    if not CHAT_ID:

        updates = telegram_api("getUpdates")

        start_messages = [
            update["message"]
            for update in updates
            if "message" in update
            and update["message"].get("chat", {}).get("type") == "private"
            and update["message"].get("text", "").split()
            and update["message"]["text"].split()[0].startswith("/start")
        ]

        if not start_messages:
            raise SystemExit(
                "No /start message found. Open your bot in Telegram, "
                "press Start, and run this script again."
            )

        CHAT_ID = str(start_messages[-1]["chat"]["id"])

        print(f"Your Telegram Chat ID is: {CHAT_ID}")
        print("Save this ID in your .env file as TELEGRAM_CHAT_ID.")

    # Send our first notification!
    telegram_api(
        "sendMessage",
        chat_id=CHAT_ID,
        text=(
            "🎬 Movie Alert System\n\n"
            "Your Telegram notification pipeline is working!\n\n"
            "Dune: Part Three and Avengers: Doomsday, "
            "we're coming for those tickets."
        )
    )

    print("Success! Test notification sent.")

except requests.RequestException as error:
    print(f"Network error: {type(error).__name__}. Check your internet.")

except RuntimeError as error:
    print(f"Telegram API error: {error}")