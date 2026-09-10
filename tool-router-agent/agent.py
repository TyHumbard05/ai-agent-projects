import argparse
import ast
import json
import operator
import os
import re
from dataclasses import dataclass, asdict

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

TOOLS = {"calculator", "text_stats", "todo_parser", "none"}


@dataclass
class ToolDecision:
    tool: str
    argument: str
    reason: str


_ALLOWED_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_ALLOWED_UNARY = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def safe_calculate(expression: str) -> float:
    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_BINOPS:
            return _ALLOWED_BINOPS[type(node.op)](evaluate(node.left), evaluate(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_UNARY:
            return _ALLOWED_UNARY[type(node.op)](evaluate(node.operand))
        raise ValueError("Unsupported expression")

    tree = ast.parse(expression, mode="eval")
    return float(evaluate(tree))


def text_stats(text: str) -> dict[str, int]:
    words = re.findall(r"\b\w+\b", text)
    return {"characters": len(text), "words": len(words), "lines": len(text.splitlines()) or 1}


def todo_parser(text: str) -> list[str]:
    chunks = re.split(r"[\n;]+", text)
    return [re.sub(r"^[-*\d.\s]+", "", item).strip() for item in chunks if item.strip()]


def build_prompt(task: str) -> str:
    return f"""Choose exactly one local tool for the task. Return JSON only with keys tool, argument, reason.
Allowed tools:
- calculator: arithmetic expressions only
- text_stats: count characters, words, and lines
- todo_parser: split a rough to-do list into clean items
- none: when none of the tools safely fit

Never invent another tool. Keep argument to only what the selected tool needs.

Task:
{task.strip()}
"""


def parse_decision(raw: str) -> ToolDecision:
    data = json.loads(raw)
    tool = str(data.get("tool", "none")).lower()
    if tool not in TOOLS:
        tool = "none"
    return ToolDecision(
        tool=tool,
        argument=str(data.get("argument", "")),
        reason=str(data.get("reason", "")).strip(),
    )


def choose_tool(task: str, client: OpenAI | None = None, model: str | None = None) -> ToolDecision:
    api = client or OpenAI()
    response = api.responses.create(
        model=model or os.getenv("OPENAI_MODEL", "gpt-5.5"),
        input=build_prompt(task),
        text={"format": {"type": "json_object"}},
    )
    return parse_decision(response.output_text)


def execute(decision: ToolDecision):
    if decision.tool == "calculator":
        return safe_calculate(decision.argument)
    if decision.tool == "text_stats":
        return text_stats(decision.argument)
    if decision.tool == "todo_parser":
        return todo_parser(decision.argument)
    return {"message": "No safe matching tool selected."}


def main() -> None:
    parser = argparse.ArgumentParser(description="AI router with a small allowlisted local toolset")
    parser.add_argument("task", help="Task for the agent")
    args = parser.parse_args()
    decision = choose_tool(args.task)
    print(json.dumps({"decision": asdict(decision), "result": execute(decision)}, indent=2))


if __name__ == "__main__":
    main()
