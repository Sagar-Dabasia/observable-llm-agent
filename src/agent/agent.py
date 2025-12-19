from __future__ import annotations
import json
import re
from typing import Any, Dict, Tuple

from .tracer import AgentTracer
from .tools import calculator, search_kb, echo
from .llm import OllamaClient
from .config import Settings


def _extract_json(text: str) -> str:
    # remove common fenced blocks
    text = text.strip()
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, flags=re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1).strip()
    m = re.search(r"(\{.*\})", text, flags=re.DOTALL)
    if m:
        return m.group(1).strip()
    return text


def run_agent(user_input: str, tracer: AgentTracer, settings: Settings):
    trace = tracer.start_run(user_input)

    # crude context overflow check (chars as proxy)
    if len(user_input) > settings.max_context_chars:
        tracer.finish_run(trace, final_answer=None, failure_type="context_overflow")
        return trace

    llm = OllamaClient(
        host=settings.ollama_host,
        model=settings.ollama_model,
        temperature=settings.temperature,
    )

    tool_spec = """
You are a router that must choose exactly ONE tool.

Available tools:
1) search_kb(query: string) -> returns a short string or NOT_FOUND
2) calculator(expression: string) -> returns a number or ERROR
3) echo(text: string) -> returns the text unchanged

Return ONLY valid JSON with keys:
tool_name: one of ["search_kb","calculator","echo"]
arguments: object

No markdown. No extra text.
""".strip()

    router_user = f"User input: {user_input}\nChoose the best tool and arguments."
    trace.llm_router_prompt = router_user

    tracer.log_step(trace, "Asking LLM to choose a tool (router)")

    router_res = llm.chat(router_user, system=tool_spec)
    trace.llm_router_raw = router_res.text

    tracer.log_step(
        trace,
        "Router LLM returned tool selection",
        tool_name="llm_router",
        tool_args={"latency_s": router_res.latency_s},
        tool_output=router_res.text,
    )

    # Parse tool JSON
    try:
        obj = json.loads(_extract_json(router_res.text))
        tool_name = obj["tool_name"]
        args = obj.get("arguments", {}) or {}
    except Exception:
        tracer.finish_run(trace, final_answer=None, failure_type="tool_json_invalid")
        return trace

    # Execute tool
    tracer.log_step(trace, "Executing selected tool", tool_name=tool_name, tool_args=args)

    if tool_name == "search_kb":
        tool_out = search_kb(str(args.get("query", "")).replace("?", "").strip())
    elif tool_name == "calculator":
        tool_out = calculator(str(args.get("expression", "")))
    elif tool_name == "echo":
        tool_out = echo(str(args.get("text", user_input)))
    else:
        tracer.finish_run(trace, final_answer=None, failure_type="tool_name_invalid")
        return trace

    tracer.log_step(trace, "Tool returned output", tool_name=tool_name, tool_args=args, tool_output=tool_out)

    # Final answer prompt
    final_system = "You are a helpful assistant. Use the tool output to answer. If tool output is NOT_FOUND or ERROR, say you cannot complete the request."
    final_user = f"""User input: {user_input}

Tool used: {tool_name}
Tool arguments: {args}
Tool output: {tool_out}

Write the final answer concisely."""
    trace.llm_final_prompt = final_user

    tracer.log_step(trace, "Asking LLM to produce final answer")

    final_res = llm.chat(final_user, system=final_system)
    trace.llm_final_raw = final_res.text

    # hallucination detector: tool says NOT_FOUND but model still answers confidently
    failure = None
    if str(tool_out).strip() == "NOT_FOUND":
        # very simple heuristic
        if len(final_res.text.strip()) > 0 and "cannot" not in final_res.text.lower() and "not found" not in final_res.text.lower():
            failure = "hallucination"

    tracer.finish_run(trace, final_answer=final_res.text, failure_type=failure)
    return trace
