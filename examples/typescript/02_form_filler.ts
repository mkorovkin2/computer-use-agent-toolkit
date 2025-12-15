/**
 * Example 02: Form Filler
 *
 * This example shows how to fill out multi-field forms with the agent.
 * It demonstrates automated form submission and data entry.
 *
 * Use case: Automated form submission, data entry
 */

import { ComputerUseAgent } from "../../typescript/src";

const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) {
  console.error("❌ Please set ANTHROPIC_API_KEY environment variable");
  process.exit(1);
}

console.log("🤖 Computer Use Agent - Form Filler Example");
console.log("=".repeat(60));

async function main() {
  // Initialize agent
  const agent = new ComputerUseAgent({
    apiKey,
    model: "claude-sonnet-4-20250514",
    safetyDelay: 0.2, // Slightly longer delay for form interactions
  });

  // Form data to fill
  const formData = {
    name: "John Doe",
    email: "john.doe@example.com",
    phone: "+1-555-0123",
    message: "Hello! I'm interested in learning more about your services.",
  };

  const goal = `
Fill out the contact form with the following information:
- Name: ${formData.name}
- Email: ${formData.email}
- Phone: ${formData.phone}
- Message: ${formData.message}

Then click the Submit button.
`;

  console.log(`\n🎯 Goal: Fill out contact form`);
  console.log(`\n📋 Form Data:`);
  Object.entries(formData).forEach(([key, value]) => {
    console.log(`   ${key.charAt(0).toUpperCase() + key.slice(1)}: ${value}`);
  });

  console.log(`\n⏳ Running agent...\n`);

  // Run agent
  const result = await agent.run(goal, 20);

  console.log("\n" + "=".repeat(60));
  console.log("📊 FINAL RESULTS");
  console.log("=".repeat(60));
  console.log(`✓ Total iterations: ${result.iterations}`);
  console.log(`✓ Form filling complete!`);

  console.log("\n💡 Tips:");
  console.log("   - The agent analyzes the form layout before filling");
  console.log("   - It uses tab/click to navigate between fields");
}

main().catch(console.error);

