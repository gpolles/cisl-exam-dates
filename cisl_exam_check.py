#!/usr/bin/env python3

import requests
from google import genai
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PUSHOVER_USER_KEY = os.getenv("PUSHOVER_USER_KEY")
PUSHOVER_APP_TOKEN = os.getenv("PUSHOVER_APP_TOKEN")
# Configuration
URL = "https://iiclosangeles.esteri.it/en/lingua-e-cultura/certificazioni/"
# Use a custom User-Agent to avoid being blocked as a bot
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

def send_pushover_message(user_key, api_token, message, title=None):
    """
    Sends a notification to a device via Pushover.
    """
    url = "https://api.pushover.net/1/messages.json"

    payload = {
        "token": api_token,
        "user": user_key,
        "message": message,
    }

    # Add optional title if provided
    if title:
        payload["title"] = title

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status() # Raise an error for bad responses (4xx, 5xx)

        print("Message sent successfully!")
        print(f"Server Response: {response.json()}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to send message: {e}")

def check_website():
    try:
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
        print(result_text)

        if result_text and result_text.upper() != "NONE":
            subject = "CISL exam dates available"
            body = f"The CISL page contains available exam dates:\n\n{result_text}. See {URL} for more details."
            send_pushover_message(
                user_key=PUSHOVER_USER_KEY,
                api_token=PUSHOVER_APP_TOKEN,
                title=subject,
                message=body
            )

    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    check_website()