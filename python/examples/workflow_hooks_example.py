"""
Example: Using workflow hooks for logging and conditional logic.
"""

from computer_use_agent import ComputerUseAgent
import os
import time

api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    print("Please set ANTHROPIC_API_KEY environment variable")
    exit(1)

# Initialize agent
agent = ComputerUseAgent(
    api_key=api_key,
    model="claude-sonnet-4-20250514",
)

# Track metrics
metrics = {
    "screenshots_taken": 0,
    "clicks": 0,
    "keystrokes": 0,
    "start_time": time.time(),
}

# Hook: Log every screenshot
@agent.on_before_screenshot
def log_screenshot(context):
    metrics["screenshots_taken"] += 1
    print(f"📸 Taking screenshot #{metrics['screenshots_taken']}")

# Hook: Log every action before execution
@agent.on_before_action
def log_action(context, action):
    action_type = action.get("text", action.get("key", f"action at ({action.get('x', '?')}, {action.get('y', '?')})"))
    print(f"⚡ About to execute action: {action_type}")

# Hook: Track action statistics
@agent.on_after_action
def track_stats(context, action, result):
    if "x" in action and "y" in action:
        metrics["clicks"] += 1
    if "text" in action:
        metrics["keystrokes"] += len(action["text"])
    
    if not result.success:
        print(f"❌ Action failed: {result.error}")

# Hook: Safety check for clicks in top-left corner
@agent.on_tool_call("click")
def safety_check(context, args):
    if args["x"] < 50 and args["y"] < 50:
        print(f"⚠️  WARNING: Clicking near top-left corner at ({args['x']}, {args['y']})")
        # Could add confirmation here
    return args

# Hook: Conditional logic - if clicking on right side, log it
@agent.when("click", lambda ctx, action: action["x"] > 1000)
def on_right_click(context, action):
    print(f"→ Detected click on right side of screen at x={action['x']}")
    context.state["right_clicks"] = context.state.get("right_clicks", 0) + 1

# Hook: Start of each iteration
@agent.on_iteration_start
def iteration_start(context, iteration):
    print(f"\n{'='*60}")
    print(f"Starting iteration {iteration}")
    print(f"{'='*60}")

# Hook: End of each iteration
@agent.on_iteration_end
def iteration_end(context, iteration):
    elapsed = time.time() - metrics["start_time"]
    print(f"Completed iteration {iteration} (total elapsed: {elapsed:.1f}s)")

# Run agent
result = agent.run(
    goal="Click on the Safari icon to open the browser",
    max_iterations=5,
)

# Print final metrics
print(f"\n{'='*60}")
print("FINAL METRICS")
print(f"{'='*60}")
print(f"Total iterations: {result['iterations']}")
print(f"Screenshots taken: {metrics['screenshots_taken']}")
print(f"Total clicks: {metrics['clicks']}")
print(f"Total keystrokes: {metrics['keystrokes']}")
print(f"Right-side clicks: {agent.state.get('right_clicks', 0)}")
print(f"Total time: {time.time() - metrics['start_time']:.1f}s")
print(f"Success: {result['success']}")
print(f"{'='*60}")

