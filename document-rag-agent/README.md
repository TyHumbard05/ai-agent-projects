# Document RAG Agent

A small retrieval-augmented generation example that answers questions from documents indexed in an OpenAI vector store.

The goal is not just to retrieve text. The agent keeps the generation step grounded in retrieved evidence and validates citations before returning them.

## What It Demonstrates

- OpenAI vector-store search
- Retrieval-augmented generation (RAG)
- Strict Structured Outputs with JSON Schema
- Grounded answering from retrieved excerpts only
- Citation validation
- Prompt-injection resistance for retrieved document text
- Explicit insufficient-evidence behavior

## Flow

```text
Question
   |
   v
Vector store search
   |
   v
Top relevant document chunks
   |
   v
Assign local source IDs (S1, S2, ...)
   |
   v
Grounded model answer
   |
   v
Validate cited IDs against retrieved sources
   |
   v
Answer + source metadata
```

The model never gets permission to invent arbitrary citations. Application code assigns source IDs after retrieval and rejects any citation ID that was not actually retrieved.

## Setup

From the repository root:

```bash
pip install -r requirements.txt
cp .env.example .env
```

Set:

```env
OPENAI_API_KEY=your_key_here
OPENAI_VECTOR_STORE_ID=vs_your_vector_store_id
```

This example assumes you already have an OpenAI vector store containing documents. It intentionally focuses on the retrieval and grounded-answering layer rather than document-upload lifecycle management.

## Run

```bash
python document-rag-agent/agent.py "What does the policy say about refunds?"
```

Or supply the vector store directly:

```bash
python document-rag-agent/agent.py \
  "What does the policy say about refunds?" \
  --vector-store-id vs_123 \
  --max-results 5
```

Example output shape:

```json
{
  "answer": "...",
  "insufficient_evidence": false,
  "citations": [
    {
      "source_id": "S1",
      "file_id": "file_123",
      "filename": "refund-policy.pdf",
      "score": 0.91
    }
  ]
}
```

## Safety / Reliability Notes

Retrieved text is treated as untrusted evidence. Instructions embedded inside documents are not allowed to override the agent's grounding policy. If retrieval returns no useful evidence, the agent returns an insufficient-evidence result instead of fabricating an answer.

## Why This Is Useful

Many practical AI systems need to answer questions from private or domain-specific information rather than from model memory. This project demonstrates the core pattern behind those systems while keeping retrieval, generation, and citation validation clearly separated.
