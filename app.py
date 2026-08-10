"""
AI Company Enrichment Agent

Author: Sudharsan K

Description:
An AI-powered automation tool that validates company-domain relationships
and enriches company datasets using Groq API.
"""

import json
import os

import pandas as pd
from dotenv import load_dotenv
from groq import Groq


# =====================================================
# Configuration
# =====================================================

INPUT_FILE = "sample_input.csv"
OUTPUT_FILE = "output.csv"

MODEL_NAME = "llama-3.3-70b-versatile"


# =====================================================
# Initialize Groq Client
# =====================================================

def initialize_client():
    """Load environment variables and create a Groq client."""

    load_dotenv()

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not found in .env file."
        )

    return Groq(api_key=api_key)


# =====================================================
# Prompt Builder
# =====================================================

def build_prompt(company_name: str, domain: str) -> str:
    """Create the prompt sent to Groq."""

    return f"""
You are an AI Company Enrichment Agent.

Your job is to research and validate the relationship between
a company name and a website/domain.

Company Name:
{company_name}

Website / Domain:
{domain}

Perform the following tasks:

1. Determine whether the company name and website/domain
   belong to the same organization.

2. Identify the official current company name.

3. Check whether the company has changed its name due to:

   - acquisition
   - merger
   - rebranding
   - corporate restructuring
   - change from an old company name to a new company name

4. If the company name has changed:

   - Set "company_name_changed" to true.
   - Identify the previous company name if possible.
   - Explain the reason for the name change.

5. Identify:

   - Official LinkedIn company page
   - Current CEO
   - Founder(s)

6. Assign a confidence score between 0 and 1.

IMPORTANT:

- Do not assume that different names automatically mean
  different companies.

- A company may have changed its name after an acquisition,
  merger, rebranding, or restructuring.

- If the input company name is an old name but the website
  belongs to the same organization under its new name,
  mark "same_company" as true.

- A website may represent a product, brand, or service
  owned by a parent company.

- If the input name is a product or brand and the provided
  domain belongs to its parent company, identify the parent
  company as the official company.

- Do not mark the company as unrelated simply because the
  input name and official company name are different.

- Do not confuse a product/brand relationship with a
  company name change.

- If you cannot establish that the two names belong to the
  same organization, mark "same_company" as false.

- Do not invent information.

- If information is unavailable, return an empty string.

- Return ONLY valid JSON.

Return exactly this structure:

{{
    "same_company": true,
    "official_company_name": "",
    "company_name_changed": false,
    "previous_company_name": "",
    "name_change_reason": "",
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
    """Clean Groq response and convert it into a Python dictionary."""

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

def enrich_company(
    client,
    company_name: str,
    domain: str
) -> dict:
    """Research a single company using Groq."""

    prompt = build_prompt(
        company_name,
        domain
    )

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a highly accurate company research "
                    "and enrichment assistant. "
                    "Return only valid JSON."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        response_format={
            "type": "json_object"
        }
    )

    response_text = response.choices[0].message.content

    return clean_json_response(response_text)


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

                    "Same Company": company_data.get(
                        "same_company"
                    ),

                    "Official Company Name": company_data.get(
                        "official_company_name"
                    ),

                    "Company Name Changed": company_data.get(
                        "company_name_changed"
                    ),

                    "Previous Company Name": company_data.get(
                        "previous_company_name"
                    ),

                    "Name Change Reason": company_data.get(
                        "name_change_reason"
                    ),

                    "LinkedIn": company_data.get(
                        "linkedin"
                    ),

                    "CEO": company_data.get(
                        "ceo"
                    ),

                    "Founder": company_data.get(
                        "founder"
                    ),

                    "Confidence": company_data.get(
                        "confidence"
                    ),
                }
            )

        except Exception as error:

            print(
                f"Failed to process '{company_name}'"
            )

            print(error)

    output_df = pd.DataFrame(
        enriched_companies
    )

    output_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\n====================================")
    print("Company enrichment completed.")
    print(f"Results saved to '{OUTPUT_FILE}'.")
    print("====================================")


# =====================================================
# Entry Point
# =====================================================

if __name__ == "__main__":
    main()
