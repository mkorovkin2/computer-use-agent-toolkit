/**
 * Example 04: Custom Tools
 *
 * This example shows how to extend the agent with custom tools:
 * - Register TypeScript functions as tools
 * - Mix UI interactions with API/database calls
 * - Create tools for external system integration
 *
 * Use case: Business workflows, system integration, data validation
 */

import { ComputerUseAgent } from "../../typescript/src";

const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) {
  console.error("❌ Please set ANTHROPIC_API_KEY environment variable");
  process.exit(1);
}

console.log("🤖 Computer Use Agent - Custom Tools Example");
console.log("=".repeat(60));

// Simulated databases
const inventoryDb: Record<string, any> = {
  "LAPTOP-001": { name: "MacBook Pro 16", stock: 5, price: 2499.99 },
  "LAPTOP-002": { name: "Dell XPS 15", stock: 0, price: 1899.99 },
  "PHONE-001": { name: "iPhone 15 Pro", stock: 12, price: 999.99 },
  "PHONE-002": { name: "Samsung S24", stock: 8, price: 899.99 },
};

const ordersDb: any[] = [];
const notificationsSent: any[] = [];

async function main() {
  // Initialize agent
  const agent = new ComputerUseAgent({
    apiKey,
    model: "claude-sonnet-4-20250514",
  });

  // Register custom tool: Check inventory
  agent.tool("check_inventory", "Check product inventory by SKU", (args: any) => {
    const sku = args.sku;
    console.log(`\n🔍 Checking inventory for SKU: ${sku}`);

    const product = inventoryDb[sku];
    if (!product) {
      return { error: `Product ${sku} not found`, in_stock: false };
    }

    const result = {
      sku,
      name: product.name,
      stock: product.stock,
      price: product.price,
      in_stock: product.stock > 0,
    };

    console.log(`   ✓ Found: ${product.name} - Stock: ${product.stock}`);
    return result;
  });

  // Register custom tool: Place order
  agent.tool("place_order", "Place an order for a product", (args: any) => {
    const { sku, quantity, customer_email } = args;
    console.log(`\n📦 Placing order: ${quantity}x ${sku} for ${customer_email}`);

    const product = inventoryDb[sku];
    if (!product) {
      return { success: false, error: "Product not found" };
    }

    if (product.stock < quantity) {
      return {
        success: false,
        error: `Insufficient stock. Available: ${product.stock}, Requested: ${quantity}`,
      };
    }

    // Create order
    const order = {
      order_id: `ORD-${String(ordersDb.length + 1).padStart(4, "0")}`,
      sku,
      product_name: product.name,
      quantity,
      customer_email,
      total: product.price * quantity,
      timestamp: new Date().toISOString(),
    };
    ordersDb.push(order);

    // Update inventory
    inventoryDb[sku].stock -= quantity;

    console.log(`   ✓ Order placed: ${order.order_id}`);
    return { success: true, order };
  });

  // Register custom tool: Send notification
  agent.tool("send_notification", "Send email notification", (args: any) => {
    const { to, subject, message } = args;
    console.log(`\n📧 Sending notification to: ${to}`);
    console.log(`   Subject: ${subject}`);
    console.log(`   Message: ${message.substring(0, 50)}...`);

    const notification = {
      to,
      subject,
      message,
      sent_at: new Date().toISOString(),
    };
    notificationsSent.push(notification);

    return { success: true, notification };
  });

  // Agent workflow
  const goal = `
You are an e-commerce assistant. Here's your task:

1. Look at the screen - there should be a product SKU displayed (like PHONE-001)
2. Use check_inventory to verify the product is in stock
3. If in stock:
   - Use place_order to order 2 units for customer: alice@example.com
   - Use send_notification to email the customer confirming their order
4. If out of stock:
   - Use send_notification to email the customer that the product is unavailable

For this demo, use SKU: PHONE-001
`;

  console.log(`\n🎯 Goal: E-commerce order processing workflow`);
  console.log(`\n📊 Initial Inventory:`);
  Object.entries(inventoryDb).forEach(([sku, product]) => {
    console.log(`   ${sku}: ${product.name} - Stock: ${product.stock}`);
  });

  console.log(`\n⏳ Running agent with custom tools...\n`);

  // Run agent
  const result = await agent.run(goal, 15);

  // Print results
  console.log("\n" + "=".repeat(60));
  console.log("📊 FINAL RESULTS");
  console.log("=".repeat(60));
  console.log(`✓ Success: ${result.success}`);
  console.log(`✓ Iterations: ${result.iterations}`);

  console.log(`\n📦 Orders Placed: ${ordersDb.length}`);
  ordersDb.forEach((order) => {
    console.log(
      `   ${order.order_id}: ${order.quantity}x ${order.product_name} - $${order.total.toFixed(2)}`
    );
  });

  console.log(`\n📧 Notifications Sent: ${notificationsSent.length}`);
  notificationsSent.forEach((notif) => {
    console.log(`   To: ${notif.to} - ${notif.subject}`);
  });

  console.log(`\n📊 Updated Inventory:`);
  Object.entries(inventoryDb).forEach(([sku, product]) => {
    console.log(`   ${sku}: ${product.name} - Stock: ${product.stock}`);
  });

  console.log("\n💡 Key Concepts:");
  console.log("   - Custom tools integrate external systems with UI automation");
  console.log("   - Tools can call databases, APIs, or any TypeScript code");
  console.log("   - Claude decides when to use each tool based on the goal");
  console.log("   - Mix UI actions (click, type) with custom tools seamlessly");
}

main().catch(console.error);

