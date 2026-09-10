import argparse
import json
import os
from dataclasses import dataclass, asdict

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


@dataclass
class ResearchPlan:
    objective: str
    subquestions: list[str]
    search_terms: list[str]
    evidence_needed: list[str]
    risks: list[str]
    completion_criteria: list[str]


def build_prompt(question: str) -> str:
    return f"""Create a research plan for the question below. Do not answer the question.
Return JSON only with these keys:
objective, subquestions, search_terms, evidence_needed, risks, completion_criteria.
All fields except objective must be arrays of concise strings.

Research question:
{question.strip()}
"""


def _list(data: dict, key: str) -> list[str]:
    value = data.get(key) or []
    if not isinstance(value, list):
        value = [value]
    return [str(item).strip() for item in value if str(item).strip()]


def parse_plan(raw: str) -> ResearchPlan:
    data = json.loads(raw)
    return ResearchPlan(
        objective=str(data.get("objective", "")).strip(),
        subquestions=_list(data, "subquestions"),
        search_terms=_list(data, "search_terms"),
        evidence_needed=_list(data, "evidence_needed"),
        risks=_list(data, "risks"),
        completion_criteria=_list(data, "completion_criteria"),
    )


def plan(question: str, client: OpenAI | None = None, model: str | None = None) -> ResearchPlan:
    api = client or OpenAI()
    response = api.responses.create(
        model=model or os.getenv("OPENAI_MODEL", "gpt-5.5"),
        input=build_prompt(question),
        text={"format": {"type": "json_object"}},
    )
    return parse_plan(response.output_text)


def main() -> None:
    parser = argparse.ArgumentParser(description="AI research-planning agent")
    parser.add_argument("question", help="Question to turn into a research plan")
    args = parser.parse_args()
    print(json.dumps(asdict(plan(args.question)), indent=2))


if __name__ == "__main__":
    main()
