"""
Example 10: Error Recovery and Resilience

This example demonstrates building robust agents with:
- Automatic retry logic
- Error detection and recovery
- Fallback strategies
- Graceful degradation

Use case: Production agents, unreliable environments, long-running workflows
"""

from computer_use_agent import ComputerUseAgent
import os
import time
from datetime import datetime

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("❌ Please set ANTHROPIC_API_KEY environment variable")
    exit(1)

print("🤖 Computer Use Agent - Error Recovery Example")
print("=" * 60)

# Initialize agent
agent = ComputerUseAgent(
    api_key=api_key,
    model="claude-sonnet-4-20250514",
    safety_delay=0.2,  # Longer delay for stability
)

# Error tracking
error_log = []
recovery_attempts = []
successful_recoveries = []


# Hook: Detect and retry failed actions
@agent.on_after_action
def auto_retry_on_failure(context, action, result):
    """Automatically retry failed actions with exponential backoff."""
    
    if not result.success:
        error_entry = {
            "iteration": context.iteration,
            "action": action,
            "error": result.error,
            "timestamp": datetime.now().isoformat(),
        }
        error_log.append(error_entry)
        
        print(f"\n❌ Action failed: {result.error}")
        print(f"   Action: {action}")
        
        # Check if we should retry
        max_retries = 3
        retry_count = context.state.get(f"retry_{context.iteration}", 0)
        
        if retry_count < max_retries:
            print(f"\n🔄 Attempting retry {retry_count + 1}/{max_retries}...")
            
            # Wait with exponential backoff
            wait_time = 2 ** retry_count
            print(f"   Waiting {wait_time}s before retry...")
            time.sleep(wait_time)
            
            # Track retry attempt
            retry_attempt = {
                "iteration": context.iteration,
                "attempt": retry_count + 1,
                "action": action,
            }
            recovery_attempts.append(retry_attempt)
            
            # Update retry count
            context.state[f"retry_{context.iteration}"] = retry_count + 1
            
            # Note: In a real implementation, you'd re-execute the action here
            # For this example, we're just logging the retry attempt
            
        else:
            print(f"\n⚠️  Max retries ({max_retries}) exceeded for this action")
            print(f"   Moving to fallback strategy...")
            
            # Trigger fallback
            context.state["fallback_mode"] = True


# Hook: Detect patterns of failure
@agent.on_iteration_end
def detect_failure_patterns(context, iteration):
    """Detect if agent is stuck in a failure pattern."""
    
    # Check last N actions
    recent_actions = context.action_history[-5:] if len(context.action_history) >= 5 else context.action_history
    failure_rate = sum(1 for a in recent_actions if not a.success) / len(recent_actions) if recent_actions else 0
    
    if failure_rate > 0.6:  # More than 60% failures
        print(f"\n⚠️  HIGH FAILURE RATE DETECTED: {failure_rate:.0%}")
        print(f"   Last {len(recent_actions)} actions had {int(failure_rate * len(recent_actions))} failures")
        print(f"   Consider alternative approach or human intervention")
        
        context.state["high_failure_rate"] = True


# Custom tool: Health check
@agent.tool(name="health_check", description="Check if system is responding correctly")
def health_check(component: str = "system") -> dict:
    """Perform a health check on a component."""
    
    print(f"\n🏥 Health check: {component}")
    
    # Simulate health check
    is_healthy = True  # In real implementation, actually check the component
    
    if is_healthy:
        print(f"   ✓ {component} is healthy")
    else:
        print(f"   ✗ {component} is unhealthy")
    
    return {
        "component": component,
        "healthy": is_healthy,
        "checked_at": datetime.now().isoformat(),
    }


# Custom tool: Reset state
@agent.tool(name="reset_workflow_state", description="Reset workflow to known good state")
def reset_workflow_state() -> dict:
    """Reset the workflow to a known good state."""
    
    print(f"\n🔄 Resetting workflow state...")
    
    # In a real implementation, this would:
    # - Close problematic windows
    # - Clear temporary data
    # - Return to starting point
    
    print(f"   ✓ Workflow state reset complete")
    
    return {
        "reset": True,
        "timestamp": datetime.now().isoformat(),
    }


