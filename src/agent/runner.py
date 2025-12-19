from dotenv import load_dotenv
load_dotenv()

from .tracer import AgentTracer
from .agent import run_agent
from .config import load_settings

def run_observable_agent(user_input: str):
    settings = load_settings()
    tracer = AgentTracer()
    return run_agent(user_input, tracer, settings)
