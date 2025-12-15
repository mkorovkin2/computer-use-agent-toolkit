"""
Example: Using custom tools to integrate with external systems.
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

# Simulated database
fake_database = {
    "users": [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"},
        {"id": 3, "name": "Charlie", "email": "charlie@example.com"},
    ],
    "products": [
        {"id": 101, "name": "Widget", "price": 29.99, "stock": 15},
        {"id": 102, "name": "Gadget", "price": 49.99, "stock": 8},
        {"id": 103, "name": "Doohickey", "price": 19.99, "stock": 0},
    ],
}

# Register custom tool to query database
@agent.tool(
    name="query_database",
    description="Query the database for user or product information"
)
def query_database(table: str, id: int) -> dict:
    """Query the simulated database."""
    if table not in fake_database:
        return {"error": f"Table '{table}' not found"}
    
    items = fake_database[table]
    for item in items:
        if item["id"] == id:
            return {"success": True, "data": item}
    
    return {"error": f"Item with id {id} not found in {table}"}

# Register custom tool to send notification
@agent.tool(name="send_notification")
def send_notification(message: str, priority: str = "normal") -> dict:
    """Send a notification (simulated)."""
    print(f"\n📧 NOTIFICATION [{priority.upper()}]: {message}\n")
    return {"sent": True, "message": message, "priority": priority}

# Register custom tool to log action
@agent.tool(name="log_action")
def log_action(action: str, details: str) -> dict:
    """Log an action to the system log."""
    print(f"\n📝 LOG: {action} - {details}\n")
    return {"logged": True}

# Run agent with access to custom tools
result = agent.run(
    goal=(
        "1. Check the screen for any product displayed\n"
        "2. Use query_database to look up product 102 from the products table\n"
        "3. If the product is in stock, send a high priority notification saying 'Product available'\n"
        "4. If out of stock, send a normal notification saying 'Product unavailable'\n"
        "5. Log the action you took"
    ),
    max_iterations=10,
)

print(f"\n{'='*60}")
print(f"Custom tool example completed!")
print(f"Success: {result['success']}")
print(f"Iterations: {result['iterations']}")
print(f"Final state: {json.dumps(result['state'], indent=2)}")
print(f"{'='*60}")

