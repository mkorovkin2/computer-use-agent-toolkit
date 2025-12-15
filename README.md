# Computer Use Agent Toolkit

A powerful, flexible SDK for building computer use agents with Claude AI. Take screenshots, analyze them with Claude's vision capabilities, and execute real-world actions like clicks, typing, and scrolling - all with a simple, intuitive API.

## 🌟 Features

- **🖼️ Screen Capture** - Capture full screen, specific windows, or custom regions
- **🤖 Claude Integration** - Leverage Claude's vision and reasoning for UI understanding  
- **🖱️ Action Execution** - Click, type, scroll, and more with safety controls
- **🔧 Custom Tools** - Register your own tools that Claude can call alongside UI actions
- **🎣 Workflow Hooks** - Hook into any point in the agent loop for custom logic
- **🔄 State Management** - Share state across workflow steps
- **⚡ Conditional Logic** - Define "if X then Y" workflows with simple decorators
- **✅ Cross-Platform** - Works on macOS, Windows, and Linux
- **🛡️ Safety First** - Built-in rate limiting, safety delays, and confirmation modes

## 🚀 Quick Start

### Installation

**Option 1: Automated Setup (Recommended)**

```bash
cd python
./first-time-setup.sh
```

This interactive script will set up everything for you!

**Option 2: Manual Setup**

```bash
cd python
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -e .
```

**Set your API key:**

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

### Basic Usage

```python
from computer_use_agent import ComputerUseAgent

# Initialize agent
agent = ComputerUseAgent(
    api_key="your-anthropic-api-key",
    model="claude-sonnet-4-20250514"
)

# Run agent with a goal
result = agent.run(
    goal="Open Chrome and navigate to github.com",
    max_iterations=10
)

print(f"Success: {result['success']}")
```

That's it! The agent will:
1. Take a screenshot
2. Send it to Claude to analyze
3. Claude decides what action to take
4. Execute the action
5. Repeat until goal is achieved

## 📖 Core Concepts

### The Agent Loop

The SDK implements a continuous loop:

```
Screenshot → Analyze (Claude) → Decide (Claude) → Act → Screenshot → ...
```

Claude sees the screen, understands the UI, and determines what actions to take to achieve your goal.

### Built-in Actions

The agent can perform these actions out of the box:

- `screenshot` - Capture screen
- `mouse_move` - Move cursor
- `click` - Click at coordinates  
- `type` - Type text
- `key` - Press keyboard keys
- `scroll` - Scroll in any direction

### Custom Tools

Extend the agent with your own tools:

```python
@agent.tool(name="check_weather")
def check_weather(city: str) -> dict:
    """Check weather for a city"""
    # Your custom logic here
    return {"temp": 72, "condition": "sunny"}

# Claude can now call check_weather while interacting with the UI
```

### Workflow Hooks

Hook into the agent loop for custom logic:

```python
@agent.on_before_action
def log_action(context, action):
    print(f"About to execute: {action}")

@agent.on_after_action  
def check_result(context, action, result):
    if not result.success:
        print(f"Action failed: {result.error}")
```

### Conditional Logic

Define conditional workflows:

```python
# If agent clicks on right side, do something
@agent.when("click", lambda ctx, action: action["x"] > 1000)
def on_right_click(context, action):
    print("Clicked on right side!")
    agent.call_tool("send_notification", message="Right click detected")
```

## 🎯 Examples

### 1. Simple Click

```python
agent = ComputerUseAgent(api_key="...")
result = agent.run(
    goal="Click on the Safari icon",
    max_iterations=5
)
```

### 2. Form Filling

```python
agent = ComputerUseAgent(api_key="...")
result = agent.run(
    goal="""
    Fill out the form with:
    Name: John Doe
    Email: john@example.com
    Message: Hello!
    Then click Submit.
    """,
    max_iterations=15
)
```

### 3. Multi-System Integration

```python
agent = ComputerUseAgent(api_key="...")

# Register custom tool
@agent.tool(name="check_inventory")
def check_inventory(product_id: str) -> dict:
    return db.query("SELECT * FROM inventory WHERE id = ?", product_id)

# Agent can now interact with UI AND call your database
result = agent.run(
    goal="Find product X on the website and check if it's in stock",
    max_iterations=20
)
```

### 4. Human-in-the-Loop

```python
@agent.on_before_action
def require_approval(context, action):
    if "delete" in str(action):
        if input("Allow delete? (y/n): ") != "y":
            raise Exception("Action cancelled")

result = agent.run(goal="Delete old files from Downloads")
```

## 📚 Full API Documentation

### ComputerUseAgent

Main agent class.

#### Constructor

```python
ComputerUseAgent(
    api_key: str,
    model: str = "claude-sonnet-4-20250514",
    screen_region: Optional[ScreenRegion] = None,
    allowed_action_region: Optional[ScreenRegion] = None,
    safety_delay: float = 0.1,
    confirmation_mode: str = "auto",
    max_tokens: int = 4096,
)
```

**Parameters:**
- `api_key`: Anthropic API key
- `model`: Claude model to use
- `screen_region`: Optional region to capture (default: full screen)
- `allowed_action_region`: Optional region where actions are allowed
- `safety_delay`: Delay after each action (seconds)
- `confirmation_mode`: "auto", "confirm", or "dry-run"
- `max_tokens`: Max tokens for Claude responses

