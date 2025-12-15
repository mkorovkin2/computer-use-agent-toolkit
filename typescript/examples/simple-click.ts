/**
 * Simple example: Click on a button.
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

  const result = await agent.run(
    "Click on the Chrome icon in the dock to open it",
    5
  );

  console.log(`Agent completed in ${result.iterations} iterations`);
  console.log(`Success: ${result.success}`);
  if (!result.success) {
    console.log(`Error: ${result.error}`);
  }
}

main().catch(console.error);

