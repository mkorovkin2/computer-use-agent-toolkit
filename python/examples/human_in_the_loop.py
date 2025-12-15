"""
Example: Human-in-the-loop workflow with approval gates.
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
    confirmation_mode="auto",  # Can be changed to "confirm" for all actions
)

# Track actions that need approval
sensitive_actions = []

# Hook: Require approval for potentially dangerous actions
@agent.on_before_action
def require_approval_for_sensitive_actions(context, action):
    """Ask for human approval before sensitive actions."""
    
    # Check for sensitive keywords in recent context
    sensitive_keywords = ["delete", "remove", "trash", "quit", "close", "shutdown"]
    
    # Check if this is a click action near dangerous UI elements
    is_sensitive = False
    
    if "x" in action and "y" in action:
        # Top menu bar area (could contain File > Quit, etc.)
        if action["y"] < 100:
            is_sensitive = True
    
    # Check for typing sensitive commands
    if "text" in action:
        text_lower = action["text"].lower()
        if any(keyword in text_lower for keyword in sensitive_keywords):
            is_sensitive = True
    
    if is_sensitive:
        print(f"\n⚠️  SENSITIVE ACTION DETECTED ⚠️")
        print(f"Action details: {action}")
        
        # Ask for approval
        response = input("\nDo you want to allow this action? (yes/no): ").strip().lower()
        
        if response != "yes":
            print("❌ Action cancelled by user")
            sensitive_actions.append({"action": action, "approved": False})
            raise Exception("Action cancelled by user")
        else:
            print("✓ Action approved")
            sensitive_actions.append({"action": action, "approved": True})
    
    return action

# Hook: Log all actions for audit trail
audit_log = []

@agent.on_after_action
def audit_trail(context, action, result):
    """Maintain audit trail of all actions."""
    audit_log.append({
        "iteration": context.iteration,
        "action": action,
        "success": result.success,
        "error": result.error,
    })

# Hook: Checkpoint at key moments
@agent.on_iteration_end
def checkpoint(context, iteration):
    """Provide checkpoints for human review."""
    if iteration % 3 == 0 and iteration > 0:
        print(f"\n{'='*60}")
        print(f"CHECKPOINT - Iteration {iteration}")
        print(f"Actions taken so far: {len(context.action_history)}")
        print(f"Current state: {context.state}")
        print(f"{'='*60}")
        
        response = input("\nContinue? (yes/no): ").strip().lower()
        if response != "yes":
            raise Exception("Workflow stopped by user at checkpoint")

# Run agent with human oversight
print("Starting agent with human-in-the-loop controls...")
print("You will be asked to approve sensitive actions.\n")

try:
    result = agent.run(
        goal=(
            "Open a text editor and create a new document with the text:\n"
            "'Hello from the computer use agent!'\n"
            "Then save the document."
        ),
        max_iterations=15,
    )
    
    # Print results
    print(f"\n{'='*60}")
    print("WORKFLOW COMPLETE")
    print(f"{'='*60}")
    print(f"Success: {result['success']}")
    print(f"Iterations: {result['iterations']}")
    print(f"\nSensitive actions detected: {len(sensitive_actions)}")
    for i, action in enumerate(sensitive_actions, 1):
        approved = "✓ APPROVED" if action["approved"] else "❌ DENIED"
        print(f"  {i}. {approved}: {action['action']}")
    print(f"\nAudit log entries: {len(audit_log)}")
    print(f"{'='*60}")

except Exception as e:
    print(f"\n❌ Workflow interrupted: {e}")
    print(f"\nAudit log has {len(audit_log)} entries")

