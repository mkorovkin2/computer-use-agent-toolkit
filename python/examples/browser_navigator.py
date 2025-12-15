"""
Example: Navigate a browser and extract information.
"""

from computer_use_agent import ComputerUseAgent
import os

api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    print("Please set ANTHROPIC_API_KEY environment variable")
    exit(1)

# Initialize agent with custom system prompt
agent = ComputerUseAgent(
    api_key=api_key,
    model="claude-sonnet-4-20250514",
)

# Navigate and extract information
result = agent.run(
    goal=(
        "1. Open a web browser\n"
        "2. Navigate to github.com\n"
        "3. Search for 'computer use agent'\n"
        "4. Click on the first result\n"
        "5. Read the repository description"
    ),
    max_iterations=20,
    system_prompt=(
        "You are a web navigation assistant. Navigate websites carefully, "
        "read the content, and complete the requested tasks. Take your time "
        "to ensure each step is completed before moving to the next."
    ),
)

print(f"\n{'='*60}")
print(f"Navigation completed in {result['iterations']} iterations")
print(f"Success: {result['success']}")
print(f"{'='*60}")

