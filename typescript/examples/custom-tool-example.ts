/**
 * Example: Using custom tools.
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

  // Simulated database
  const fakeDatabase = {
    products: [
      { id: 101, name: "Widget", price: 29.99, stock: 15 },
      { id: 102, name: "Gadget", price: 49.99, stock: 8 },
      { id: 103, name: "Doohickey", price: 19.99, stock: 0 },
    ],
  };

  // Register custom tool
  agent.tool("query_database", "Query the database for product information", (args: any) => {
    const product = fakeDatabase.products.find((p) => p.id === args.id);
    if (!product) {
      return { error: `Product with id ${args.id} not found` };
    }
    return { success: true, data: product };
  });

  // Register notification tool
  agent.tool("send_notification", "Send a notification", (args: any) => {
    console.log(`\n📧 NOTIFICATION [${args.priority?.toUpperCase()}]: ${args.message}\n`);
    return { sent: true, message: args.message, priority: args.priority };
  });

  const result = await agent.run(
    "Use query_database to look up product 102. " +
      "If in stock, send a high priority notification saying 'Product available'. " +
      "If out of stock, send a normal notification saying 'Product unavailable'.",
    10
  );

  console.log("\n" + "=".repeat(60));
  console.log("Custom tool example completed!");
  console.log(`Success: ${result.success}`);
  console.log(`Iterations: ${result.iterations}`);
  console.log(`Final state: ${JSON.stringify(result.state, null, 2)}`);
  console.log("=".repeat(60));
}

main().catch(console.error);

