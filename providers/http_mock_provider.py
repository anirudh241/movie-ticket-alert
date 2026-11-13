
import requests

from providers.schema import validate_listing_data


SOURCE_URL = "http://127.0.0.1:8000/mock_listings.json"


def fetch_listings():
    """Fetch movie listings over HTTP."""

    response = requests.get(
        SOURCE_URL,
        timeout=10
    )

    # Check whether the server returned a successful status.
    response.raise_for_status()

    # Convert the JSON response into a Python dictionary.
    data = response.json()

    return validate_listing_data(data)
