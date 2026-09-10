import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_ticket_parser_normalizes_unknown_values():
    mod = load("ticket", "ticket-triage-agent/agent.py")
    result = mod.parse_triage(json.dumps({
        "category": "mystery", "priority": "mega", "summary": "Login issue", "next_steps": "reset"
    }))
    assert result.category == "other"
    assert result.priority == "medium"
    assert result.next_steps == ["reset"]


def test_ticket_parser_accepts_valid_output():
    mod = load("ticket2", "ticket-triage-agent/agent.py")
    result = mod.parse_triage(json.dumps({
        "category": "bug", "priority": "high", "summary": "Crash", "next_steps": ["collect logs"]
    }))
    assert result.category == "bug"
    assert result.priority == "high"


def test_research_parser_normalizes_lists():
    mod = load("research", "research-planner-agent/agent.py")
    result = mod.parse_plan(json.dumps({
        "objective": "Compare approaches",
        "subquestions": "What differs?",
        "search_terms": ["alpha", "beta"],
        "evidence_needed": [], "risks": ["stale data"], "completion_criteria": ["3 sources"]
    }))
    assert result.subquestions == ["What differs?"]
    assert result.search_terms == ["alpha", "beta"]


def test_research_instructions_do_not_answer():
    mod = load("research2", "research-planner-agent/agent.py")
    assert "Do not answer the question" in mod.build_instructions()


def test_calculator_allows_arithmetic():
    mod = load("router", "tool-router-agent/agent.py")
    assert mod.safe_calculate("(2 + 3) * 4") == 20.0


def test_calculator_rejects_code_execution():
    mod = load("router2", "tool-router-agent/agent.py")
    try:
        mod.safe_calculate("__import__('os').system('echo nope')")
    except ValueError:
        pass
    else:
        raise AssertionError("unsafe expression was not rejected")


def test_calculator_rejects_huge_exponent():
    mod = load("router3", "tool-router-agent/agent.py")
    try:
        mod.safe_calculate("2 ** 100000")
    except ValueError:
        pass
    else:
        raise AssertionError("huge exponent was not rejected")


def test_router_rejects_unlisted_tool():
    mod = load("router4", "tool-router-agent/agent.py")
    decision = mod.parse_decision('{"tool":"shell","argument":"rm -rf /","reason":"no"}')
    assert decision.tool == "none"


def test_text_stats():
    mod = load("router5", "tool-router-agent/agent.py")
    assert mod.text_stats("hello world") == {"characters": 11, "words": 2, "lines": 1}


def test_todo_parser():
    mod = load("router6", "tool-router-agent/agent.py")
    assert mod.todo_parser("- finish README\n- run tests") == ["finish README", "run tests"]
