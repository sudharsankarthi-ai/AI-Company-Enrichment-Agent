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
