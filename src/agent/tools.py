from __future__ import annotations
import re
from typing import Dict


KB: Dict[str, str] = {
    "capital of france": "Paris",
    "capital of canada": "Ottawa",
    "potpie": "Potpie.ai builds enterprise-grade agent workflows and tooling for reliable agents.",
}

def search_kb(query: str) -> str:
    q = query.strip().lower()
    # normalize common phrasing
    q = q.replace("what is the ", "").replace("what's the ", "").replace("?", "").strip()
    return KB.get(q, "NOT_FOUND")


def calculator(expression: str) -> str:
    """
    Very restricted calculator:
    - digits, spaces, + - * / ( )
    - rejects anything else
    """
    expr = expression.strip()
    if not re.fullmatch(r"[0-9\.\s\+\-\*\/\(\)]+", expr):
        return "ERROR: unsupported characters"
    try:
        result = eval(expr, {"__builtins__": {}})
        return str(result)
    except Exception as e:
        return f"ERROR: {e}"

def echo(text: str) -> str:
    return text