#### Methods

##### `run(goal, max_iterations=20, system_prompt=None)`

Run the agent to completion.

**Returns:** Dict with results

```python
{
    "success": bool,
    "iterations": int,
    "state": dict,
    "action_history": list,
}
```

##### `run_iter(goal, max_iterations=20, system_prompt=None)`

Run the agent with step-by-step control. Yields `AgentStep` objects.

```python
for step in agent.run_iter(goal="..."):
    print(f"Iteration: {step.iteration}")
    print(f"Action: {step.action}")
    print(f"Reasoning: {step.reasoning}")
```

##### `tool(name=None, description=None, input_schema=None)`

Decorator to register a custom tool.

```python
@agent.tool(name="my_tool")
def my_tool(arg: str) -> dict:
    return {"result": arg}
```

##### `call_tool(tool_name, **kwargs)`

Call a custom tool directly.

```python
result = agent.call_tool("my_tool", arg="value")
```

#### Hook Decorators

- `@agent.on_before_screenshot` - Before taking screenshot
- `@agent.on_after_screenshot` - After taking screenshot
- `@agent.on_before_action` - Before executing action
- `@agent.on_after_action` - After executing action
- `@agent.on_tool_call(tool_name=None)` - When tool is called
- `@agent.on_iteration_start` - Start of each iteration
- `@agent.on_iteration_end` - End of each iteration
- `@agent.when(action_type, condition)` - Conditional handler

#### Properties

- `agent.state` - Access agent state dict

### Type Definitions

#### ScreenRegion

```python
ScreenRegion(x: int, y: int, width: int, height: int)
```

#### ActionResult

```python
ActionResult(
    success: bool,
    action_type: ActionType,
    error: Optional[str] = None,
    data: Optional[Dict] = None,
)
```

#### AgentContext

Passed to hook functions:

```python
context.state                  # State dict
context.iteration              # Current iteration
context.action_history         # List of ActionResults
context.last_screenshot        # Last screenshot (base64)
context.last_screenshot_text   # Text from last screenshot
```

## 🛡️ Safety & Best Practices

### Safety Features

1. **Rate Limiting** - Automatic delays between actions
2. **Allowed Regions** - Restrict actions to specific screen areas
3. **Confirmation Mode** - Require approval for actions
4. **Dry Run Mode** - Test without executing actions
5. **Failsafe** - PyAutoGUI failsafe (move mouse to corner to stop)

### Best Practices

1. **Start with dry-run mode** for testing:
   ```python
   agent = ComputerUseAgent(api_key="...", confirmation_mode="dry-run")
   ```

2. **Use allowed regions** to prevent accidents:
   ```python
   safe_region = ScreenRegion(x=100, y=100, width=800, height=600)
   agent = ComputerUseAgent(api_key="...", allowed_action_region=safe_region)
   ```

3. **Add logging** for debugging:
   ```python
   from computer_use_agent.utils import setup_logging
   setup_logging(level="DEBUG")
   ```

4. **Use human-in-the-loop** for sensitive operations:
   ```python
   @agent.on_before_action
   def require_approval(context, action):
       if is_sensitive(action):
           if not confirm("Allow action?"):
               raise Exception("Cancelled")
   ```

5. **Set reasonable max_iterations** to prevent runaway agents

## 🏗️ Architecture

```
┌─────────────────┐
│   User Code     │
└────────┬────────┘
         │
┌────────▼─────────────┐
│ ComputerUseAgent     │
│  - Agent Loop        │
│  - State Management  │
└───┬────────────┬─────┘
    │            │
┌───▼──────┐ ┌──▼──────────┐
│ Screen   │ │ Claude API  │
│ Capture  │ │ (Vision +   │
└──────────┘ │  Reasoning) │
             └──────┬───────┘
                    │
        ┌───────────▼───────────┐
        │   Workflow Engine     │
        │  - Custom Tools       │
        │  - Hooks              │
        │  - Conditional Logic  │
        └───┬───────────┬───────┘
            │           │
   ┌────────▼──────┐ ┌──▼──────────┐
   │ Built-in      │ │ Custom      │
   │ Actions       │ │ Tools       │
   │ (click,type)  │ │ (user code) │
   └───────────────┘ └─────────────┘
```

## 🧪 Testing

Run tests:

```bash
cd python
pytest tests/
```

Run a specific test:

```bash
pytest tests/test_agent.py::test_basic_agent
```

## 🗺️ Roadmap

- [x] Python SDK with full feature set
- [ ] TypeScript/JavaScript SDK
- [ ] Browser-specific tools (navigate, fill forms)
- [ ] OCR integration for better text extraction
- [ ] Recording and replay of agent sessions
- [ ] Visual debugging tools
- [ ] Cloud deployment helpers

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Built on [Anthropic's Claude](https://www.anthropic.com/claude) AI
- Inspired by Claude's computer use capabilities
- Uses PyAutoGUI, Pillow, MSS for cross-platform support

## 📞 Support

- 📖 [Full Documentation](./docs/)
- 💬 [GitHub Issues](https://github.com/computer-use-agent-toolkit/issues)
- 📧 Email: support@example.com

---

**Built with ❤️ for the AI agent community**
