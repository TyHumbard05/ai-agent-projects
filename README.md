# AI Agent Projects

![CI](https://github.com/TyHumbard05/ai-agent-projects/actions/workflows/tests.yml/badge.svg)

A collection of small, focused AI-agent experiments built to explore practical patterns such as **Structured Outputs, task decomposition, tool routing, retrieval, grounding, validation, and safe execution**.

Rather than putting everything into one large chatbot, each folder isolates one agent pattern so the behavior is easier to understand, test, and improve.

## Projects

### 1. [Support Ticket Triage Agent](./ticket-triage-agent)

Turns unstructured customer-support text into validated structured data:

- category
- priority
- summary
- recommended next steps

**Focus:** strict JSON Schema output, defensive validation, conservative prioritization, and separating untrusted user text from agent instructions.

### 2. [Research Planner Agent](./research-planner-agent)

Converts a broad research question into a plan containing:

- objective
- subquestions
- search terms
- evidence requirements
- risks
- completion criteria

**Focus:** task decomposition, Structured Outputs, and making a clear distinction between planning research and claiming that research has already been completed.

### 3. [Safe Tool Router Agent](./tool-router-agent)

Lets an LLM choose from a small allowlist of local tools, then validates the decision before application code executes it.

Current tools:

- arithmetic calculator
- text statistics
- to-do list parser
- safe `none` fallback

**Focus:** tool routing, capability boundaries, strict tool-selection schema, fail-closed behavior, and safe local execution. The calculator uses a restricted Python AST evaluator rather than `eval()` and limits expression size, complexity, numeric magnitude, and exponent size.

### 4. [Document RAG Agent](./document-rag-agent)

Answers questions from documents stored in an OpenAI vector store.

The agent retrieves relevant chunks, assigns local source IDs, asks the model to answer only from those excerpts, and validates every citation before returning it.

**Focus:** retrieval-augmented generation, vector search, grounding, citation validation, insufficient-evidence behavior, and treating retrieved documents as untrusted data.

## Common Architecture

```text
User input
    |
    v
Agent instructions / capability policy
    |
    v
OpenAI Responses API
    |
    v
Strict JSON Schema output
    |
    v
Application validation
    |
    +--> reject / normalize unexpected output
    |
    v
Return result or execute an allowlisted capability
```

For the RAG project, retrieval happens before generation:

```text
Question -> vector search -> retrieved chunks -> grounded generation -> citation validation
```

A recurring design goal across these experiments is that the language model interprets intent, while normal application code controls what data, sources, citations, and capabilities are actually accepted.

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
OPENAI_MODEL=gpt-5.5
```

For the document RAG agent, also set a vector store containing your indexed documents:

```env
OPENAI_VECTOR_STORE_ID=vs_your_vector_store_id
```

The `.env` file is ignored by Git and should never be committed.

## Tests

```bash
pytest -q
```

The repository also includes a GitHub Actions workflow that runs the tests on pushes and pull requests.

## What This Repository Demonstrates

- OpenAI Responses API integration
- Strict Structured Outputs with JSON Schema
- Prompt/instruction separation
- Input and output validation
- Agent task decomposition
- Tool selection and routing
- Capability allowlists
- Safe arithmetic execution without `eval()`
- OpenAI vector-store retrieval
- Retrieval-augmented generation (RAG)
- Grounded answers with citation validation
- Fail-closed and insufficient-evidence behavior
- Automated testing and CI

## Design Principles

- **Constrain model output:** schemas define the shape and allowed values before application code accepts a response.
- **Keep capabilities explicit:** the model can select only from tools or sources the application exposes.
- **Validate again in code:** Structured Outputs reduce malformed responses, but application-side validation still protects capability boundaries and citations.
- **Treat external text as untrusted:** user prompts and retrieved documents cannot redefine system policy.
- **Fail safely:** uncertainty should produce a fallback or insufficient-evidence result rather than fabricated certainty.
- **Keep examples understandable:** each project is intentionally small enough to read in one sitting.

## Status

**Active development.** The repository currently includes four runnable experiments covering structured classification, research planning, safe tool routing, and grounded document retrieval. Future additions may explore multi-step orchestration, evaluations, persistent state, and human approval workflows.

## Related Project

For a larger end-to-end automation project, see my [AI Lead Generation Agent](https://github.com/TyHumbard05/ai-lead-generation-agent).
