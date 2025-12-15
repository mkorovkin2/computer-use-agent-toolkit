/**
 * Example 05: Workflow Hooks
 *
 * This example demonstrates the hook system for:
 * - Logging all agent actions
 * - Tracking metrics and performance
 * - Adding safety checks
 * - Implementing conditional logic
 * - Creating audit trails
 *
 * Use case: Production monitoring, debugging, compliance, safety
 */

import { ComputerUseAgent } from "../../typescript/src";

const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) {
  console.error("❌ Please set ANTHROPIC_API_KEY environment variable");
  process.exit(1);
}

console.log("🤖 Computer Use Agent - Workflow Hooks Example");
console.log("=".repeat(60));

// Metrics tracking
const metrics = {
  startTime: Date.now(),
  screenshots: 0,
  clicks: 0,
  keystrokes: 0,
  actionsByType: {} as Record<string, number>,
  errors: [] as any[],
};

// Audit log
const auditLog: any[] = [];

async function main() {
  // Initialize agent
  const agent = new ComputerUseAgent({
    apiKey,
    model: "claude-sonnet-4-20250514",
  });

  // Hook 1: Before screenshot - count screenshots
  agent.onBeforeScreenshot((context) => {
    metrics.screenshots++;
    console.log(`📸 Taking screenshot #${metrics.screenshots}`);
  });

  // Hook 2: Before action - log and validate
  agent.onBeforeAction((context, action) => {
    const actionDesc =
      action.text || action.key || `at (${action.x || "?"}, ${action.y || "?"})`;
    console.log(`⚡ Action: ${actionDesc}`);

    // Safety check: warn about clicks in danger zones
    if (action.x !== undefined && action.y !== undefined) {
      const { x, y } = action;
      // Top-left corner (system menu area)
      if (x < 100 && y < 50) {
        console.log(`   ⚠️  WARNING: Clicking near system menu area!`);
      }
      // Bottom dock area (macOS)
      else if (y > 1000) {
        console.log(`   ⚠️  WARNING: Clicking in dock area!`);
      }
    }

    return action;
  });

  // Hook 3: After action - track statistics and errors
  agent.onAfterAction((context, action, result) => {
    // Count action types
    const actionType = result.actionType.toString();
    metrics.actionsByType[actionType] = (metrics.actionsByType[actionType] || 0) + 1;

    // Count clicks and keystrokes
    if (action.x !== undefined && action.y !== undefined) {
      metrics.clicks++;
    }
    if (action.text) {
      metrics.keystrokes += action.text.length;
    }

    // Log errors
    if (!result.success) {
      const errorEntry = {
        iteration: context.iteration,
        action,
        error: result.error,
      };
      metrics.errors.push(errorEntry);
      console.log(`   ❌ Action failed: ${result.error}`);
    } else {
      console.log(`   ✓ Action succeeded`);
    }

    // Add to audit log
    auditLog.push({
      iteration: context.iteration,
      action,
      success: result.success,
      error: result.success ? null : result.error,
      timestamp: Date.now(),
    });
  });

  // Hook 4: Tool call interception - modify arguments
  agent.onToolCall("click", (context, args) => {
    // Example: Convert all clicks to double-clicks in a specific region
    if ((args as any).x > 1500) {
      console.log(`   🔄 Converting to double-click (x > 1500)`);
      (args as any).clicks = 2;
    }

    return args;
  });

  // Hook 5: Conditional logic - track right-side clicks
  agent.when(
    "click",
    (ctx, action) => (action as any).x > 960,
    (context, action) => {
      context.state.rightSideClicks = (context.state.rightSideClicks || 0) + 1;
      console.log(
        `   → Right-side click detected (total: ${context.state.rightSideClicks})`
      );
    }
  );

  // Hook 6: Iteration boundaries
  agent.onIterationStart((context, iteration) => {
    console.log(`\n${"═".repeat(60)}`);
    console.log(`🔄 ITERATION ${iteration + 1}`);
    console.log("═".repeat(60));
  });

  agent.onIterationEnd((context, iteration) => {
    const elapsed = (Date.now() - metrics.startTime) / 1000;
    console.log(`\n⏱️  Iteration ${iteration + 1} complete (elapsed: ${elapsed.toFixed(1)}s)`);
  });

  // Run agent
  const goal = "Click on the Finder icon in the dock to open a file browser";

  console.log(`\n🎯 Goal: ${goal}`);
  console.log(`\n⏳ Running agent with comprehensive hooks...\n`);

  const result = await agent.run(goal, 5);

  // Print detailed metrics
  console.log("\n" + "=".repeat(60));
  console.log("📊 FINAL METRICS");
  console.log("=".repeat(60));

  console.log(`\n⏱️  Performance:`);
  console.log(`   Total time: ${((Date.now() - metrics.startTime) / 1000).toFixed(2)}s`);
  console.log(`   Iterations: ${result.iterations}`);
  console.log(
    `   Avg time/iteration: ${((Date.now() - metrics.startTime) / 1000 / result.iterations).toFixed(2)}s`
  );

  console.log(`\n📸 Screenshots:`);
  console.log(`   Total: ${metrics.screenshots}`);

  console.log(`\n⚡ Actions:`);
  console.log(`   Total clicks: ${metrics.clicks}`);
  console.log(`   Total keystrokes: ${metrics.keystrokes}`);
  console.log(`   Right-side clicks: ${agent.state.rightSideClicks || 0}`);

  console.log(`\n📋 Actions by type:`);
  Object.entries(metrics.actionsByType)
    .sort()
    .forEach(([type, count]) => {
      console.log(`   ${type}: ${count}`);
    });

  console.log(`\n❌ Errors: ${metrics.errors.length}`);
  metrics.errors.forEach((error) => {
    console.log(`   Iteration ${error.iteration}: ${error.error}`);
  });

  console.log(`\n📝 Audit log entries: ${auditLog.length}`);
  console.log(`   (Full audit log available for compliance/review)`);

  console.log(`\n🎯 Result: ${result.success ? "✓ Success" : "✗ Failed"}`);

  console.log("\n💡 Key Concepts:");
  console.log("   - Hooks provide visibility into every agent action");
  console.log("   - Use for logging, metrics, safety checks, and debugging");
  console.log("   - Conditional logic with agent.when() for 'if X then Y' workflows");
  console.log("   - Hooks can modify actions before execution");
  console.log("   - Build audit trails for compliance and review");
}

main().catch(console.error);

