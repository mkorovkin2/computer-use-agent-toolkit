"""
Example 08: Data Extraction

This example demonstrates extracting data from applications:
- Reading data from screens
- Extracting structured information
- Saving data to files
- Data validation and formatting

Use case: Web scraping, report generation, data migration
"""

from computer_use_agent import ComputerUseAgent
import os
import json
import csv
from datetime import datetime

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("❌ Please set ANTHROPIC_API_KEY environment variable")
    exit(1)

print("🤖 Computer Use Agent - Data Extraction Example")
print("=" * 60)

# Initialize agent
agent = ComputerUseAgent(
    api_key=api_key,
    model="claude-sonnet-4-20250514",
)

# Data storage
extracted_data = {
    "extraction_time": datetime.now().isoformat(),
    "source": "screen",
    "items": [],
}


# Custom tool: Save extracted data
@agent.tool(name="save_data_item", description="Save an extracted data item")
def save_data_item(
    name: str,
    value: str,
    data_type: str = "text",
    confidence: str = "high"
) -> dict:
    """Save a piece of extracted data."""
    
    item = {
        "name": name,
        "value": value,
        "type": data_type,
        "confidence": confidence,
        "extracted_at": datetime.now().isoformat(),
    }
    
    extracted_data["items"].append(item)
    
    print(f"\n💾 Data saved: {name} = {value}")
    return {"saved": True, "item": item}


# Custom tool: Validate data format
@agent.tool(name="validate_data", description="Validate extracted data format")
def validate_data(value: str, expected_format: str) -> dict:
    """Validate that data matches expected format."""
    
    import re
    
    formats = {
        "email": r'^[\w\.-]+@[\w\.-]+\.\w+$',
        "phone": r'^\+?1?\d{9,15}$',
        "url": r'^https?://[\w\.-]+\.\w+',
        "number": r'^\d+\.?\d*$',
    }
    
    pattern = formats.get(expected_format)
    if not pattern:
        return {"valid": False, "error": f"Unknown format: {expected_format}"}
    
    is_valid = bool(re.match(pattern, value))
    
    print(f"\n✓ Validation: {value} {'✓' if is_valid else '✗'} {expected_format}")
    
    return {
        "valid": is_valid,
        "value": value,
        "format": expected_format,
    }


# Custom tool: Export data to file
@agent.tool(name="export_to_file", description="Export extracted data to a file")
def export_to_file(filename: str, format: str = "json") -> dict:
    """Export all extracted data to a file."""
    
    output_dir = os.path.expanduser("~/Desktop")
    filepath = os.path.join(output_dir, filename)
    
    try:
        if format == "json":
            with open(filepath, 'w') as f:
                json.dump(extracted_data, f, indent=2)
        
        elif format == "csv":
            with open(filepath, 'w', newline='') as f:
                if extracted_data["items"]:
                    fieldnames = extracted_data["items"][0].keys()
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(extracted_data["items"])
        
        print(f"\n📄 Data exported to: {filepath}")
        print(f"   Format: {format}")
        print(f"   Items: {len(extracted_data['items'])}")
        
        return {
            "exported": True,
            "filepath": filepath,
            "format": format,
            "item_count": len(extracted_data["items"]),
        }
    
    except Exception as e:
        return {"exported": False, "error": str(e)}


# Workflow: Extract contact information from screen
goal = """
You are extracting contact information from the screen. Here's what to do:

1. Look at the screen for any visible contact information
2. Extract the following data points (if visible):
   - Name (use save_data_item with data_type="name")
   - Email (validate with validate_data format="email", then save)
   - Phone (validate with validate_data format="phone", then save)
   - Company name (use save_data_item with data_type="text")
   - Website URL (validate with validate_data format="url", then save)

3. After extracting all visible data:
   - Use export_to_file to save as "extracted_contacts.json"

For this demo, imagine the screen shows:
- Name: Sarah Johnson
- Email: sarah.johnson@techcorp.com
- Phone: +1-555-0199
- Company: TechCorp Industries
- Website: https://techcorp.com

Extract and save these items.
"""

print(f"\n🎯 Goal: Extract and save contact information")
print(f"\n📊 Expected data points: 5")
print(f"\n⏳ Running data extraction workflow...\n")

# Run agent
result = agent.run(goal=goal, max_iterations=20)

# Print results
print("\n" + "=" * 60)
print("📊 EXTRACTION RESULTS")
print("=" * 60)
print(f"✓ Success: {result['success']}")
print(f"✓ Iterations: {result['iterations']}")

print(f"\n📋 Extracted Data ({len(extracted_data['items'])} items):")
for i, item in enumerate(extracted_data['items'], 1):
    confidence_icon = "🟢" if item['confidence'] == "high" else "🟡"
    print(f"   {i}. {item['name']}: {item['value']}")
    print(f"      Type: {item['type']}, Confidence: {confidence_icon} {item['confidence']}")

print(f"\n📁 Output Files:")
output_dir = os.path.expanduser("~/Desktop")
json_file = os.path.join(output_dir, "extracted_contacts.json")
if os.path.exists(json_file):
    print(f"   ✓ {json_file}")
    print(f"     Size: {os.path.getsize(json_file)} bytes")

print("\n💡 Key Concepts:")
print("   - Agent reads and extracts data from screen")
print("   - Validates data formats before saving")
print("   - Exports to structured formats (JSON, CSV)")
print("   - Use case: Automating data entry, web scraping, report generation")
print("   - Can extract from any visible UI (apps, websites, PDFs)")

