# CISL Exam Dates — Checker

This small script checks the CISL exam page and sends an email when available dates are detected.

## Files
- `cisl_exam_check.py` — main script that scrapes the page and uses the Gemini API to extract dates.

## Requirements
- Python 3.8+
- Install dependencies in your virtualenv (example):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # or `pip install requests google-genai`
```

## Environment variables
Set these before running the script:

- `GEMINI_API_KEY` — API key for Google Gemini (used by `google-genai`).
- `SMTP_SERVER` — SMTP host (e.g. `smtp.gmail.com`).
- `SMTP_PORT` — SMTP port (defaults to `465`).
- `SMTP_USERNAME` — SMTP username (your email address).
- `SMTP_PASSWORD` — SMTP password or app-specific password.
- `EMAIL_FROM` — optional; sender address (defaults to `SMTP_USERNAME`).
- `EMAIL_TO` — recipient email address for notifications.

Example (macOS / zsh):

```bash
export GEMINI_API_KEY="your_gemini_key"
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="465"
export SMTP_USERNAME="you@example.com"
export SMTP_PASSWORD="your_smtp_password"
export EMAIL_TO="notify-me@example.com"
python3 cisl_exam_check.py
```

Notes:
- For Gmail accounts, you may need an app password or to enable the appropriate SMTP access for your account.
- Keep credentials out of source control; prefer a secrets manager or environment variables.

## Scheduling
To run regularly, add a cron job or use a scheduler (e.g., `cron`, `launchd`, or `APScheduler`). Example cron (runs hourly):

```cron
0 * * * * cd /path/to/cisl_exam_dates && /path/to/.venv/bin/python cisl_exam_check.py
```

## Troubleshooting
- If no email is sent, check that `EMAIL_TO` and SMTP variables are set and that the script prints the extracted dates (it prints `NONE` when no dates are found).
- Check network connectivity and Gemini API quota.

---
