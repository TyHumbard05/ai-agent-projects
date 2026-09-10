# AI Agent Projects

![CI](https://github.com/TyHumbard05/ai-agent-projects/actions/workflows/tests.yml/badge.svg)

A collection of small, focused AI-agent experiments built to explore practical patterns such as structured outputs, task decomposition, tool routing, validation, and safe execution.

Rather than putting everything into one large chatbot, each folder isolates one agent pattern so the behavior is easier to understand, test, and improve.

## Projects

### 1. [Support Ticket Triage Agent](./ticket-triage-agent)

Turns unstructured customer-support text into validated structured data:

- category
- priority
- summary
- recommended next steps

**Focus:** structured model output, validation, defensive defaults, and separating untrusted user text from agent instructions.

### 2. [Research Planner Agent](./research-planner-agent)

Converts a broad research question into a plan containing:

- objective
- subquestions
- search terms
- evidence requirements
- risks
- completion criteria

**Focus:** task decomposition and making a clear distinction between planning research and claiming that research has already been completed.

### 3. [Safe Tool Router Agent](./tool-router-agent)

Lets an LLM choose from a small allowlist of local tools, then validates the decision before application code executes it.

Current tools:

- arithmetic calculator
- text statistics
- to-do list parser
- safe `none` fallback

**Focus:** tool routing, capability boundaries, fail-closed behavior, and safe local execution. The calculator uses a restricted Python AST evaluator rather than `eval()` and limits expression size, complexity, numeric magnitude, and exponent size.

## Common Architecture

```text
User input
    |
    v
Agent instructions + allowed output/tool policy
    |
    v
OpenAI Responses API
    |
    v
Structured JSON response
    |
    v
Application validation
    |
    +--> reject / normalize unsafe or unexpected output
    |
    v
Return result or execute an allowlisted local tool
```

A recurring design goal across these experiments is that the language model interprets intent, while normal application code controls what data and capabilities are actually accepted.

## Setup

Requires Python 3.11+.

```bash
git clone https://github.com/TyHumbard05/ai-agent-projects.git
cd ai-agent-projects

python -m venv .venv
source .venv/bin/activate       # Linux/macOS
# .venv\Scripts\activate        # Windows PowerShell

pip install -r requirements.txt
cp .env.example .env
```

Add your API key to `.env`:

```env
OPENAI_API_KEY=your_key_here
```

The `.env` file is ignored by Git and should never be committed.

## Tests

```bash
pytest -q
```

The repository also includes a GitHub Actions workflow that runs the tests on pushes and pull requests.

## What This Repository Demonstrates

- OpenAI Responses API integration
- Structured JSON outputs
- Prompt/instruction separation
- Input and output validation
- Agent task decomposition
- Tool selection and routing
- Capability allowlists
- Safe arithmetic execution without `eval()`
- Fail-closed behavior
- Automated testing and CI

## Status

**Active development.** These are deliberately small experiments. More agents will be added as I explore retrieval, multi-step workflows, evaluation, memory/state, and human-in-the-loop approval patterns.

## Related Project

For a larger end-to-end automation project, see my [AI Lead Generation Agent](https://github.com/TyHumbard05/ai-lead-generation-agent).
