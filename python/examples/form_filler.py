"""
Example: Fill out a web form.
"""

from computer_use_agent import ComputerUseAgent
import os

api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    print("Please set ANTHROPIC_API_KEY environment variable")
    exit(1)

# Initialize agent
agent = ComputerUseAgent(
    api_key=api_key,
    model="claude-sonnet-4-20250514",
)

# Step-by-step form filling with feedback
for step in agent.run_iter(
    goal=(
        "Fill out the contact form on the webpage with the following information:\n"
        "Name: John Doe\n"
        "Email: john@example.com\n"
        "Message: Hello, I would like more information about your services.\n"
        "Then click the Submit button."
    ),
    max_iterations=15,
):
    print(f"\n--- Iteration {step.iteration} ---")
    if step.reasoning:
        print(f"Reasoning: {step.reasoning}")
    if step.action:
        print(f"Action: {step.action}")
    if step.result:
        print(f"Result: Success={step.result.success}")
        if step.result.error:
            print(f"Error: {step.result.error}")

print("\n✓ Form filling complete!")

