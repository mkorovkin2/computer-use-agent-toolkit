"""
Example 01: Simple Click

This example demonstrates the most basic usage of the Computer Use Agent:
- Initialize the agent
- Give it a simple goal
- Let it analyze the screen and click on an element

Use case: Opening an application or clicking a button
"""

from computer_use_agent import ComputerUseAgent
import os

# Get API key from environment
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("❌ Please set ANTHROPIC_API_KEY environment variable")
    print("   export ANTHROPIC_API_KEY='your-key-here'")
    exit(1)

print("🤖 Computer Use Agent - Simple Click Example")
print("=" * 60)

# Initialize the agent
agent = ComputerUseAgent(
    api_key=api_key,
    model="claude-sonnet-4-20250514",
)

# Give the agent a simple goal
goal = "Find and click on the Chrome browser icon to open it"

print(f"\n🎯 Goal: {goal}")
print(f"\n⏳ Running agent (max 5 iterations)...\n")

# Run the agent
result = agent.run(
    goal=goal,
    max_iterations=5,
)

# Print results
print("\n" + "=" * 60)
print("📊 RESULTS")
print("=" * 60)
print(f"✓ Success: {result['success']}")
print(f"✓ Iterations used: {result['iterations']}")
print(f"✓ Actions taken: {len(result.get('action_history', []))}")

if not result['success']:
    print(f"❌ Error: {result.get('error')}")

print("\n💡 Tip: Try changing the goal to click on different elements!")

