# CISL Exam Dates Project - AI Agent Guidelines

## Project Purpose
Automated monitoring tool that scrapes exam dates from the Italian CISL (Certificazioni Informatica Skill Level) website and extracts relevant information using Google Gemini API.

**Key URL:** `https://iiclosangeles.esteri.it/en/lingua-e-cultura/certificazioni/`

## Architecture Overview

### Single-Entry Point Pattern
- **Main script:** `cisl_exam_check.py` - contains all logic in one file
- **Workflow:** Web scrape → HTML extraction → Gemini API analysis → Output

### External Dependencies
- **google-genai**: Google's GenAI client for Gemini model access
- **requests**: HTTP library for website scraping
- **Gemini 3 Pro**: LLM model for intelligent HTML content extraction

**Installation:** Dependencies configured in `.venv/` with pip

## Critical Implementation Details

### Web Scraping Pattern
```python
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
response = requests.get(URL, headers=HEADERS, timeout=10)
```
- **Why custom User-Agent:** Prevents bot blocking from target website
- **Timeout:** Set to 10 seconds for safety

### Gemini API Integration
- **Model:** `gemini-3-pro-preview`
- **Task:** Extract structured exam dates from unstructured HTML
- **Output handling:** API returns plain text ("NONE" for no dates, otherwise date list)

### Error Handling Convention
- Single try-except block with generic exception printing
- No custom error types or logging framework

## Workflows & Commands

### Running the Script
```bash
cd /Users/gpolles/cisl_exam_dates
/Users/gpolles/cisl_exam_dates/.venv/bin/python cisl_exam_check.py
```
Or with activated venv:
```bash
source .venv/bin/activate
python3 cisl_exam_check.py
```

## Security & Configuration Notes
- **Gemini API Key:** Hardcoded in source (review before production use)
- **Environment:** Virtual environment located at `.venv/`
- **Python Version:** 3.x (confirmed by `python3` availability)

## Known Patterns & Conventions
1. **Prompt Engineering:** Uses multi-line prompt template with context injection for reliable extraction
2. **Early Exit Design:** "NONE" response indicates no action needed by downstream systems
3. **Graceful Degradation:** Network/API errors caught but printed directly (no logging framework)

## Expansion Points
- Add logging/monitoring instead of print statements
- Implement scheduling (cron/APScheduler) for periodic checks
- Add database persistence for historical date tracking
- Integrate email notifications for date availability
