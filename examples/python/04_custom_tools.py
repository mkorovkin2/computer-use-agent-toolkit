"""
Example 04: Custom Tools

This example shows how to extend the agent with custom tools:
- Register Python functions as tools
- Mix UI interactions with API/database calls
- Create tools for external system integration

Use case: Business workflows, system integration, data validation
"""

from computer_use_agent import ComputerUseAgent
import os
import json
from datetime import datetime

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("❌ Please set ANTHROPIC_API_KEY environment variable")
    exit(1)

print("🤖 Computer Use Agent - Custom Tools Example")
print("=" * 60)

# Initialize agent
agent = ComputerUseAgent(
    api_key=api_key,
    model="claude-sonnet-4-20250514",
)

# Simulated databases
inventory_db = {
    "LAPTOP-001": {"name": "MacBook Pro 16", "stock": 5, "price": 2499.99},
    "LAPTOP-002": {"name": "Dell XPS 15", "stock": 0, "price": 1899.99},
    "PHONE-001": {"name": "iPhone 15 Pro", "stock": 12, "price": 999.99},
    "PHONE-002": {"name": "Samsung S24", "stock": 8, "price": 899.99},
}

orders_db = []
notifications_sent = []


# Register custom tool: Check inventory
@agent.tool(name="check_inventory", description="Check product inventory by SKU")
def check_inventory(sku: str) -> dict:
    """Check if a product is in stock."""
    print(f"\n🔍 Checking inventory for SKU: {sku}")
    
    product = inventory_db.get(sku)
    if not product:
        return {"error": f"Product {sku} not found", "in_stock": False}
    
    result = {
        "sku": sku,
        "name": product["name"],
        "stock": product["stock"],
        "price": product["price"],
        "in_stock": product["stock"] > 0,
    }
    
    print(f"   ✓ Found: {product['name']} - Stock: {product['stock']}")
    return result


# Register custom tool: Place order
@agent.tool(name="place_order", description="Place an order for a product")
def place_order(sku: str, quantity: int, customer_email: str) -> dict:
    """Place an order if sufficient stock is available."""
    print(f"\n📦 Placing order: {quantity}x {sku} for {customer_email}")
    
    product = inventory_db.get(sku)
    if not product:
        return {"success": False, "error": "Product not found"}
    
    if product["stock"] < quantity:
        return {
            "success": False,
            "error": f"Insufficient stock. Available: {product['stock']}, Requested: {quantity}",
        }
    
    # Create order
    order = {
        "order_id": f"ORD-{len(orders_db) + 1:04d}",
        "sku": sku,
        "product_name": product["name"],
        "quantity": quantity,
        "customer_email": customer_email,
        "total": product["price"] * quantity,
        "timestamp": datetime.now().isoformat(),
    }
    orders_db.append(order)
    
    # Update inventory
    inventory_db[sku]["stock"] -= quantity
    
    print(f"   ✓ Order placed: {order['order_id']}")
    return {"success": True, "order": order}


# Register custom tool: Send notification
@agent.tool(name="send_notification", description="Send email notification")
def send_notification(to: str, subject: str, message: str) -> dict:
    """Send an email notification (simulated)."""
    print(f"\n📧 Sending notification to: {to}")
    print(f"   Subject: {subject}")
    print(f"   Message: {message[:50]}...")
    
    notification = {
        "to": to,
        "subject": subject,
        "message": message,
        "sent_at": datetime.now().isoformat(),
    }
    notifications_sent.append(notification)
    
    return {"success": True, "notification": notification}


# Agent workflow
goal = """
You are an e-commerce assistant. Here's your task:

1. Look at the screen - there should be a product SKU displayed (like PHONE-001)
2. Use check_inventory to verify the product is in stock
3. If in stock:
   - Use place_order to order 2 units for customer: alice@example.com
   - Use send_notification to email the customer confirming their order
4. If out of stock:
   - Use send_notification to email the customer that the product is unavailable

For this demo, use SKU: PHONE-001
"""

print(f"\n🎯 Goal: E-commerce order processing workflow")
print(f"\n📊 Initial Inventory:")
for sku, product in inventory_db.items():
    print(f"   {sku}: {product['name']} - Stock: {product['stock']}")

print(f"\n⏳ Running agent with custom tools...\n")

# Run agent
result = agent.run(goal=goal, max_iterations=15)

# Print results
print("\n" + "=" * 60)
print("📊 FINAL RESULTS")
print("=" * 60)
print(f"✓ Success: {result['success']}")
print(f"✓ Iterations: {result['iterations']}")

print(f"\n📦 Orders Placed: {len(orders_db)}")
for order in orders_db:
    print(f"   {order['order_id']}: {order['quantity']}x {order['product_name']} - ${order['total']:.2f}")

print(f"\n📧 Notifications Sent: {len(notifications_sent)}")
for notif in notifications_sent:
    print(f"   To: {notif['to']} - {notif['subject']}")

print(f"\n📊 Updated Inventory:")
for sku, product in inventory_db.items():
    print(f"   {sku}: {product['name']} - Stock: {product['stock']}")

print("\n💡 Key Concepts:")
print("   - Custom tools integrate external systems with UI automation")
print("   - Tools can call databases, APIs, or any Python code")
print("   - Claude decides when to use each tool based on the goal")
print("   - Mix UI actions (click, type) with custom tools seamlessly")

