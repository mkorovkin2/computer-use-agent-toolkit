"""
Simple example: Click on a button.
"""

from computer_use_agent import ComputerUseAgent
import os

# Get API key from environment
api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    print("Please set ANTHROPIC_API_KEY environment variable")
    exit(1)

# Initialize agent
agent = ComputerUseAgent(
    api_key=api_key,
    model="claude-sonnet-4-20250514",
)

# Run agent with a simple goal
result = agent.run(
    goal="Click on the Chrome icon in the dock to open it",
    max_iterations=5,
)

print(f"Agent completed in {result['iterations']} iterations")
print(f"Success: {result['success']}")
if not result['success']:
    print(f"Error: {result.get('error')}")

