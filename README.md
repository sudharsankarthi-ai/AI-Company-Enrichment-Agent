# AI Company Enrichment Agent

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Gemini](https://img.shields.io/badge/Google-Gemini%202.5%20Flash-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## Overview

AI Company Enrichment Agent is an AI-powered Python application that automates company research using Google's Gemini API.

The application validates company-domain relationships and enriches datasets by retrieving:

- Official company name
- LinkedIn company page
- CEO
- Founder
- Confidence score

The enriched information is exported into a structured CSV file.

---

## Features

- Reads company data from CSV
- Validates company-domain relationships
- Retrieves LinkedIn company pages
- Finds CEO and Founder
- Uses structured JSON responses
- Exports enriched CSV reports

---

## Tech Stack

- Python
- Google Gemini 2.5 Flash
- Pandas
- Python Dotenv

---

## Project Workflow

```text
CSV Input
      │
      ▼
Load Company Data
      │
      ▼
Build AI Prompt
      │
      ▼
Gemini API
      │
      ▼
Parse JSON
      │
      ▼
Export CSV
```

---

## Installation

```bash
git clone https://github.com/sudharsankarthi-ai/AI-Company-Enrichment-Agent.git

cd AI-Company-Enrichment-Agent

pip install -r requirements.txt
```

Create a `.env` file

```env
GEMINI_API_KEY=YOUR_API_KEY
```

Run

```bash
python app.py
```

---

## Skills Demonstrated

- Python Development
- Prompt Engineering
- Gemini API Integration
- JSON Parsing
- CSV Processing
- Automation Workflows
- Error Handling

---

## Future Improvements

- Batch processing
- Retry logic
- Multi-agent architecture
- Streamlit dashboard
- Docker support

---

## License

MIT License