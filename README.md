# AI Company Enrichment Agent

## Overview

AI Company Enrichment Agent is an AI-powered Python application that automates company research and data enrichment using web search and large language models.

The application validates company-domain relationships, researches companies using web sources, and enriches datasets by identifying:

- Official company name
- Company name changes
- Previous company name
- Reason for name change
- Official LinkedIn company page
- Current CEO
- Founder(s)
- Confidence score

Web research is performed using Tavily, while Groq's Llama 3.3 70B model processes, validates, and structures the collected information.

The enriched information is exported into a structured CSV file.

---

## Features

- Reads company data from CSV
- Validates company-domain relationships
- Performs live web research
- Identifies official company names
- Detects actual company name changes
- Identifies previous company names
- Provides name change reasons
- Finds official LinkedIn company pages
- Identifies current CEO
- Identifies company founders
- Uses structured JSON responses
- Assigns confidence scores
- Exports enriched CSV reports
- Handles unavailable information without inventing data

---

## Tech Stack

- Python
- Groq API
- Llama 3.3 70B
- Tavily Search API
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
Web Research
      │
      ├── Company Information
      ├── LinkedIn
      ├── CEO
      ├── Founder
      └── Company History
      │
      ▼
Build Research Context
      │
      ▼
Groq / Llama 3.3 70B
      │
      ▼
Validate & Structure Data
      │
      ▼
JSON Response
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

Create a `.env` file:

```env
GROQ_API_KEY=YOUR_API_KEY
TAVILY_API_KEY=YOUR_API_KEY
```

Run:

```bash
python app.py
```

---

## Input Format

The application accepts a CSV file with the following columns:

```csv
Company,Domain
Google,https://www.google.com
Facebook,https://www.facebook.com
ChatGPT,https://chatgpt.com
```

---

## Output

The application generates an `output.csv` file containing:

- Input Company
- Input Domain
- Same Company
- Official Company Name
- Company Name Changed
- Previous Company Name
- Name Change Reason
- LinkedIn
- CEO
- Founder
- Confidence

---

## Skills Demonstrated

- Python Development
- Prompt Engineering
- LLM Integration
- Groq API Integration
- Web Research Automation
- Tavily API Integration
- Company Data Enrichment
- JSON Parsing
- CSV Processing
- Data Validation
- Automation Workflows
- Error Handling

---

## Future Improvements

- Batch processing
- Retry logic
- Rate-limit handling
- Source verification
- Multi-agent architecture
- Streamlit dashboard
- Docker support
- Database integration

---

## License

MIT License
