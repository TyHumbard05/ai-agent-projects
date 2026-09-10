# Support Ticket Triage Agent

A small AI agent that turns unstructured support requests into structured triage data.

It asks the model for four fields: category, priority, summary, and recommended next steps. The application validates the model output against a fixed category/priority allowlist before returning it.

## Why this project

Support queues are a good example of where an LLM is useful for interpreting messy human language, but the rest of the application still needs predictable data. This experiment focuses on that boundary: flexible language in, validated structure out.

## Run

From the repository root:

```bash
pip install -r requirements.txt
cp .env.example .env
# Add your OPENAI_API_KEY to .env
python ticket-triage-agent/agent.py "I was charged twice and need help with the duplicate payment"
```

Example shape:

```json
{
  "category": "billing",
  "priority": "medium",
  "summary": "Customer reports a duplicate charge.",
  "next_steps": ["Review the payment history", "Confirm whether a duplicate transaction occurred"]
}
```

## Concepts demonstrated

- OpenAI Responses API
- JSON-structured model output
- Output validation
- Defensive defaults
- CLI interfaces
- Separation of prompt, parsing, and application logic
