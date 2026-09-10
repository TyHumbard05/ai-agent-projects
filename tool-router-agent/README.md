# Safe Tool Router Agent

A small tool-using agent that lets an LLM choose from a strict allowlist of local functions, then validates the choice before any tool executes.

Available tools:

- `calculator` — arithmetic only
- `text_stats` — word/character/line counts
- `todo_parser` — turns rough list text into clean tasks
- `none` — safe fallback when no tool fits

## Why this project

Tool calling is one of the most useful agent patterns, but blindly executing model-generated actions is dangerous. This project demonstrates a simple security boundary: **the model chooses intent, application code controls capability**.

The calculator uses Python's AST rather than `eval()`, and unrecognized tools are converted to `none`.

## Run

From the repository root:

```bash
pip install -r requirements.txt
cp .env.example .env
# Add your OPENAI_API_KEY to .env
python tool-router-agent/agent.py "Calculate (17 * 4) + 9"
```

## Concepts demonstrated

- LLM tool routing
- Allowlisted capabilities
- Safe arithmetic evaluation
- Structured decision validation
- Separation of model choice from tool execution
- Fail-closed behavior
