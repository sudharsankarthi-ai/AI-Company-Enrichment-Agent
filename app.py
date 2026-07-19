"""
AI Company Enrichment Agent

Author: Sudharsan K

Description:
An AI-powered automation tool that validates company-domain relationships
and enriches company datasets using Google's Gemini API.
"""

import json
import os

import pandas as pd
from dotenv import load_dotenv
from google import genai
from google.genai import types


# =====================================================
# Configuration
# =====================================================

INPUT_FILE = "sample_input.csv"
OUTPUT_FILE = "output.csv"
MODEL_NAME = "gemini-2.5-flash"


# =====================================================
# Initialize Gemini Client
# =====================================================

def initialize_client():
    """Load environment variables and create a Gemini client."""

    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file.")

    return genai.Client(api_key=api_key)


# =====================================================
# Prompt Builder
# =====================================================

def build_prompt(company_name: str, domain: str) -> str:
    """Create the prompt sent to Gemini."""

    return f"""
You are an AI Company Enrichment Agent.

Company Name:
{company_name}

Website / Domain:
{domain}

Your tasks:

1. Verify whether the company name and domain belong to the same organization.

2. Identify:
- Official company name
- Official LinkedIn company page
- CEO
- Founder

3. Assign a confidence score between 0 and 1.

Return ONLY valid JSON in this format:

{{
    "same_company": true,
    "official_company_name": "",
    "linkedin": "",
    "ceo": "",
    "founder": "",
    "confidence": 0.0
}}
"""


# =====================================================
# JSON Cleanup
# =====================================================

def clean_json_response(response_text: str) -> dict:
    """Clean Gemini response and convert it into a Python dictionary."""

    text = response_text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "", 1)

    if text.startswith("```"):
        text = text.replace("```", "", 1)

    if text.endswith("```"):
        text = text[:-3]

    return json.loads(text.strip())


# =====================================================
# Company Research
# =====================================================

def enrich_company(client, company_name: str, domain: str) -> dict:
    """Research a single company using Gemini."""

    prompt = build_prompt(company_name, domain)

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        ),
    )

    return clean_json_response(response.text)


# =====================================================
# Main Workflow
# =====================================================

def main():

    client = initialize_client()

    companies_df = pd.read_csv(INPUT_FILE)

    enriched_companies = []

    for _, company_record in companies_df.iterrows():

        company_name = company_record["Company"]
        domain = company_record["Domain"]

        print(f"Processing: {company_name}")

        try:

            company_data = enrich_company(
                client,
                company_name,
                domain,
            )

            enriched_companies.append(
                {
                    "Input Company": company_name,
                    "Input Domain": domain,
                    "Same Company": company_data.get("same_company"),
                    "Official Company Name": company_data.get(
                        "official_company_name"
                    ),
                    "LinkedIn": company_data.get("linkedin"),
                    "CEO": company_data.get("ceo"),
                    "Founder": company_data.get("founder"),
                    "Confidence": company_data.get("confidence"),
                }
            )

        except Exception as error:

            print(f"Failed to process '{company_name}'")
            print(error)

    output_df = pd.DataFrame(enriched_companies)

    output_df.to_csv(OUTPUT_FILE, index=False)

    print("\n====================================")
    print("Company enrichment completed.")
    print(f"Results saved to '{OUTPUT_FILE}'.")
    print("====================================")


# =====================================================
# Entry Point
# =====================================================

if __name__ == "__main__":
    main()