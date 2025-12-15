"""
Example 07: Human-in-the-Loop

This example demonstrates adding human oversight and approval gates:
- Approval required for sensitive actions
- Checkpoint system for long workflows
- Audit trail creation
- Interactive decision points

Use case: Production systems, compliance, high-risk operations
"""

from computer_use_agent import ComputerUseAgent
import os
from datetime import datetime

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("❌ Please set ANTHROPIC_API_KEY environment variable")
    exit(1)

print("🤖 Computer Use Agent - Human-in-the-Loop Example")
print("=" * 60)

# Initialize agent
agent = ComputerUseAgent(
    api_key=api_key,
    model="claude-sonnet-4-20250514",
)

# Tracking
sensitive_actions = []
audit_trail = []
checkpoints = []


def is_sensitive_action(action):
    """Determine if an action is sensitive and requires approval."""
    
    # Define sensitive keywords
    sensitive_keywords = [
        "delete", "remove", "trash", "quit", "close",
        "shutdown", "restart", "uninstall", "format"
    ]
    
    # Check text being typed
    if "text" in action:
        text_lower = action["text"].lower()
        if any(keyword in text_lower for keyword in sensitive_keywords):
            return True, f"Typing sensitive text: '{action['text']}'"
    
    # Check coordinates (e.g., top menu bar where dangerous actions live)
    if "x" in action and "y" in action:
        x, y = action["x"], action["y"]
        
        # Top menu bar (File > Quit, etc.)
        if y < 100:
            return True, f"Clicking in menu bar area ({x}, {y})"
        
        # System controls (close buttons, etc.)
        if x < 50 or x > 1800:
            return True, f"Clicking near window controls ({x}, {y})"
    
    return False, None


# Hook: Require approval for sensitive actions
@agent.on_before_action
def require_approval(context, action):
    """Ask for human approval before sensitive actions."""
    
    is_sensitive, reason = is_sensitive_action(action)
    
    if is_sensitive:
        print(f"\n{'⚠️ ' * 20}")
        print(f"SENSITIVE ACTION DETECTED")
        print(f"{'⚠️ ' * 20}")
        print(f"\nReason: {reason}")
        print(f"Action details: {action}")
        print(f"Current iteration: {context.iteration}")
        
        # Ask for approval
        while True:
            response = input("\n👤 Approve this action? (yes/no/inspect): ").strip().lower()
            
            if response == "yes":
                print("✅ Action APPROVED by user")
                sensitive_actions.append({
                    "action": action,
                    "reason": reason,
                    "approved": True,
                    "timestamp": datetime.now().isoformat(),
                })
                break
            elif response == "no":
                print("❌ Action DENIED by user - stopping agent")
                sensitive_actions.append({
                    "action": action,
                    "reason": reason,
                    "approved": False,
                    "timestamp": datetime.now().isoformat(),
                })
                raise Exception("Action denied by user")
            elif response == "inspect":
                print("\n📊 Current Context:")
                print(f"   Iteration: {context.iteration}")
                print(f"   Actions so far: {len(context.action_history)}")
                print(f"   State: {context.state}")
                continue
            else:
                print("Please answer 'yes', 'no', or 'inspect'")
                continue
    
    return action


# Hook: Create audit trail for ALL actions
@agent.on_after_action
def create_audit_trail(context, action, result):
    """Maintain detailed audit trail."""
    
    audit_entry = {
        "timestamp": datetime.now().isoformat(),
        "iteration": context.iteration,
        "action": action,
        "success": result.success,
        "error": result.error if not result.success else None,
        "sensitive": is_sensitive_action(action)[0],
    }
    audit_trail.append(audit_entry)


# Hook: Checkpoint system - pause for review periodically
@agent.on_iteration_end
def checkpoint_review(context, iteration):
    """Provide checkpoints for human review."""
    
    # Checkpoint every 3 iterations
    if iteration > 0 and (iteration + 1) % 3 == 0:
        print(f"\n{'🔵 ' * 20}")
        print(f"CHECKPOINT - Iteration {iteration + 1}")
        print(f"{'🔵 ' * 20}")
        print(f"\n📊 Progress Summary:")
        print(f"   Actions taken: {len(context.action_history)}")
        print(f"   Successes: {sum(1 for a in context.action_history if a.success)}")
        print(f"   Failures: {sum(1 for a in context.action_history if not a.success)}")
        print(f"   Current state: {context.state}")
        
        checkpoint_entry = {
            "iteration": iteration + 1,
            "actions_count": len(context.action_history),
            "timestamp": datetime.now().isoformat(),
        }
        checkpoints.append(checkpoint_entry)
        
        response = input("\n👤 Continue workflow? (yes/no): ").strip().lower()
        if response != "yes":
            print("🛑 Workflow stopped by user at checkpoint")
            raise Exception("Workflow stopped by user at checkpoint")
        
        print("▶️  Continuing...\n")


# Hook: Log iteration starts
@agent.on_iteration_start
def log_iteration_start(context, iteration):
    """Log start of each iteration."""
    print(f"\n{'─' * 60}")
    print(f"▶️  Iteration {iteration + 1} starting")
    print(f"{'─' * 60}")


# Run agent with human oversight
goal = """
Open TextEdit and create a new document.
Type: "This is a test document created by an AI agent."
Save the document to the Desktop as "agent_test.txt"

Note: This workflow includes actions that may require approval.
"""

print(f"\n🎯 Goal: {goal}")
print(f"\n⚠️  Human-in-the-loop mode ACTIVE")
print(f"   - Sensitive actions will require approval")
print(f"   - Checkpoints every 3 iterations")
print(f"   - Full audit trail maintained")

print(f"\n⏳ Running agent with human oversight...\n")

try:
    result = agent.run(goal=goal, max_iterations=15)
    
    # Success - print results
    print("\n" + "=" * 60)
    print("📊 FINAL RESULTS")
    print("=" * 60)
    print(f"✓ Workflow completed successfully")
    print(f"✓ Iterations: {result['iterations']}")

except Exception as e:
    # Workflow was interrupted
    print("\n" + "=" * 60)
    print("⚠️  WORKFLOW INTERRUPTED")
    print("=" * 60)
    print(f"Reason: {e}")

# Print oversight summary
print(f"\n📋 Oversight Summary:")
print(f"   Sensitive actions detected: {len(sensitive_actions)}")
for i, sa in enumerate(sensitive_actions, 1):
    status = "✅ APPROVED" if sa["approved"] else "❌ DENIED"
    print(f"   {i}. {status} - {sa['reason']}")

print(f"\n🔍 Checkpoints: {len(checkpoints)}")
for i, cp in enumerate(checkpoints, 1):
    print(f"   {i}. Iteration {cp['iteration']} - {cp['actions_count']} actions")

print(f"\n📝 Audit Trail: {len(audit_trail)} entries")
print(f"   (Full audit trail available for compliance review)")

print("\n💡 Key Concepts:")
print("   - Human approval gates for sensitive operations")
print("   - Checkpoint system for review and control")
print("   - Complete audit trail for compliance")
print("   - Interactive decision points in workflows")
print("   - Essential for production and high-risk scenarios")

