#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from startup_validate.crew import StartupValidate


warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'startup_idea': 'AI interviewer that evaluates job candidates via simulated work scenarios and outputs ranked shortlists'
    }
    
    try:
        res = StartupValidate().crew().kickoff(inputs=inputs)
        with open("res.md", "w") as f:
            f.write(res.raw)
        print(f"Result saved to res.md")
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "startup_idea": "AI LLMs"
    }
    try:
        StartupValidate().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        StartupValidate().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "startup_idea": "AI LLMs"
    }
    
    try:
        StartupValidate().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
