"""
Example 09: Cross-Application Workflow

This example demonstrates working across multiple applications:
- Switching between applications
- Copying data from one app to another
- Coordinating complex multi-app workflows
- Managing application state

Use case: Data migration, report compilation, cross-system workflows
"""

from computer_use_agent import ComputerUseAgent
import os
import subprocess
import time

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("❌ Please set ANTHROPIC_API_KEY environment variable")
    exit(1)

print("🤖 Computer Use Agent - Cross-Application Example")
print("=" * 60)

# Initialize agent
agent = ComputerUseAgent(
    api_key=api_key,
    model="claude-sonnet-4-20250514",
)

# Track application switches
app_switches = []


# Custom tool: Switch to application
@agent.tool(name="switch_to_app", description="Switch to a specific application")
def switch_to_app(app_name: str) -> dict:
    """Bring an application to the foreground."""
    
    print(f"\n🔄 Switching to: {app_name}")
    
    try:
        # macOS: use 'open -a'
        if os.system('uname') == 0:  # Unix-like
            subprocess.run(['open', '-a', app_name], check=True)
        else:  # Windows
            subprocess.run(['start', '', app_name], shell=True, check=True)
        
        time.sleep(1.5)  # Wait for app to come to foreground
        
        app_switches.append({
            "app_name": app_name,
            "timestamp": time.time(),
        })
        
        print(f"   ✓ Switched to {app_name}")
        return {"success": True, "app": app_name}
    
    except Exception as e:
        print(f"   ✗ Failed to switch: {e}")
        return {"success": False, "error": str(e)}


# Custom tool: Check if application is running
@agent.tool(name="is_app_running", description="Check if an application is running")
def is_app_running(app_name: str) -> dict:
    """Check if an application is currently running."""
    
    try:
        # macOS/Linux
        result = subprocess.run(
            ['pgrep', '-i', app_name],
            capture_output=True,
            text=True
        )
        is_running = result.returncode == 0
        
        print(f"\n🔍 Checking {app_name}: {'Running ✓' if is_running else 'Not running ✗'}")
        
        return {
            "app_name": app_name,
            "is_running": is_running,
        }
    
    except Exception as e:
        return {"error": str(e), "is_running": False}


# Custom tool: Copy to clipboard
@agent.tool(name="copy_to_clipboard", description="Copy text to clipboard")
def copy_to_clipboard(text: str) -> dict:
    """Copy text to system clipboard."""
    
    try:
        # macOS
        process = subprocess.Popen(
            ['pbcopy'],
            stdin=subprocess.PIPE,
            close_fds=True
        )
        process.communicate(text.encode('utf-8'))
        
        print(f"\n📋 Copied to clipboard: {text[:50]}...")
        return {"success": True, "length": len(text)}
    
    except Exception as e:
        return {"success": False, "error": str(e)}


# Custom tool: Get clipboard content
@agent.tool(name="get_clipboard", description="Get text from clipboard")
def get_clipboard() -> dict:
    """Get current clipboard content."""
    
    try:
        # macOS
        result = subprocess.run(
            ['pbpaste'],
            capture_output=True,
            text=True,
            check=True
        )
        
        content = result.stdout
        print(f"\n📋 Clipboard content: {content[:50]}...")
        
        return {"success": True, "content": content}
    
    except Exception as e:
        return {"success": False, "error": str(e)}


# Workflow: Copy data between applications
goal = """
You need to copy data from one application to another. Here's the workflow:

1. Use switch_to_app to open "TextEdit"
2. In TextEdit, you should see some text. Select all (Cmd+A) and copy it (Cmd+C)
3. Use get_clipboard to verify the text was copied
4. Use switch_to_app to switch to "Notes"
5. In Notes, create a new note and paste the text (Cmd+N, then Cmd+V)
6. Use switch_to_app to switch back to "TextEdit"

This demonstrates coordinating actions across multiple applications.

For this demo, assume TextEdit has the text: "Sample data for cross-app workflow"
"""

print(f"\n🎯 Goal: Copy data from TextEdit to Notes")
print(f"\n📱 Applications involved: TextEdit, Notes")
print(f"\n⏳ Running cross-application workflow...\n")

# Hook: Track when agent switches apps
@agent.on_tool_call("switch_to_app")
def log_app_switch(context, args):
    """Log application switches."""
    context.state["current_app"] = args.get("app_name")
    return args

# Run agent
result = agent.run(goal=goal, max_iterations=20)

# Print results
print("\n" + "=" * 60)
print("📊 WORKFLOW RESULTS")
print("=" * 60)
print(f"✓ Success: {result['success']}")
print(f"✓ Iterations: {result['iterations']}")

print(f"\n🔄 Application Switches: {len(app_switches)}")
for i, switch in enumerate(app_switches, 1):
    print(f"   {i}. Switched to: {switch['app_name']}")

print(f"\n📱 Final Application: {agent.state.get('current_app', 'Unknown')}")

print("\n💡 Key Concepts:")
print("   - Agent coordinates actions across multiple applications")
print("   - Uses clipboard for data transfer between apps")
print("   - switch_to_app tool handles application focusing")
print("   - State tracking keeps track of current application")
print("\n📋 Real-world use cases:")
print("   - Copying data from spreadsheets to web forms")
print("   - Extracting data from PDFs to databases")
print("   - Compiling reports from multiple sources")
print("   - Automating repetitive cross-app tasks")

