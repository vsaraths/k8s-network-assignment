
import os
import requests

FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://127.0.0.1:8081"
)

try:
    response = requests.get(
        f"{FRONTEND_URL}/orders",
        timeout=5
    )

    response.raise_for_status()
    print("Request successful!")
    print(response.json())

except requests.RequestException as error:
    print(f"Request failed: {error}")
