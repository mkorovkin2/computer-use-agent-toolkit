/**
 * Example 01: Simple Click
 *
 * This example demonstrates the most basic usage of the Computer Use Agent:
 * - Initialize the agent
 * - Give it a simple goal
 * - Let it analyze the screen and click on an element
 *
 * Use case: Opening an application or clicking a button
 */

import { ComputerUseAgent } from "../../typescript/src";

const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) {
  console.error("❌ Please set ANTHROPIC_API_KEY environment variable");
  console.error("   export ANTHROPIC_API_KEY='your-key-here'");
  process.exit(1);
}

console.log("🤖 Computer Use Agent - Simple Click Example");
console.log("=".repeat(60));

async function main() {
  // Initialize the agent
  const agent = new ComputerUseAgent({
    apiKey,
    model: "claude-sonnet-4-20250514",
  });

  // Give the agent a simple goal
  const goal = "Find and click on the Chrome browser icon to open it";

  console.log(`\n🎯 Goal: ${goal}`);
  console.log(`\n⏳ Running agent (max 5 iterations)...\n`);

  // Run the agent
  const result = await agent.run(goal, 5);

  // Print results
  console.log("\n" + "=".repeat(60));
  console.log("📊 RESULTS");
  console.log("=".repeat(60));
  console.log(`✓ Success: ${result.success}`);
  console.log(`✓ Iterations used: ${result.iterations}`);
  console.log(`✓ Actions taken: ${result.actionHistory?.length || 0}`);

  if (!result.success) {
    console.log(`❌ Error: ${result.error}`);
  }

  console.log("\n💡 Tip: Try changing the goal to click on different elements!");
}

main().catch(console.error);

