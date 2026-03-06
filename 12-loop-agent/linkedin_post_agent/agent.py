from google.adk.agents import LoopAgent, SequentialAgent

from .subagents.post_generator import initial_post_generator
from .subagents.post_refiner import post_refiner
from .subagents.post_reviewer import post_reviewer

from dotenv import load_dotenv

load_dotenv()

# Create the Refinement Loop Agent
refinement_loop = LoopAgent(
    name="post_refinement_agent",
    max_iterations=10,
    sub_agents=[
        post_reviewer,
        post_refiner,
    ],
    description="Iteratively reviews and refines a LinkedIn post until quality requirements are met",
)

# Create the Sequential Pipeline
root_agent = SequentialAgent(
    name="linked_in_post_generation_pipeline",
    sub_agents=[
        initial_post_generator,
        refinement_loop,
    ],
    description="Generates and refines a LinkedIn post through an iterative review process",
)
