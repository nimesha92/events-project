import os

import requests

LAMBDA_FUNCTION_URL = os.getenv("LAMBDA_FUNCTION_URL")


def trigger_low_seat_notification(
    event_id: int,
    remaining_seats: int,
) -> None:
    if not LAMBDA_FUNCTION_URL:
        print("LAMBDA_FUNCTION_URL is not configured")
        return

    payload = {
        "event_id": event_id,
        "remaining_seats": remaining_seats,
    }

    try:
        response = requests.post(
            LAMBDA_FUNCTION_URL,
            json=payload,
            timeout=10,
        )

        response.raise_for_status()

        print(
            "Low-seat notification triggered:",
            response.json(),
        )

    except requests.RequestException as error:
        print(
            "Failed to trigger Lambda:",
            error,
        )