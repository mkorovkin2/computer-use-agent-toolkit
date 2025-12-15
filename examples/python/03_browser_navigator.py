"""
Example 03: Browser Navigator

This example demonstrates web navigation and information extraction:
- Opening a browser
- Navigating to websites
- Using search functionality
- Reading and extracting content

Use case: Web research, data gathering, automated browsing
"""

from computer_use_agent import ComputerUseAgent
import os

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("❌ Please set ANTHROPIC_API_KEY environment variable")
    exit(1)

print("🤖 Computer Use Agent - Browser Navigator Example")
print("=" * 60)

# Initialize agent with custom system prompt for web navigation
agent = ComputerUseAgent(
    api_key=api_key,
    model="claude-sonnet-4-20250514",
)

# Navigation task
website = "github.com"
search_term = "computer use agent"

goal = f"""
1. Open a web browser (Safari, Chrome, or Firefox)
2. Navigate to {website}
3. Use the search bar to search for '{search_term}'
4. Click on the first relevant result
5. Read the repository description and README

Take your time with each step and ensure the page loads before proceeding.
"""

print(f"\n🎯 Goal: Navigate to {website} and search for '{search_term}'")
print(f"\n⏳ Running agent (max 25 iterations)...\n")

# Run with a custom system prompt for better web navigation
result = agent.run(
    goal=goal,
    max_iterations=25,
    system_prompt=(
        "You are a web navigation assistant. You excel at browsing websites, "
        "finding information, and interacting with web interfaces. "
        "Always wait for pages to load completely before taking the next action. "
        "Read URLs and page titles to confirm you're on the right page."
    ),
)

# Results
print("\n" + "=" * 60)
print("📊 RESULTS")
print("=" * 60)
print(f"✓ Success: {result['success']}")
print(f"✓ Iterations: {result['iterations']}")
print(f"✓ Actions taken: {len(result.get('action_history', []))}")

if result.get('state'):
    print(f"\n📝 Agent State:")
    for key, value in result['state'].items():
        print(f"   {key}: {value}")

print("\n💡 Tips:")
print("   - The agent can handle different browsers automatically")
print("   - It waits for page loads and handles navigation delays")
print("   - Use a higher max_iterations for complex web workflows")
print("   - Custom system prompts help guide agent behavior")

