# Observable LLM Agent Debugging System

An observable, tool-using LLM agent designed to expose internal decision-making,
tool usage, and failure modes through structured execution traces.

This project focuses on **agent observability and debugging**, not agent intelligence.

---

## What this project demonstrates

- LLM-driven tool routing using **strict JSON tool calls**
- Step-by-step tracing of agent decisions
- Full visibility into:
  - router prompts and raw LLM output
  - tool calls (arguments + outputs)
  - final answer generation
- Automatic detection of common agent failure modes

---

## Failure modes detected

The system explicitly detects and logs:

- `tool_json_invalid`  
  When the LLM router returns malformed or non-parseable JSON.

- `context_overflow`  
  When user input exceeds a configurable context-length threshold.

- `hallucination`  
  Heuristic detection when a tool returns `NOT_FOUND` but the LLM still produces a confident answer.

Each failure is stored directly in the run trace.

---

## Architecture overview

User Input

↓

LLM Router (JSON tool selection)

↓

Tool Execution

↓

LLM Final Answer

↓

Structured Trace (JSON)

Every step is logged for replay and debugging.

---

## Requirements

- Python 3.10+
- Ollama installed and running locally

---

## Setup

pip install -e .

## Install Ollama from:
https://ollama.com

## Pull a model:
ollama pull llama3.1:8b

## Run the agent
python scripts/run_agent.py

## Each run produces a trace file in:
runs/<run_id>.json

---

## Trace contents

Each run trace includes:
  - Router prompt and raw router output
  - Selected tool name and arguments
  - Tool execution output
  - Final answer prompt and raw output
  - Failure type (if detected)
  - Step-by-step timestamps
  - This makes it easy to understand why an agent failed, not just that it failed.

---

## Design notes

  - Local LLM inference is used for reproducibility and cost control
  - No external frameworks are required
  - The system is intentionally minimal and extensible

---

## Goal

This repository demonstrates an engineering approach to LLM agent observability and
debugging — the core challenges involved in deploying reliable agentic systems.
