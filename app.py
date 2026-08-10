"""
AI Company Enrichment Agent

Author: Sudharsan K

Description:
An AI-powered automation tool that validates company-domain relationships,
researches companies using web search, and enriches company datasets
using Groq API.
"""

import json
import os

import pandas as pd
from dotenv import load_dotenv
from groq import Groq
from tavily import TavilyClient


# =====================================================
# Configuration
# =====================================================

INPUT_FILE = "sample_input.csv"
OUTPUT_FILE = "output.csv"

MODEL_NAME = "llama-3.3-70b-versatile"

MAX_SEARCH_RESULTS = 5


# =====================================================
# Initialize Clients
# =====================================================

def initialize_clients():
    """Load environment variables and create API clients."""

    load_dotenv()

    groq_api_key = os.getenv("GROQ_API_KEY")
    tavily_api_key = os.getenv("TAVILY_API_KEY")

    if not groq_api_key:
        raise ValueError(
            "GROQ_API_KEY not found in .env file."
        )

    if not tavily_api_key:
        raise ValueError(
            "TAVILY_API_KEY not found in .env file."
        )

    groq_client = Groq(
        api_key=groq_api_key
    )

    tavily_client = TavilyClient(
        api_key=tavily_api_key
    )

    return groq_client, tavily_client


# =====================================================
# Web Research
# =====================================================

def search_company(
    tavily_client,
    company_name: str,
    domain: str
) -> list:
    """
    Search the web for company information.

    Searches for:
    - CEO and founder
    - LinkedIn
    - Official company information
    """

    queries = [
        f'"{company_name}" CEO founder',
        f'"{company_name}" LinkedIn company',
        f'"{company_name}" "{domain}" official company'
    ]

    search_results = []

    for query in queries:

        print(f"  Web search: {query}")

        try:

            response = tavily_client.search(
                query=query,
                search_depth="advanced",
                max_results=MAX_SEARCH_RESULTS
            )

            results = response.get(
                "results",
                []
            )

            for result in results:

                search_results.append(
                    {
                        "query": query,
                        "title": result.get(
                            "title",
                            ""
                        ),
                        "url": result.get(
                            "url",
                            ""
                        ),
                        "content": result.get(
                            "content",
                            ""
                        )
                    }
                )

        except Exception as error:

            print(
                f"  Search failed: {error}"
            )

    return search_results


# =====================================================
# Research Context Builder
# =====================================================

def build_research_context(
    search_results: list
) -> str:
    """
    Convert web search results into context
    that can be provided to Groq.
    """

    if not search_results:
        return "No web research results were found."

    context_parts = []

    for index, result in enumerate(
        search_results,
        start=1
    ):

        context_parts.append(
            f"""
SOURCE {index}

Search Query:
{result.get("query", "")}

Title:
{result.get("title", "")}

URL:
{result.get("url", "")}

Content:
{result.get("content", "")}
"""
        )

    return "\n".join(context_parts)


# =====================================================
# Prompt Builder
# =====================================================

