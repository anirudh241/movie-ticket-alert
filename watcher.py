from providers.http_mock_provider import fetch_listings
import json
import time
from pathlib import Path

import requests

from notifier import send_telegram_message


# Project configuration
BASE_DIR = Path(__file__).resolve().parent

LISTINGS_FILE = BASE_DIR / "mock_listings.json"
STATE_FILE = BASE_DIR / "watcher_state.json"

CHECK_INTERVAL = 10  # Seconds (temporary testing interval)


def load_listings():
    """Read the current movie listings from our mock provider."""

    with open(LISTINGS_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict) or not isinstance(data.get("shows"), list):
        raise ValueError("Invalid listing data structure.")

    return data


def load_state():
    """Load IDs of previously notified showtimes."""

    if not STATE_FILE.exists():
        return set()

    with open(STATE_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return set(data["notified_session_ids"])


def save_state(notified_ids):
    """Persist notified show IDs to prevent duplicate alerts."""

    temporary_file = STATE_FILE.with_suffix(".tmp")

    data = {
        "notified_session_ids": sorted(notified_ids)
    }

    with open(temporary_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    temporary_file.replace(STATE_FILE)


def format_notification(movie_data, show):
    """Construct a readable movie booking notification."""

    return (
        "🎬 BOOKINGS OPEN!\n\n"
        f"{movie_data['movie']}\n"
        f"{movie_data['cinema']}\n\n"
        f"Date: {movie_data['date']}\n"
        f"Language: {movie_data['language']}\n"
        f"Format: {movie_data['format']}\n"
        f"Showtime: {show['time']}\n"
    )


def run_watcher():

    notified_ids = load_state()

    print("🎬 Movie Ticket Watcher started!")
    print(f"Checking every {CHECK_INTERVAL} seconds.")

    while True:

        try:
            movie_data = fetch_listings()

            new_shows = 0

            for show in movie_data["shows"]:

                session_id = show.get("session_id")

                if not session_id:
                    print("Skipping show without a session ID.")
                    continue

                session_id = str(session_id)

                # Skip previously notified showtimes
                if session_id in notified_ids:
                    continue

                message = format_notification(movie_data, show)

                # Send notification
                send_telegram_message(message)

                # Save only after successful delivery
                notified_ids.add(session_id)
                save_state(notified_ids)

                print(f"New showtime detected: {show['time']}")

                new_shows += 1

            if new_shows == 0:
                print("No new showtimes detected.")

        except (
            OSError,
            ValueError,
            requests.RequestException,
            RuntimeError
        ) as error:

            print(f"Monitoring error: {error}")

        print(f"Next check in {CHECK_INTERVAL} seconds...\n")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":

    try:
        run_watcher()

    except KeyboardInterrupt:
        print("\nWatcher stopped by user.")
