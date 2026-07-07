# Multi-Provider LLM Starter Kit

A production-style Python starter kit for building LLM applications with multiple providers, clean architecture, structured outputs, streaming responses, logging, error handling, tests, and a FastAPI deployment roadmap.

This project is part of an AI Engineer portfolio track. It demonstrates how to move beyond simple chatbot scripts and build maintainable LLM application foundations that can later support APIs, RAG systems, workflow automation, and cloud deployment.

## Current Status

Phase 1B complete:

* Project foundation built
* Mock provider implemented
* Gemini, Groq, and Mistral clients added
* Provider factory added
* Streaming supported
* Structured complaint analysis working
* Robust JSON cleaning and parsing added
* Unit tests passing

## Purpose

The goal of this project is to create a reusable starter kit for AI applications that can work with multiple LLM providers through a consistent interface.

Instead of writing application logic directly around one provider, the project uses a provider abstraction pattern:

```python
client = get_llm_client(provider_name)
response = client.generate(prompt)
```

This makes the application easier to extend, test, and adapt to different providers.

## Supported Providers

Current providers:

* Mock provider for local development and tests
* Google Gemini
* Groq
* Mistral

The mock provider is used to test application logic without making live API calls.

## Key Features

* Clean `src/` Python project layout
* Environment-based configuration
* Safe `.env.example` template
* Custom exception classes
* Logging setup
* Provider interface using a shared client contract
* Provider factory for clean provider selection
* Mock LLM client
* Gemini client
* Groq client
* Mistral client
* Standard text generation
* Streaming generation
* Banking complaint triage prompt
* Structured JSON output parsing
* JSON response cleanup for common LLM formatting issues
* Pydantic validation for structured outputs
* Local CLI demo runner
* Unit tests with pytest
* Pyright/Pylance configuration for `src/` layout

## Repository Structure

```text
multi-provider-llm-starter-kit/
│
├── src/
│   └── multi_provider_llm/
│       ├── __init__.py
│       ├── config.py
│       ├── exceptions.py
│       ├── run_demo.py
│       │
│       ├── clients/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── factory.py
│       │   ├── mock_client.py
│       │   ├── gemini_client.py
│       │   ├── groq_client.py
│       │   └── mistral_client.py
│       │
│       ├── prompts/
│       │   ├── __init__.py
│       │   └── complaint_prompts.py
│       │
│       ├── services/
│       │   ├── __init__.py
│       │   └── complaint_service.py
│       │
│       └── utils/
│           ├── __init__.py
│           └── logging_config.py
│
├── tests/
│   ├── test_mock_client.py
│   ├── test_complaint_service.py
│   └── test_provider_factory.py
│
├── .env.example
├── .gitignore
├── pytest.ini
├── pyrightconfig.json
├── requirements.txt
└── README.md
```

## Setup

Clone the repository:

```bash
git clone <your-repo-url>
cd multi-provider-llm-starter-kit
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/Scripts/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a local `.env` file:

```bash
cp .env.example .env
```

Example configuration:

```env
APP_NAME=Multi-Provider LLM Starter Kit
ENVIRONMENT=development
LOG_LEVEL=INFO

# Provider options: mock, gemini, groq, mistral
DEFAULT_PROVIDER=mock

# App settings
MAX_OUTPUT_TOKENS=600
TEMPERATURE=0.2

# Gemini
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash

# Groq
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant

