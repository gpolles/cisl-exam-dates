#!/usr/bin/env python3

import requests
from google import genai
import os
import smtplib
import ssl
from email.message import EmailMessage

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# Configuration
URL = "https://iiclosangeles.esteri.it/en/lingua-e-cultura/certificazioni/"
# Use a custom User-Agent to avoid being blocked as a bot
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

# Email configuration (read from environment)
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM", SMTP_USERNAME)
EMAIL_TO = os.getenv("EMAIL_TO")

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
            body = f"The CISL page contains available exam dates:\n\n{result_text}"
            send_email(subject, body)

    except Exception as e:
        print(f"Error occurred: {e}")


def send_email(subject: str, body: str):
    if not SMTP_SERVER or not SMTP_USERNAME or not SMTP_PASSWORD or not EMAIL_TO:
        print("Email settings not fully configured; skipping email send.")
        return

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg.set_content(body)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        print(f"Email sent to {EMAIL_TO}")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    check_website()