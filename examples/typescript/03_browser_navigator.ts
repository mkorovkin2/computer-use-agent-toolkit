/**
 * Example 03: Browser Navigator
 *
 * This example demonstrates web navigation and information extraction:
 * - Opening a browser
 * - Navigating to websites
 * - Using search functionality
 * - Reading and extracting content
 *
 * Use case: Web research, data gathering, automated browsing
 */

import { ComputerUseAgent } from "../../typescript/src";

const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) {
  console.error("❌ Please set ANTHROPIC_API_KEY environment variable");
  process.exit(1);
}

console.log("🤖 Computer Use Agent - Browser Navigator Example");
console.log("=".repeat(60));

async function main() {
  // Initialize agent
  const agent = new ComputerUseAgent({
    apiKey,
    model: "claude-sonnet-4-20250514",
  });

  // Navigation task
  const website = "github.com";
  const searchTerm = "computer use agent";

  const goal = `
1. Open a web browser (Safari, Chrome, or Firefox)
2. Navigate to ${website}
3. Use the search bar to search for '${searchTerm}'
4. Click on the first relevant result
5. Read the repository description and README

Take your time with each step and ensure the page loads before proceeding.
`;

  console.log(`\n🎯 Goal: Navigate to ${website} and search for '${searchTerm}'`);
  console.log(`\n⏳ Running agent (max 25 iterations)...\n`);

  // Run with custom system prompt
  const result = await agent.run(
    goal,
    25,
    "You are a web navigation assistant. You excel at browsing websites, " +
      "finding information, and interacting with web interfaces. " +
      "Always wait for pages to load completely before taking the next action. " +
      "Read URLs and page titles to confirm you're on the right page."
  );

  // Results
  console.log("\n" + "=".repeat(60));
  console.log("📊 RESULTS");
  console.log("=".repeat(60));
  console.log(`✓ Success: ${result.success}`);
  console.log(`✓ Iterations: ${result.iterations}`);
  console.log(`✓ Actions taken: ${result.actionHistory?.length || 0}`);

  if (result.state && Object.keys(result.state).length > 0) {
    console.log(`\n📝 Agent State:`);
    Object.entries(result.state).forEach(([key, value]) => {
      console.log(`   ${key}: ${value}`);
    });
  }

  console.log("\n💡 Tips:");
  console.log("   - The agent can handle different browsers automatically");
  console.log("   - It waits for page loads and handles navigation delays");
  console.log("   - Use a higher max_iterations for complex web workflows");
  console.log("   - Custom system prompts help guide agent behavior");
}

main().catch(console.error);