# Custom tool: Fallback action
@agent.tool(name="execute_fallback", description="Execute fallback strategy")
def execute_fallback(reason: str) -> dict:
    """Execute a fallback strategy when primary approach fails."""
    
    print(f"\n🛟 Executing fallback strategy")
    print(f"   Reason: {reason}")
    
    # Fallback logic
    fallback_strategies = [
        "Use keyboard shortcuts instead of clicking",
        "Try alternative UI element",
        "Restart the application",
        "Request human intervention",
    ]
    
    strategy = fallback_strategies[len(recovery_attempts) % len(fallback_strategies)]
    print(f"   Strategy: {strategy}")
    
    successful_recoveries.append({
        "reason": reason,
        "strategy": strategy,
        "timestamp": datetime.now().isoformat(),
    })
    
    return {
        "fallback_executed": True,
        "strategy": strategy,
    }


# Workflow with error handling
goal = """
You are performing a task that may encounter errors. Here's what to do:

1. Try to click on a specific UI element (this might fail)
2. If actions start failing repeatedly:
   - Use health_check to diagnose the issue
   - Use execute_fallback to try alternative approaches
   - Use reset_workflow_state if needed to recover

3. Continue until the task is complete or fallback strategies are exhausted

For this demo, simulate a scenario where the first few actions might fail,
requiring the agent to adapt and use fallback strategies.

The goal: Open Calculator app and perform a calculation.
"""

print(f"\n🎯 Goal: Open Calculator with error recovery")
print(f"\n🛡️  Error handling features:")
print(f"   - Automatic retry with exponential backoff")
print(f"   - Failure pattern detection")
print(f"   - Multiple fallback strategies")
print(f"   - Health checks")

print(f"\n⏳ Running resilient workflow...\n")

# Run agent
try:
    result = agent.run(goal=goal, max_iterations=25)
    
    success = result['success']
except Exception as e:
    print(f"\n❌ Workflow exception: {e}")
    success = False
    result = {"iterations": 0, "success": False}

# Print comprehensive results
print("\n" + "=" * 60)
print("📊 ERROR RECOVERY REPORT")
print("=" * 60)
print(f"✓ Workflow completed: {success}")
print(f"✓ Iterations: {result.get('iterations', 0)}")

print(f"\n❌ Errors Encountered: {len(error_log)}")
for i, error in enumerate(error_log[:5], 1):  # Show first 5
    print(f"   {i}. Iteration {error['iteration']}: {error['error'][:60]}...")

print(f"\n🔄 Recovery Attempts: {len(recovery_attempts)}")
for i, attempt in enumerate(recovery_attempts[:5], 1):
    print(f"   {i}. Iteration {attempt['iteration']}, Attempt {attempt['attempt']}")

print(f"\n✓ Successful Recoveries: {len(successful_recoveries)}")
for i, recovery in enumerate(successful_recoveries, 1):
    print(f"   {i}. Strategy: {recovery['strategy']}")
    print(f"      Reason: {recovery['reason'][:60]}...")

print(f"\n📊 Error Statistics:")
total_actions = len(agent.context.action_history) if hasattr(agent, 'context') else 0
if total_actions > 0:
    success_rate = sum(1 for a in agent.context.action_history if a.success) / total_actions
    print(f"   Total actions: {total_actions}")
    print(f"   Success rate: {success_rate:.1%}")
    print(f"   Failure rate: {1 - success_rate:.1%}")

print("\n💡 Key Concepts:")
print("   - Automatic retry with exponential backoff")
print("   - Failure pattern detection alerts you to systematic issues")
print("   - Multiple fallback strategies for resilience")
print("   - Health checks help diagnose problems")
print("   - Essential for production agents and long-running workflows")

print("\n🎓 Best Practices:")
print("   1. Always implement retry logic for network/UI actions")
print("   2. Monitor failure rates to detect systematic issues")
print("   3. Have multiple fallback strategies")
print("   4. Log errors comprehensively for debugging")
print("   5. Set maximum retry limits to prevent infinite loops")

