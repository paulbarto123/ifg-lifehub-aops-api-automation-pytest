import requests

def post_api_request(url: str, api_key: str, payload: dict, timeout: int = 30) -> dict:
    """
    Reusable function to send POST API requests.

    :param url: Full API endpoint URL
    :param api_key: API key for authentication
    :param payload: Request body (dict)
    :param timeout: Request timeout in seconds
    :return: Parsed JSON response (dict)
    :raises: requests.HTTPError for non-2xx responses
    """

    headers = {
        "apiKey": api_key,
        "Content-Type": "application/json"
    }

    response = requests.post(
        url=url,
        headers=headers,
        json=payload,
        timeout=timeout
    )

    # Raise exception if request failed
    response.raise_for_status()

    return response.json()