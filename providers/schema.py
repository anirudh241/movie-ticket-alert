
def validate_listing_data(data):
    """Validate and return standardized movie listing data."""

    if not isinstance(data, dict):
        raise ValueError("Listing data must be a JSON object.")

    required_fields = [
        "movie", "cinema", "date",
        "language", "format", "shows"
    ]

    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

    for field in required_fields[:-1]:
        if not isinstance(data[field], str) or not data[field].strip():
            raise ValueError(f"Invalid or empty field: {field}")

    if not isinstance(data["shows"], list):
        raise ValueError("'shows' must be a list.")

    for index, show in enumerate(data["shows"]):

        if not isinstance(show, dict):
            raise ValueError(f"Show {index} must be an object.")

        if not show.get("session_id") or not show.get("time"):
            raise ValueError(
                f"Show {index} requires session_id and time."
            )

    return data
