# Research Planner Agent

An AI agent that converts a broad question into a structured research plan without pretending the research has already been completed.

The output includes an objective, subquestions, search terms, evidence requirements, risks, and completion criteria.

## Why this project

A useful research agent should know the difference between **planning** and **claiming an answer**. This experiment makes that boundary explicit and produces a plan that could later be handed to search/retrieval tools.

## Run

From the repository root:

```bash
pip install -r requirements.txt
cp .env.example .env
# Add your OPENAI_API_KEY to .env
python research-planner-agent/agent.py "How are AI agents changing software engineering workflows?"
```

## Concepts demonstrated

- Research task decomposition
- Structured outputs
- Evidence planning
- Explicit uncertainty/risk tracking
- Clear completion criteria
- Provider call isolated from parsing logic
