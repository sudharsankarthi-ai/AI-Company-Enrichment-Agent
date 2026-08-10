# AI Company Enrichment Agent



## Overview

AI Company Enrichment Agent is an AI-powered Python application that automates company research using the Groq API.

The application validates company-domain relationships and enriches datasets by identifying:

- Official company name
- Company name changes
- Previous company name
- Reason for name change
- LinkedIn company page
- CEO
- Founder
- Confidence score

The enriched information is exported into a structured CSV file.

---

## Features

- Reads company data from CSV
- Validates company-domain relationships
- Detects actual company name changes
- Identifies previous company names
- Provides name change reasons
- Retrieves LinkedIn company pages
- Finds CEO and Founder
- Uses structured JSON responses
- Exports enriched CSV reports

---

## Tech Stack

- Python
- Groq API
- Llama 3.3 70B
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
Groq API
      │
      ▼
Parse JSON
      │
      ▼
Company Enrichment
      │
      ▼
Export CSV
Installation
git clone https://github.com/sudharsankarthi-ai/AI-Company-Enrichment-Agent.git

cd AI-Company-Enrichment-Agent

pip install -r requirements.txt

Create a .env file

GROQ_API_KEY=YOUR_API_KEY

Run

python app.py
Skills Demonstrated
Python Development
Prompt Engineering
Groq API Integration
LLM Integration
JSON Parsing
CSV Processing
Data Enrichment
Automation Workflows
Error Handling
Future Improvements
Batch processing
Retry logic
Multi-agent architecture
Advanced company relationship detection
Streamlit dashboard
Docker support
License

MIT License
