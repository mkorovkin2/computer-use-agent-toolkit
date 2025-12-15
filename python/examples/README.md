# Computer Use Agent - Examples

This directory contains example agents demonstrating various features of the SDK.

## Setup

1. Install the package:
```bash
cd python
pip install -e .
```

2. Set your Anthropic API key:
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

## Examples

### 1. Simple Click (`simple_click.py`)
Basic example showing how to create an agent that clicks on an element.

```bash
python examples/simple_click.py
```

**Features demonstrated:**
- Basic agent initialization
- Simple goal execution
- Result handling

### 2. Form Filler (`form_filler.py`)
Fill out a web form with multiple fields using step-by-step iteration.

```bash
python examples/form_filler.py
```

**Features demonstrated:**
- Step-by-step execution with `run_iter()`
- Form interaction (clicking, typing)
- Real-time progress monitoring

### 3. Browser Navigator (`browser_navigator.py`)
Navigate a web browser and extract information.

```bash
python examples/browser_navigator.py
```

**Features demonstrated:**
- Multi-step navigation
- Custom system prompts
- Reading and understanding web content

### 4. Custom Tool Example (`custom_tool_example.py`)
Integrate custom tools that Claude can call alongside UI actions.

```bash
python examples/custom_tool_example.py
```

**Features demonstrated:**
- Custom tool registration with `@agent.tool()`
- Database queries
- Sending notifications
- Logging actions
- Mixing UI actions with API calls

### 5. Workflow Hooks Example (`workflow_hooks_example.py`)
Use hooks to add logging, metrics, and conditional logic.

```bash
python examples/workflow_hooks_example.py
```

**Features demonstrated:**
- Before/after action hooks
- Screenshot hooks
- Iteration hooks
- Tool call interception
- Conditional handlers with `@agent.when()`
- Metrics tracking

### 6. Multi-System Integration (`multi_system_integration.py`)
Build a complete workflow that combines UI interaction with external system integration.

```bash
python examples/multi_system_integration.py
```

**Features demonstrated:**
- Complex multi-step workflows
- Inventory checking
- Order placement
- Email notifications
- State management
- End-to-end business process automation

### 7. Human-in-the-Loop (`human_in_the_loop.py`)
Add approval gates and human oversight to agent workflows.

```bash
python examples/human_in_the_loop.py
```

**Features demonstrated:**
- Approval gates for sensitive actions
- Audit logging
- Checkpoints for human review
- Safety controls
- Interactive workflows

## Tips for Running Examples

1. **Screen Content**: Some examples expect specific UI elements. Make sure your screen shows relevant content for the agent to interact with.

2. **Safety**: All examples use safe defaults with rate limiting and safety delays. Adjust `safety_delay` and `confirmation_mode` as needed.

3. **Debugging**: Set `confirmation_mode="dry-run"` to test without actually executing actions.

4. **Logging**: Enable debug logging to see detailed execution:
```python
from computer_use_agent.utils import setup_logging
setup_logging(level="DEBUG")
```

## Creating Your Own Agent

Here's a minimal template:

```python
from computer_use_agent import ComputerUseAgent
import os

agent = ComputerUseAgent(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    model="claude-sonnet-4-20250514",
)

# Add custom tools
@agent.tool(name="my_tool")
def my_tool(arg: str) -> dict:
    return {"result": f"Processed: {arg}"}

# Add hooks
@agent.on_before_action
def log_action(context, action):
    print(f"Taking action: {action}")

# Run
result = agent.run(
    goal="Your goal here",
    max_iterations=10,
)

print(f"Success: {result['success']}")
```

## Troubleshooting

- **API Key Error**: Make sure `ANTHROPIC_API_KEY` is set
- **Import Error**: Install the package with `pip install -e .`
- **Screen Capture Error**: Ensure you have permissions for screen recording on macOS
- **Mouse/Keyboard Error**: Some systems require accessibility permissions

## Learn More

See the main README.md for full API documentation.

