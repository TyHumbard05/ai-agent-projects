import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def load_rag():
    spec = importlib.util.spec_from_file_location("rag_agent", ROOT / "document-rag-agent/agent.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_normalize_search_results_assigns_local_source_ids():
    mod = load_rag()
    page = {
        "data": [
            {
                "file_id": "file_1",
                "filename": "policy.txt",
                "score": 0.91,
                "content": [{"type": "text", "text": "Refunds are allowed within 30 days."}],
            }
        ]
    }
    sources = mod.normalize_search_results(page)
    assert len(sources) == 1
    assert sources[0].source_id == "S1"
    assert sources[0].filename == "policy.txt"
    assert "30 days" in sources[0].text


def test_grounded_answer_rejects_invented_citation_ids():
    mod = load_rag()
    raw = json.dumps(
        {
            "answer": "The policy allows refunds.",
            "citation_ids": ["S99"],
            "insufficient_evidence": False,
        }
    )
    with pytest.raises(ValueError):
        mod.parse_grounded_answer(raw, {"S1", "S2"})


def test_grounded_answer_deduplicates_valid_citations():
    mod = load_rag()
    raw = json.dumps(
        {
            "answer": "The policy allows refunds.",
            "citation_ids": ["S1", "S1"],
            "insufficient_evidence": False,
        }
    )
    answer = mod.parse_grounded_answer(raw, {"S1"})
    assert answer.citation_ids == ["S1"]


def test_no_retrieval_results_returns_insufficient_evidence_without_generation():
    mod = load_rag()

    class VectorStores:
        def search(self, **kwargs):
            return {"data": []}

    class FakeClient:
        vector_stores = VectorStores()

    answer, sources = mod.answer_question("Unknown topic?", "vs_test", client=FakeClient())
    assert sources == []
    assert answer.insufficient_evidence is True
    assert answer.citation_ids == []


def test_output_payload_only_exposes_cited_source_metadata():
    mod = load_rag()
    sources = [
        mod.RetrievedSource("S1", "file_1", "one.txt", 0.9, "one"),
        mod.RetrievedSource("S2", "file_2", "two.txt", 0.8, "two"),
    ]
    answer = mod.GroundedAnswer("Supported by source two.", ["S2"], False)
    payload = mod.output_payload(answer, sources)
    assert payload["citations"] == [
        {"source_id": "S2", "file_id": "file_2", "filename": "two.txt", "score": 0.8}
    ]
