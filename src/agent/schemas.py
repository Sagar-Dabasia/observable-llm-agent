from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from datetime import datetime
import uuid


class ToolCall(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]
    output: Optional[Any] = None


class ReasoningStep(BaseModel):
    step_id: int
    thought: str
    tool_call: Optional[ToolCall] = None
    timestamp: datetime


class AgentRunTrace(BaseModel):
    run_id: str
    user_input: str
    steps: List[ReasoningStep]
    final_answer: Optional[str] = None
    failure_type: Optional[str] = None
    started_at: datetime
    finished_at: Optional[datetime] = None
    llm_router_prompt: Optional[str] = None
    llm_router_raw: Optional[str] = None
    llm_final_prompt: Optional[str] = None
    llm_final_raw: Optional[str] = None


    @staticmethod
    def new(user_input: str) -> "AgentRunTrace":
        return AgentRunTrace(
            run_id=str(uuid.uuid4()),
            user_input=user_input,
            steps=[],
            started_at=datetime.utcnow(),
        )