def build_prompt(
    company_name: str,
    domain: str,
    research_context: str
) -> str:
    """Create the enrichment prompt sent to Groq."""

    return f"""
You are an AI Company Enrichment Agent.

You are given:

Input Company Name:
{company_name}

Website / Domain:
{domain}

You also have web research results collected from
multiple sources.

Use the web research as evidence when determining
company information.

WEB RESEARCH:

{research_context}


=====================================================
TASK 1 — COMPANY IDENTITY
=====================================================

Determine the relationship between the input company name
and the website/domain.


IMPORTANT RULE FOR SAME COMPANY:

"same_company" refers to corporate identity, not ownership.

Set "same_company" to TRUE when:

- The input company and the company represented by the domain
  are the same corporate entity.
- The input company was officially renamed and the domain
  now represents the renamed company.
- The input company has a different legal name but remains
  the same corporate organization.

Set "same_company" to FALSE when:

- The input is a product, brand, or service owned by another
  company.
- The input is a subsidiary and the domain represents the
  parent company.
- The input is a brand operated by another company.
- The input and domain represent genuinely different
  organizations.


=====================================================
TASK 2 — OFFICIAL COMPANY NAME
=====================================================

Identify the current official company name.

Use the web research as evidence.

Do not automatically treat a different legal suffix such as:

LLC
Inc.
Ltd.
Corporation
Corp.
PLC

as a company name change.


=====================================================
TASK 3 — COMPANY NAME CHANGE
=====================================================

Determine whether the INPUT COMPANY ITSELF has officially
changed its company/corporate name.

Only set:

"company_name_changed": true

when there is evidence that the input company itself was
officially renamed.

A different official company name does NOT automatically
mean that the company changed its name.


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
ChatGPT is a product/service operated by OpenAI.


WhatsApp → Meta Platforms, Inc.

same_company = false
company_name_changed = false

Reason:
WhatsApp is not the previous corporate name of Meta.


Instagram → Meta Platforms, Inc.

same_company = false
company_name_changed = false

Reason:
Instagram is not the previous corporate name of Meta.


If the difference is caused by:

- product relationship
- brand relationship
- parent company
- subsidiary
- ownership
- acquisition where the acquired company retained
  its own corporate identity

DO NOT classify it as a company name change unless
the input company itself was officially renamed.


If the input company was officially renamed:

- same_company must be true
- company_name_changed must be true
- previous_company_name should contain the previous name
- name_change_reason should explain the change


=====================================================
TASK 4 — LINKEDIN
=====================================================

Find the official LinkedIn company page.

IMPORTANT:

- Prefer the official LinkedIn company page.
- Do not return an employee's LinkedIn profile.
- Do not return a generic LinkedIn search page.
- Do not invent a LinkedIn URL.
- If the official LinkedIn company page cannot be
  established from the research, return an empty string.


=====================================================
TASK 5 — CEO
=====================================================

Identify the CURRENT CEO or equivalent current chief executive.

Use the web research.

Do not return a former CEO if a current CEO is available.

Do not guess.

If the current CEO cannot be reliably established,
return an empty string.


=====================================================
TASK 6 — FOUNDER
=====================================================

Identify the founder or founders.

Use the web research.

If multiple founders are clearly established,
return their names separated by commas.

Do not confuse:

- CEO
- current executive
- investor
- early employee

with founder.

If the founder cannot be reliably established,
return an empty string.


=====================================================
TASK 7 — CONFIDENCE
=====================================================

Assign a confidence score between 0 and 1.

The confidence score should reflect how strongly the
available web evidence supports the overall enrichment.

Higher confidence:

- Multiple sources agree
- Official website confirms information
- Official LinkedIn page is found
- Reliable sources identify the CEO/founder

Lower confidence:

- Limited search results
- Conflicting information
- Weak sources
- Company identity is unclear


=====================================================
IMPORTANT RULES
=====================================================

- Use the provided web research as evidence.
- Prefer official company sources.
- Prefer official LinkedIn pages.
- Do not invent information.
- Do not guess CEO or founder names.
- Do not guess LinkedIn URLs.
- If information is unavailable, return an empty string.
- A renamed company remains the same company.
- A product is not automatically the same company as
  its parent company.
- A subsidiary is not automatically the same company as
  its parent company.
- Ownership does not automatically mean corporate identity
  is the same.
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

def clean_json_response(
    response_text: str
) -> dict:
    """Clean Groq response and convert it into a dictionary."""

    text = response_text.strip()

    if text.startswith("```json"):
        text = text.replace(
            "```json",
            "",
            1
        )

    if text.startswith("```"):
        text = text.replace(
            "```",
            "",
            1
        )

    if text.endswith("```"):
        text = text[:-3]

    return json.loads(
        text.strip()
    )


# =====================================================
# Company Enrichment
# =====================================================

def enrich_company(
    groq_client,
    tavily_client,
    company_name: str,
    domain: str
) -> dict:
    """Research and enrich a single company."""

    print("  Starting web research...")

    search_results = search_company(
        tavily_client,
        company_name,
        domain
    )

    print(
        f"  Sources found: {len(search_results)}"
    )

    research_context = build_research_context(
        search_results
    )

    prompt = build_prompt(
        company_name,
        domain,
        research_context
    )

    print("  Sending research to Groq...")

    response = groq_client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a highly accurate company "
                    "research and enrichment assistant. "
                    "Use web evidence carefully. "
                    "Distinguish corporate identity from "
                    "products, brands, subsidiaries, and "
                    "parent companies. "
                    "Never invent CEO, founder, or LinkedIn "
                    "information. "
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

    response_text = (
        response
        .choices[0]
        .message
        .content
    )

    return clean_json_response(
        response_text
    )


# =====================================================
# Main Workflow
# =====================================================

def main():

    groq_client, tavily_client = (
        initialize_clients()
    )

    companies_df = pd.read_csv(
        INPUT_FILE
    )

    enriched_companies = []

    for _, company_record in (
        companies_df.iterrows()
    ):

        company_name = company_record[
            "Company"
        ]

        domain = company_record[
            "Domain"
        ]

        print(
            f"\nProcessing: {company_name}"
        )

        try:

            company_data = enrich_company(
                groq_client,
                tavily_client,
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

            print(
                "  Enrichment completed."
            )

        except Exception as error:

            print(
                f"  Failed to process "
                f"'{company_name}'"
            )

            print(
                f"  Error: {error}"
            )

    output_df = pd.DataFrame(
        enriched_companies
    )

    output_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\n====================================")
    print("Company enrichment completed.")
    print(
        f"Results saved to '{OUTPUT_FILE}'."
    )
    print("====================================")


# =====================================================
# Entry Point
# =====================================================

if __name__ == "__main__":
    main()
