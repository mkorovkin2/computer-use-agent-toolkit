"""
Example 06: Multi-System Integration

This example demonstrates integrating UI automation with backend systems:
- Database queries during UI workflows
- API calls triggered by screen events
- Email notifications based on UI state
- Complete end-to-end business process automation

Use case: Order processing, inventory management, CRM workflows
"""

from computer_use_agent import ComputerUseAgent
import os
from datetime import datetime

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("❌ Please set ANTHROPIC_API_KEY environment variable")
    exit(1)

print("🤖 Computer Use Agent - Multi-System Integration Example")
print("=" * 60)

# Initialize agent
agent = ComputerUseAgent(
    api_key=api_key,
    model="claude-sonnet-4-20250514",
)

# Simulated backend systems
class InventorySystem:
    """Simulated inventory management system."""
    
    def __init__(self):
        self.inventory = {
            "WIDGET-100": {"name": "Premium Widget", "qty": 150, "warehouse": "A"},
            "GADGET-200": {"name": "Super Gadget", "qty": 0, "warehouse": "B"},
            "TOOL-300": {"name": "Mega Tool", "qty": 75, "warehouse": "C"},
        }
    
    def check_stock(self, sku):
        """Check if product is in stock."""
        product = self.inventory.get(sku)
        if not product:
            return {"found": False, "error": "Product not found"}
        
        return {
            "found": True,
            "sku": sku,
            "name": product["name"],
            "quantity": product["qty"],
            "warehouse": product["warehouse"],
            "in_stock": product["qty"] > 0,
        }
    
    def reserve_stock(self, sku, quantity):
        """Reserve stock for an order."""
        product = self.inventory.get(sku)
        if not product or product["qty"] < quantity:
            return {"success": False, "error": "Insufficient stock"}
        
        product["qty"] -= quantity
        return {
            "success": True,
            "reserved": quantity,
            "remaining": product["qty"],
        }


class CRMSystem:
    """Simulated CRM system."""
    
    def __init__(self):
        self.customers = {
            "alice@example.com": {"name": "Alice Smith", "tier": "gold"},
            "bob@example.com": {"name": "Bob Jones", "tier": "silver"},
        }
    
    def get_customer(self, email):
        """Get customer information."""
        customer = self.customers.get(email)
        if not customer:
            return {"found": False}
        return {"found": True, "email": email, **customer}
    
    def log_interaction(self, email, interaction_type, notes):
        """Log customer interaction."""
        print(f"   📝 CRM: Logged {interaction_type} for {email}")
        return {"logged": True, "timestamp": datetime.now().isoformat()}


class NotificationSystem:
    """Simulated notification system."""
    
    def __init__(self):
        self.sent_notifications = []
    
    def send_email(self, to, subject, body):
        """Send email notification."""
        notification = {
            "to": to,
            "subject": subject,
            "body": body,
            "sent_at": datetime.now().isoformat(),
        }
        self.sent_notifications.append(notification)
        print(f"\n📧 Email sent to {to}")
        print(f"   Subject: {subject}")
        return {"sent": True, "notification_id": len(self.sent_notifications)}


# Initialize systems
inventory = InventorySystem()
crm = CRMSystem()
notifications = NotificationSystem()


# Register custom tools
@agent.tool(name="check_inventory", description="Check inventory for a product")
def check_inventory(sku: str) -> dict:
    """Check if product is available in inventory."""
    print(f"\n🔍 Checking inventory: {sku}")
    result = inventory.check_stock(sku)
    if result.get("found"):
        print(f"   ✓ Found: {result['name']} - Qty: {result['quantity']}")
    return result


@agent.tool(name="reserve_inventory", description="Reserve inventory for order")
def reserve_inventory(sku: str, quantity: int) -> dict:
    """Reserve inventory."""
    print(f"\n📦 Reserving {quantity}x {sku}")
    result = inventory.reserve_stock(sku, quantity)
    if result.get("success"):
        print(f"   ✓ Reserved. Remaining: {result['remaining']}")
    return result


@agent.tool(name="get_customer_info", description="Get customer from CRM")
def get_customer_info(email: str) -> dict:
    """Look up customer information."""
    print(f"\n👤 Looking up customer: {email}")
    result = crm.get_customer(email)
    if result.get("found"):
        print(f"   ✓ Found: {result['name']} ({result['tier']} tier)")
    return result


@agent.tool(name="log_crm_interaction", description="Log interaction in CRM")
def log_crm_interaction(email: str, interaction_type: str, notes: str) -> dict:
    """Log customer interaction."""
    return crm.log_interaction(email, interaction_type, notes)


@agent.tool(name="send_customer_email", description="Send email to customer")
def send_customer_email(to: str, subject: str, body: str) -> dict:
    """Send email notification."""
    return notifications.send_email(to, subject, body)


# Workflow: Process an order found on screen
goal = """
You are processing an order. Here's the workflow:

1. Look at the screen for order details (product SKU and customer email)
2. Use get_customer_info to look up the customer
3. Use check_inventory to verify the product is in stock
4. If in stock:
   a. Use reserve_inventory to reserve 5 units
   b. Use send_customer_email to confirm the order
   c. Use log_crm_interaction to log "order_placed"
5. If out of stock:
   a. Use send_customer_email to notify customer
   b. Use log_crm_interaction to log "stock_unavailable"

For this demo:
- Product SKU: WIDGET-100
- Customer email: alice@example.com
- Quantity: 5
"""

print(f"\n🎯 Goal: Process order with multi-system integration")
print(f"\n🗄️  Initial State:")
print(f"   Inventory: {inventory.inventory['WIDGET-100']['qty']} units of WIDGET-100")
print(f"   Customer: {crm.customers['alice@example.com']['name']}")

print(f"\n⏳ Running integrated workflow...\n")

# Run agent
result = agent.run(goal=goal, max_iterations=15)

# Print results
print("\n" + "=" * 60)
print("📊 FINAL RESULTS")
print("=" * 60)
print(f"✓ Success: {result['success']}")
print(f"✓ Iterations: {result['iterations']}")

print(f"\n🗄️  Updated Inventory:")
for sku, product in inventory.inventory.items():
    print(f"   {sku}: {product['name']} - Qty: {product['qty']}")

print(f"\n📧 Notifications Sent: {len(notifications.sent_notifications)}")
for notif in notifications.sent_notifications:
    print(f"   To: {notif['to']}")
    print(f"   Subject: {notif['subject']}")

print("\n💡 Key Concepts:")
print("   - Agent coordinates between UI and multiple backend systems")
print("   - Tools represent different system integrations")
print("   - Complete business workflows with proper error handling")
print("   - Real-world use: Order processing, CRM updates, notifications")

