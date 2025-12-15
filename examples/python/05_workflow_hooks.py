"""
Example 05: Workflow Hooks

This example demonstrates the hook system for:
- Logging all agent actions
- Tracking metrics and performance
- Adding safety checks
- Implementing conditional logic
- Creating audit trails

Use case: Production monitoring, debugging, compliance, safety
"""

from computer_use_agent import ComputerUseAgent
import os
import time
import json

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("❌ Please set ANTHROPIC_API_KEY environment variable")
    exit(1)

print("🤖 Computer Use Agent - Workflow Hooks Example")
print("=" * 60)

# Initialize agent
agent = ComputerUseAgent(
    api_key=api_key,
    model="claude-sonnet-4-20250514",
)

# Metrics tracking
metrics = {
    "start_time": time.time(),
    "screenshots": 0,
    "clicks": 0,
    "keystrokes": 0,
    "actions_by_type": {},
    "errors": [],
}

# Audit log
audit_log = []


# Hook 1: Before screenshot - count screenshots
@agent.on_before_screenshot
def track_screenshots(context):
    metrics["screenshots"] += 1
    print(f"📸 Taking screenshot #{metrics['screenshots']}")


# Hook 2: Before action - log and validate
@agent.on_before_action
def log_and_validate_action(context, action):
    """Log every action before execution and perform safety checks."""
    
    # Log the action
    action_desc = f"Action: {action.get('text', action.get('key', f'at ({action.get('x', '?')}, {action.get('y', '?')})'))}"
    print(f"⚡ {action_desc}")
    
    # Safety check: warn about clicks in danger zones
    if "x" in action and "y" in action:
        x, y = action["x"], action["y"]
        # Top-left corner (system menu area)
        if x < 100 and y < 50:
            print(f"   ⚠️  WARNING: Clicking near system menu area!")
        # Bottom dock area (macOS)
        elif y > 1000:
            print(f"   ⚠️  WARNING: Clicking in dock area!")
    
    return action


# Hook 3: After action - track statistics and errors
@agent.on_after_action
def track_action_stats(context, action, result):
    """Track action statistics and log errors."""
    
    # Count action types
    action_type = str(result.action_type.value if hasattr(result.action_type, 'value') else result.action_type)
    metrics["actions_by_type"][action_type] = metrics["actions_by_type"].get(action_type, 0) + 1
    
    # Count clicks and keystrokes
    if "x" in action and "y" in action:
        metrics["clicks"] += 1
    if "text" in action:
        metrics["keystrokes"] += len(action["text"])
    
    # Log errors
    if not result.success:
        error_entry = {
            "iteration": context.iteration,
            "action": action,
            "error": result.error,
        }
        metrics["errors"].append(error_entry)
        print(f"   ❌ Action failed: {result.error}")
    else:
        print(f"   ✓ Action succeeded")
    
    # Add to audit log
    audit_log.append({
        "iteration": context.iteration,
        "action": action,
        "success": result.success,
        "error": result.error if not result.success else None,
        "timestamp": time.time(),
    })


# Hook 4: Tool call interception - modify arguments
@agent.on_tool_call("click")
def intercept_clicks(context, args):
    """Intercept and potentially modify click actions."""
    
    # Example: Convert all clicks to double-clicks in a specific region
    # (This is just for demonstration - normally you wouldn't do this)
    if args.get("x", 0) > 1500:
        print(f"   🔄 Converting to double-click (x > 1500)")
        args["clicks"] = 2
    
    return args


# Hook 5: Conditional logic - track right-side clicks
@agent.when("click", lambda ctx, action: action.get("x", 0) > 960)
def on_right_side_click(context, action):
    """Triggered when clicking on right side of screen."""
    context.state["right_side_clicks"] = context.state.get("right_side_clicks", 0) + 1
    print(f"   → Right-side click detected (total: {context.state['right_side_clicks']})")


# Hook 6: Iteration boundaries
@agent.on_iteration_start
def iteration_start(context, iteration):
    """Log iteration start."""
    print(f"\n{'═' * 60}")
    print(f"🔄 ITERATION {iteration + 1}")
    print(f"{'═' * 60}")


@agent.on_iteration_end
def iteration_end(context, iteration):
    """Log iteration end with timing."""
    elapsed = time.time() - metrics["start_time"]
    print(f"\n⏱️  Iteration {iteration + 1} complete (elapsed: {elapsed:.1f}s)")


# Run agent
goal = "Click on the Finder icon in the dock to open a file browser"

print(f"\n🎯 Goal: {goal}")
print(f"\n⏳ Running agent with comprehensive hooks...\n")

result = agent.run(goal=goal, max_iterations=5)

# Print detailed metrics
print("\n" + "=" * 60)
print("📊 FINAL METRICS")
print("=" * 60)

print(f"\n⏱️  Performance:")
print(f"   Total time: {time.time() - metrics['start_time']:.2f}s")
print(f"   Iterations: {result['iterations']}")
print(f"   Avg time/iteration: {(time.time() - metrics['start_time']) / result['iterations']:.2f}s")

print(f"\n📸 Screenshots:")
print(f"   Total: {metrics['screenshots']}")

print(f"\n⚡ Actions:")
print(f"   Total clicks: {metrics['clicks']}")
print(f"   Total keystrokes: {metrics['keystrokes']}")
print(f"   Right-side clicks: {agent.state.get('right_side_clicks', 0)}")

print(f"\n📋 Actions by type:")
for action_type, count in sorted(metrics["actions_by_type"].items()):
    print(f"   {action_type}: {count}")

print(f"\n❌ Errors: {len(metrics['errors'])}")
for error in metrics["errors"]:
    print(f"   Iteration {error['iteration']}: {error['error']}")

print(f"\n📝 Audit log entries: {len(audit_log)}")
print(f"   (Full audit log available for compliance/review)")

print(f"\n🎯 Result: {'✓ Success' if result['success'] else '✗ Failed'}")

print("\n💡 Key Concepts:")
print("   - Hooks provide visibility into every agent action")
print("   - Use for logging, metrics, safety checks, and debugging")
print("   - Conditional logic with @agent.when() for 'if X then Y' workflows")
print("   - Hooks can modify actions before execution")
print("   - Build audit trails for compliance and review")