# Mistral
MISTRAL_API_KEY=your_mistral_api_key_here
MISTRAL_MODEL=mistral-small-latest
```

The `.env` file should never be committed to GitHub. It is already included in `.gitignore`.

## Running Tests

Run the full test suite:

```bash
pytest
```

The tests cover:

* mock provider behaviour
* empty prompt validation
* streaming interface
* complaint prompt construction
* structured complaint analysis
* JSON response parsing
* JSON cleanup from markdown fences
* invalid JSON rejection
* provider factory behaviour
* unsupported provider rejection

The unit tests do not call live LLM APIs. This keeps the test suite fast, reliable, and free from API usage costs.

## Running the Local Demo

Run the default mock provider:

```bash
PYTHONPATH=src python src/multi_provider_llm/run_demo.py --provider mock
```

Run Gemini:

```bash
PYTHONPATH=src python src/multi_provider_llm/run_demo.py --provider gemini
```

Run Groq:

```bash
PYTHONPATH=src python src/multi_provider_llm/run_demo.py --provider groq
```

Run Mistral:

```bash
PYTHONPATH=src python src/multi_provider_llm/run_demo.py --provider mistral
```

## Streaming Mode

Run streaming output with the mock provider:

```bash
PYTHONPATH=src python src/multi_provider_llm/run_demo.py --provider mock --stream
```

Run streaming with Gemini:

```bash
PYTHONPATH=src python src/multi_provider_llm/run_demo.py --provider gemini --stream
```

Streaming is useful for chatbots, copilots, document assistants, RAG systems, and any AI application where users should see output as it is generated.

## Structured Complaint Analysis

Run structured complaint analysis with the mock provider:

```bash
PYTHONPATH=src python src/multi_provider_llm/run_demo.py --provider mock --analyse-complaint
```

Run it with Gemini:

```bash
PYTHONPATH=src python src/multi_provider_llm/run_demo.py --provider gemini --analyse-complaint
```

Run it with Groq:

```bash
PYTHONPATH=src python src/multi_provider_llm/run_demo.py --provider groq --analyse-complaint
```

Run it with Mistral:

```bash
PYTHONPATH=src python src/multi_provider_llm/run_demo.py --provider mistral --analyse-complaint
```

Example output:

```json
{
  "summary": "Customer reports a deducted QR payment that the merchant did not receive.",
  "category": "payment_dispute",
  "urgency": "high",
  "needs_human_review": true,
  "recommended_action": "Check transaction status and merchant settlement records."
}
```

## Banking and Fintech Use Case

The structured output example focuses on banking complaint triage.

The system analyses a customer complaint and returns:

* summary
* complaint category
* urgency
* whether human review is required
* recommended operational action

This pattern can support workflows such as:

* payment dispute triage
* QR payment issue routing
* duplicate card charge review
* mobile banking support
* failed transfer escalation
* customer support automation

Although the example is banking-focused, the same architecture can be reused for insurance, legal operations, healthcare administration, SaaS support, HR case routing, and internal enterprise automation.

## Provider Abstraction

Each provider follows the same interface:

```python
generate(prompt: str) -> str
generate_stream(prompt: str) -> Iterator[str]
```

This means the rest of the application does not need to know the details of each provider SDK.

Current client classes:

* `MockLLMClient`
* `GeminiClient`
* `GroqClient`
* `MistralClient`

Provider selection is handled centrally by:

```python
get_llm_client(provider_name)
```

This keeps future FastAPI endpoints clean and makes it easier to add more providers later.

## Structured Output Handling

LLM outputs are not always perfectly formatted. This project includes a structured output service that:

* builds a complaint triage prompt
* calls the selected LLM provider
* cleans common JSON formatting issues
* removes markdown JSON fences if present
* extracts the JSON object from surrounding text
* parses the response with `json.loads`
* validates the schema using Pydantic
* raises clear custom errors when parsing or validation fails

This is important because production AI applications need reliable data, not just natural language responses.

## Error Handling

The project uses custom exceptions:

* `LLMStarterKitError`
* `LLMProviderError`
* `MissingAPIKeyError`
* `UnsupportedProviderError`
* `StructuredOutputError`

This makes failures easier to understand and debug.

## Logging

The project includes central logging configuration.

The app logs useful operational behaviour such as:

* selected provider
* demo start
* application errors

It avoids logging API keys or sensitive customer data.

## Skills Demonstrated

This project demonstrates:

* Python application structure
* LLM API integration
* multi-provider architecture
* provider abstraction
* provider factory pattern
* streaming responses
* structured JSON outputs
* prompt template design
* Pydantic validation
* error handling
* logging
* pytest unit testing
* `.env` configuration management
* `src/` layout project setup
* Pyright/Pylance configuration
* banking and fintech workflow thinking

## Current Limitations

This project is still in progress.

Current limitations:

* No FastAPI backend yet
* No deployed API service yet
* No frontend UI yet
* No Dockerfile yet
* No GitHub Actions workflow yet
* No RAG or vector database integration yet
* No database persistence
* No authentication or user management
* No token/cost tracking yet
* No production monitoring yet

These are planned for later phases.

## Roadmap

Planned next phases:

1. Add FastAPI backend
2. Add `/health` endpoint
3. Add `/generate` endpoint
4. Add streaming API endpoint
5. Add `/complaints/analyse` endpoint
6. Add request/response schemas
7. Add API endpoint tests
8. Add Docker support
9. Add GitHub Actions CI
10. Add improved documentation with API examples
11. Extend into RAG and automation projects later

## Portfolio Relevance

This project is designed to be a professional AI Engineer portfolio project.

It shows the ability to build an LLM application foundation with clean architecture, multiple providers, structured outputs, streaming, tests, and realistic business use cases.

The project is intentionally designed to grow into a backend service and later support larger AI systems such as RAG assistants, workflow automation tools, and enterprise copilots.
