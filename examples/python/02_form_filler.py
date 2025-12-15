"""
Example 02: Form Filler

This example shows how to fill out multi-field forms with the agent.
It demonstrates:
- Step-by-step execution with run_iter()
- Real-time progress monitoring
- Multiple sequential actions (click, type, tab)

Use case: Automated form submission, data entry
"""

from computer_use_agent import ComputerUseAgent
import os

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("❌ Please set ANTHROPIC_API_KEY environment variable")
    exit(1)

print("🤖 Computer Use Agent - Form Filler Example")
print("=" * 60)

# Initialize agent
agent = ComputerUseAgent(
    api_key=api_key,
    model="claude-sonnet-4-20250514",
    safety_delay=0.2,  # Slightly longer delay for form interactions
)

# Form data to fill
form_data = {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+1-555-0123",
    "message": "Hello! I'm interested in learning more about your services.",
}

goal = f"""
Fill out the contact form with the following information:
- Name: {form_data['name']}
- Email: {form_data['email']}
- Phone: {form_data['phone']}
- Message: {form_data['message']}

Then click the Submit button.
"""

print(f"\n🎯 Goal: Fill out contact form")
print(f"\n📋 Form Data:")
for key, value in form_data.items():
    print(f"   {key.capitalize()}: {value}")

print(f"\n⏳ Running agent with step-by-step monitoring...\n")

# Run with step-by-step control
iteration_count = 0
for step in agent.run_iter(goal=goal, max_iterations=20):
    iteration_count += 1
    
    print(f"\n{'─' * 60}")
    print(f"📍 Iteration {step.iteration + 1}")
    print(f"{'─' * 60}")
    
    if step.reasoning:
        print(f"💭 Reasoning: {step.reasoning[:100]}...")
    
    if step.action:
        print(f"⚡ Action: {step.action.value}")
    
    if step.result:
        status = "✓" if step.result.success else "✗"
        print(f"{status} Result: {'Success' if step.result.success else 'Failed'}")
        if step.result.error:
            print(f"   Error: {step.result.error}")

print("\n" + "=" * 60)
print("📊 FINAL RESULTS")
print("=" * 60)
print(f"✓ Total iterations: {iteration_count}")
print(f"✓ Form filling complete!")

print("\n💡 Tips:")
print("   - The agent analyzes the form layout before filling")
print("   - It uses tab/click to navigate between fields")
print("   - run_iter() gives you real-time control and visibility")

