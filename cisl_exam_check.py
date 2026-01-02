#!/usr/bin/env python3

import requests
from google import genai
import os
import sys
import logging

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PUSHOVER_USER_KEY = os.getenv("PUSHOVER_USER_KEY")
PUSHOVER_APP_TOKEN = os.getenv("PUSHOVER_APP_TOKEN")

# Configure logging to stdout
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)
# Configuration
URL = "https://iiclosangeles.esteri.it/en/lingua-e-cultura/certificazioni/"
# Use a custom User-Agent to avoid being blocked as a bot
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}


def send_pushover_message(user_key, api_token, message, title=None):
    """Send a notification to Pushover. Prints errors but does not raise.

    This helper is safe to call from exception handlers.
    """
    if not user_key or not api_token:
        logger.warning("Pushover credentials not set; skipping notification.")
        return

    url = "https://api.pushover.net/1/messages.json"

    payload = {
        "token": api_token,
        "user": user_key,
        "message": message,
    }

    if title:
        payload["title"] = title

    try:
        response = requests.post(url, data=payload, timeout=10)
        response.raise_for_status()
        logger.info("Pushover: message sent successfully")
    except requests.exceptions.RequestException as e:
        logger.exception(f"Pushover: failed to send message: {e}")


def check_website():
    """Check the CISL website and return structured result.

    Returns:
        dict: {"has_more_dates": bool, "dates": str}

    Raises:
        Exception: on network, API, or parsing errors.
    """
    response = requests.get(URL, headers=HEADERS, timeout=10)
    response.raise_for_status()

    client = genai.Client(api_key=GEMINI_API_KEY)
    prompt = f"""
        Extract the information about exam dates for citizenship applicants from 
        the following HTML content:\n\n{response.text}\n\nJust output 'NONE' if 
        there are no dates or are all fully booked. Otherwise, list the available 
        dates.
        Do not include any additional text.
    """
    lm_response = client.models.generate_content(
        model="gemini-3-pro-preview",
        contents=prompt)
    result_text = lm_response.text.strip()

    if not result_text:
        return {"has_more_dates": False, "dates": None}

    if result_text.upper() == "NONE":
        return {"has_more_dates": False, "dates": None}

    # Otherwise we have some dates
    return {"has_more_dates": True, "dates": result_text}


def _main():
    try:
        result = check_website()
        if result.get("has_more_dates"):
            subject = "CISL exam dates available"
            body = f"The CISL page contains available exam dates:\n\n{result.get('dates')}\n\nSee {URL} for more details."
            send_pushover_message(
                user_key=PUSHOVER_USER_KEY,
                api_token=PUSHOVER_APP_TOKEN,
                title=subject,
                message=body,
            )
        else:
            logger.info("No available dates found; nothing to notify.")

    except Exception as e:
        # Notify about the failure
        subject = "CISL check failed"
        body = f"CISL check failed with error: {e}"
        send_pushover_message(
            user_key=PUSHOVER_USER_KEY,
            api_token=PUSHOVER_APP_TOKEN,
            title=subject,
            message=body,
        )
        logger.exception(f"Error occurred: {e}")


if __name__ == "__main__":
    _main()
