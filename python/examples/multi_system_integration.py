"""
Example: Multi-system integration - UI interaction + API calls.
"""

from computer_use_agent import ComputerUseAgent
import os
import json

api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    print("Please set ANTHROPIC_API_KEY environment variable")
    exit(1)

# Initialize agent
agent = ComputerUseAgent(
    api_key=api_key,
    model="claude-sonnet-4-20250514",
)

# Simulated inventory system
inventory = {
    "WIDGET-001": {"name": "Premium Widget", "quantity": 150, "location": "Warehouse A"},
    "GADGET-002": {"name": "Super Gadget", "quantity": 0, "location": "Warehouse B"},
    "TOOL-003": {"name": "Mega Tool", "quantity": 75, "location": "Warehouse C"},
}

# Simulated order system
orders = []

# Register tool to check inventory
@agent.tool(name="check_inventory")
def check_inventory(product_code: str) -> dict:
    """Check inventory for a product code."""
    product = inventory.get(product_code)
    if not product:
        return {"error": f"Product {product_code} not found", "in_stock": False}
    
    return {
        "product_code": product_code,
        "name": product["name"],
        "quantity": product["quantity"],
        "location": product["location"],
        "in_stock": product["quantity"] > 0,
    }

# Register tool to place order
@agent.tool(name="place_order")
def place_order(product_code: str, quantity: int, customer_email: str) -> dict:
    """Place an order for a product."""
    product = inventory.get(product_code)
    
    if not product:
        return {"success": False, "error": "Product not found"}
    
    if product["quantity"] < quantity:
        return {
            "success": False,
            "error": f"Insufficient stock. Available: {product['quantity']}, Requested: {quantity}"
        }
    
    # Create order
    order = {
        "order_id": f"ORD-{len(orders) + 1:04d}",
        "product_code": product_code,
        "product_name": product["name"],
        "quantity": quantity,
        "customer_email": customer_email,
        "status": "pending",
    }
    orders.append(order)
    
    # Update inventory
    inventory[product_code]["quantity"] -= quantity
    
    return {
        "success": True,
        "order_id": order["order_id"],
        "message": f"Order placed successfully for {quantity}x {product['name']}",
    }

# Register tool to send email
@agent.tool(name="send_email")
def send_email(to: str, subject: str, body: str) -> dict:
    """Send an email (simulated)."""
    print(f"\n📧 EMAIL SENT")
    print(f"To: {to}")
    print(f"Subject: {subject}")
    print(f"Body: {body}\n")
    return {"sent": True, "to": to}

# Hook to auto-send confirmation email after order
@agent.on_after_action
def auto_email_on_order(context, action, result):
    if result.success and result.data and "order_id" in str(result.data):
        # Check if we just placed an order
        if "place_order" in str(context.action_history[-1:]):
            print("🎉 Order detected! Sending confirmation email...")

# Run agent with multi-system workflow
result = agent.run(
    goal=(
        "You are an order processing assistant. Here's what you need to do:\n\n"
        "1. Look at the screen for any product code displayed (like WIDGET-001)\n"
        "2. Use check_inventory to verify the product is in stock\n"
        "3. If in stock, use place_order to order 10 units for customer john@example.com\n"
        "4. If the order succeeds, use send_email to send a confirmation to the customer\n"
        "5. If out of stock, send an email saying the product is unavailable\n\n"
        "Product to check: WIDGET-001"
    ),
    max_iterations=10,
)

# Print results
print(f"\n{'='*60}")
print("WORKFLOW COMPLETE")
print(f"{'='*60}")
print(f"Success: {result['success']}")
print(f"Iterations: {result['iterations']}")
print(f"\nOrders placed: {len(orders)}")
for order in orders:
    print(f"  - {order['order_id']}: {order['quantity']}x {order['product_name']}")
print(f"\nUpdated Inventory:")
for code, product in inventory.items():
    print(f"  - {code}: {product['quantity']} units in {product['location']}")
print(f"{'='*60}")

