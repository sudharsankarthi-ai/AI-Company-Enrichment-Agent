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

Input Company Name:
{company_name}

Website / Domain:
{domain}


1. Determine the relationship between the input company name
and the website/domain.

IMPORTANT RULE FOR SAME COMPANY:

"same_company" refers to corporate identity, not ownership.

Set "same_company" to TRUE when:

- The input company and the company represented by the domain
  are the same corporate entity.
- The input company was officially renamed and the domain
  now represents the renamed company.
- The input company has a different legal name but is still
  the same corporate organization.

Set "same_company" to FALSE when:

- The input is a product, brand, or service owned by another
  company.
- The input is a subsidiary and the domain represents the
  parent company.
- The input is a brand operated by another company.
- The input and domain represent genuinely different
  organizations.


2. Identify the official current company name.


3. Determine whether the INPUT COMPANY ITSELF has changed
its company/corporate name.

IMPORTANT RULE FOR COMPANY NAME CHANGES:

Only set "company_name_changed" to TRUE when the company
provided in the INPUT COMPANY field has actually changed
its company/corporate name.

A different official company name does NOT automatically
mean that the company name changed.

If the input company was officially renamed into the current
company, then:

- same_company = TRUE
- company_name_changed = TRUE

If the input is simply a product, brand, subsidiary, or
service of another company, then:

- same_company = FALSE
- company_name_changed = FALSE


Examples:

Google → Google LLC

same_company = true
company_name_changed = false


Facebook → Meta Platforms, Inc.

same_company = true
company_name_changed = true


Twitter → X Corp.

same_company = true
company_name_changed = true


ChatGPT → OpenAI

same_company = false
company_name_changed = false

Reason:
ChatGPT is a product/service operated by OpenAI and was
not the previous corporate name of OpenAI.


WhatsApp → Meta Platforms, Inc.

same_company = false
company_name_changed = false

Reason:
WhatsApp is a company/product owned by Meta and was not
the previous corporate name of Meta.


Instagram → Meta Platforms, Inc.

same_company = false
company_name_changed = false

Reason:
Instagram is a brand/company owned by Meta and was not
the previous corporate name of Meta.


If the difference between the input company name and
official company name is caused by:

- product relationship
- brand relationship
- parent company
- subsidiary
- ownership
- acquisition where the acquired company retained its
  own corporate identity

DO NOT classify it as a company name change unless the
input company itself was officially renamed.


4. If the INPUT COMPANY was actually renamed:

- Set "same_company" to true.
- Set "company_name_changed" to true.
- Set "previous_company_name" to the input company name
  or its recognized previous corporate name.
- Explain the actual reason for the name change.


5. Identify:

- Official LinkedIn company page
- Current CEO
- Founder(s)


6. Assign a confidence score between 0 and 1.


IMPORTANT:

- Do not assume that different names automatically mean
  different companies.

- Do not assume that different names automatically mean
  a company name change.

- A renamed company remains the same company for this
  analysis.

- If company_name_changed is true because the input company
  was officially renamed, same_company must also be true.

- Products and brands are NOT automatically the same company
  as their parent company.

- Parent companies and subsidiaries are NOT automatically
  the same company.

- Ownership does not mean corporate identity is the same.

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
                    "Carefully distinguish corporate identity, "
                    "company renaming, products, brands, "
                    "subsidiaries, and parent companies. "
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