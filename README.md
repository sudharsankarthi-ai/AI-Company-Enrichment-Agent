AI Company Enrichment Agent

An AI-powered Python automation tool that validates company-domain relationships and enriches company datasets using the Groq API and Llama 3.3 70B.

The agent takes a list of company names and domains as input, analyzes their relationship, identifies company information, detects potential company name changes, and exports the results into a structured CSV file.

Overview

Company datasets often contain incomplete, outdated, or inconsistent information.

For example:

A company may have changed its name after a rebranding.
A company may operate under a different official corporate name.
A product or brand may belong to a larger parent company.
Company records may contain inconsistent naming.
Important information such as CEO, founder, or LinkedIn details may be missing.

The AI Company Enrichment Agent automates the initial enrichment and validation process using an LLM-powered workflow.

Key Features
Reads company data from a CSV file
Validates company-domain relationships
Identifies the official company name
Detects potential company name changes
Identifies previous company names
Provides a reason for detected name changes
Retrieves LinkedIn company information
Identifies CEO and founder(s)
Generates a confidence score between 0 and 1
Uses structured JSON responses from the LLM
Handles individual company processing errors
Exports enriched results to CSV
Example Input

The input CSV contains two columns:

Company,Domain
google,https://www.google.com/
facebook,https://www.facebook.com/
chatgpt,https://chatgpt.com/
Example Output

The agent generates an enriched CSV containing:

Input Company	Official Company Name	Same Company	Name Changed	CEO	Confidence
google	Google LLC	True	False	Sundar Pichai	0.99
facebook	Meta Platforms, Inc.	True	True	Mark Zuckerberg	0.99
chatgpt	OpenAI	True	False	Sam Altman	0.90

The complete output includes:

Input Company
Input Domain
Same Company
Official Company Name
Company Name Changed
Previous Company Name
Name Change Reason
LinkedIn
CEO
Founder
Confidence
Project Workflow
CSV Input
    │
    ▼
Load Company Data
    │
    ▼
Build AI Research Prompt
    │
    ▼
Groq API
(Llama 3.3 70B)
    │
    ▼
Structured JSON Response
    │
    ▼
Validate & Extract Company Data
    │
    ▼
Generate Enriched CSV
How It Works
1. Input Processing

The application reads company names and domains from sample_input.csv using Pandas.

2. AI Prompt Generation

A structured prompt is generated for each company containing:

Company name
Website/domain
Company-domain validation requirements
Company name-change detection requirements
Enrichment fields
3. LLM Processing

The prompt is sent to the Groq API using Llama 3.3 70B.

The model analyzes the provided company and returns structured JSON.

4. JSON Processing

The application cleans and parses the AI response using Python's JSON parser.

5. Data Enrichment

The extracted information is mapped into structured fields including:

Official company name
LinkedIn
CEO
Founder
Name-change information
Confidence score
6. CSV Export

The final enriched dataset is exported as:

output.csv
Tech Stack
Python
Groq API
Llama 3.3 70B
Pandas
Python-dotenv
JSON
CSV
Installation
1. Clone the repository
git clone https://github.com/sudharsankarthi-ai/AI-Company-Enrichment-Agent.git
2. Navigate into the project
cd AI-Company-Enrichment-Agent
3. Install dependencies
pip install -r requirements.txt
4. Configure the API key

Create a .env file in the project directory:

GROQ_API_KEY=YOUR_API_KEY

Do not commit your .env file to GitHub.

5. Run the application
python app.py

The enriched results will be saved to:

output.csv
Project Structure
AI-Company-Enrichment-Agent/
│
├── app.py
├── sample_input.csv
├── output.csv
├── requirements.txt
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
Skills Demonstrated
Python Development
API Integration
LLM Integration
Prompt Engineering
Structured JSON Generation
JSON Parsing
CSV Processing
Data Enrichment
Data Validation
Automation Workflows
Error Handling
Environment Variable Management
Why This Project?

The project demonstrates how LLMs can be integrated into practical data workflows rather than being used only for conversational applications.

The goal is to automate repetitive company research and transform raw company-domain data into a more structured and useful dataset.

Current Capabilities

The current version focuses on:

Company → Domain → AI Validation → Enrichment → CSV

It is intentionally designed as a lightweight Python automation tool.

Future Improvements

Potential future versions could include:

Web-based company verification
External data-source verification
Batch processing optimization
Retry and rate-limit handling
More detailed company relationship classification
Acquisition and merger detection
Product-to-parent-company classification
Multi-agent research architecture
Streamlit dashboard
Docker deployment
Database integration
License

MIT License

Author

Sudharsan K

GitHub:
https://github.com/sudharsankarthi-ai
