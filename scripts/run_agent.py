from agent.runner import run_observable_agent

if __name__ == "__main__":
    examples = [
        "What is the capital of France?",
        "12 + 30 / 2",
        "hello there"
        "X" * 7000

    ]

    for q in examples:
        trace = run_observable_agent(q)
        print(f"Saved run: {trace.run_id} | input_length: {len(q)}")

