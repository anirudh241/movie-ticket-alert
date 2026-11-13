
import json
from pathlib import Path

from providers.schema import validate_listing_data


DATA_FILE = Path(__file__).resolve().parent.parent / "mock_listings.json"


def fetch_listings():
    """Fetch listings from the local mock JSON file."""

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return validate_listing_data(data)
