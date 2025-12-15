/**
 * Example: Using workflow hooks for logging and metrics.
 */

import { ComputerUseAgent } from "../src";

const apiKey = process.env.ANTHROPIC_API_KEY;

if (!apiKey) {
  console.error("Please set ANTHROPIC_API_KEY environment variable");
  process.exit(1);
}

async function main() {
  const agent = new ComputerUseAgent({
    apiKey,
    model: "claude-sonnet-4-20250514",
  });

  // Track metrics
  const metrics = {
    screenshotsTaken: 0,
    clicks: 0,
    keystrokes: 0,
    startTime: Date.now(),
  };

  // Hook: Log every screenshot
  agent.onBeforeScreenshot((context) => {
    metrics.screenshotsTaken++;
    console.log(`📸 Taking screenshot #${metrics.screenshotsTaken}`);
  });

  // Hook: Log every action
  agent.onBeforeAction((context, action) => {
    const actionType = action.text || action.key || `action at (${action.x ?? "?"}, ${action.y ?? "?"})`;
    console.log(`⚡ About to execute action: ${actionType}`);
  });

  // Hook: Track statistics
  agent.onAfterAction((context, action, result) => {
    if (action.x !== undefined && action.y !== undefined) {
      metrics.clicks++;
    }
    if (action.text) {
      metrics.keystrokes += action.text.length;
    }

    if (!result.success) {
      console.log(`❌ Action failed: ${result.error}`);
    }
  });

  // Hook: Safety check
  agent.onToolCall("click", (context, args) => {
    if (args.x < 50 && args.y < 50) {
      console.log(`⚠️  WARNING: Clicking near top-left corner at (${args.x}, ${args.y})`);
    }
    return args;
  });

  // Hook: Conditional logic
  agent.when(
    "click",
    (ctx, action) => action.x > 1000,
    (context, action) => {
      console.log(`→ Detected click on right side of screen at x=${action.x}`);
      context.state.rightClicks = (context.state.rightClicks || 0) + 1;
    }
  );

  // Hook: Iteration boundaries
  agent.onIterationStart((context, iteration) => {
    console.log(`\n${"=".repeat(60)}`);
    console.log(`Starting iteration ${iteration}`);
    console.log("=".repeat(60));
  });

  agent.onIterationEnd((context, iteration) => {
    const elapsed = (Date.now() - metrics.startTime) / 1000;
    console.log(`Completed iteration ${iteration} (total elapsed: ${elapsed.toFixed(1)}s)`);
  });

  // Run agent
  const result = await agent.run("Click on the Safari icon to open the browser", 5);

  // Print final metrics
  console.log(`\n${"=".repeat(60)}`);
  console.log("FINAL METRICS");
  console.log("=".repeat(60));
  console.log(`Total iterations: ${result.iterations}`);
  console.log(`Screenshots taken: ${metrics.screenshotsTaken}`);
  console.log(`Total clicks: ${metrics.clicks}`);
  console.log(`Total keystrokes: ${metrics.keystrokes}`);
  console.log(`Right-side clicks: ${agent.state.rightClicks || 0}`);
  console.log(`Total time: ${((Date.now() - metrics.startTime) / 1000).toFixed(1)}s`);
  console.log(`Success: ${result.success}`);
  console.log("=".repeat(60));
}

main().catch(console.error);

