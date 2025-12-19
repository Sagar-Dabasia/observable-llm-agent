import json
from pathlib import Path
from datetime import datetime
from typing import Optional

from .schemas import AgentRunTrace, ReasoningStep, ToolCall


class AgentTracer:
    def __init__(self, run_dir: str = "runs"):
        self.run_dir = Path(run_dir)
        self.run_dir.mkdir(exist_ok=True)

    def start_run(self, user_input: str) -> AgentRunTrace:
        return AgentRunTrace.new(user_input)

    def log_step(
        self,
        trace: AgentRunTrace,
        thought: str,
        tool_name: Optional[str] = None,
        tool_args: Optional[dict] = None,
        tool_output: Optional[object] = None,
    ):
        step = ReasoningStep(
            step_id=len(trace.steps) + 1,
            thought=thought,
            tool_call=ToolCall(
                tool_name=tool_name,
                arguments=tool_args or {},
                output=tool_output,
            )
            if tool_name
            else None,
            timestamp=datetime.utcnow(),
        )
        trace.steps.append(step)

    def finish_run(
        self,
        trace: AgentRunTrace,
        final_answer: Optional[str] = None,
        failure_type: Optional[str] = None,
    ):
        trace.final_answer = final_answer
        trace.failure_type = failure_type
        trace.finished_at = datetime.utcnow()
        self._persist(trace)

    def _persist(self, trace: AgentRunTrace):
        out = self.run_dir / f"{trace.run_id}.json"
        out.write_text(trace.model_dump_json(indent=2), encoding="utf-8")



