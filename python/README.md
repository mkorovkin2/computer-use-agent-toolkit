# Computer Use Agent - Python SDK

A powerful SDK for building computer use agents with Claude AI. Take screenshots, analyze them with Claude's vision capabilities, and execute real-world actions like clicks, typing, and scrolling.

## Quick Setup (First Time)

**The easiest way to get started:**

```bash
cd python
./first-time-setup.sh
```

This script will:
- ✅ Create a virtual environment
- ✅ Upgrade pip to the latest version
- ✅ Install the package in editable mode
- ✅ Optionally install dev dependencies
- ✅ Verify the installation

## Manual Installation

If you prefer to install manually:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install the package
pip install -e .

# Or with dev dependencies
pip install -e ".[dev]"
```

## Quick Start

```python
from computer_use_agent import ComputerUseAgent

# Initialize agent
agent = ComputerUseAgent(
    api_key="your-anthropic-api-key",
    model="claude-sonnet-4.5"
)

# Run agent with a goal
result = agent.run(
    goal="Open Chrome and navigate to github.com",
    max_iterations=10
)
```

## Features

- 🖼️ **Screen Capture** - Capture full screen, windows, or custom regions
- 🤖 **Claude Integration** - Leverage Claude's vision and reasoning for UI understanding
- 🖱️ **Action Execution** - Click, type, scroll, and more with safety controls
- 🔧 **Custom Tools** - Register your own tools that Claude can call
- 🎣 **Workflow Hooks** - Hook into the agent loop for custom logic
- 🔄 **State Management** - Share state across workflow steps
- ✅ **Cross-Platform** - Works on macOS, Windows, and Linux

## Documentation

See the [examples](./examples/) directory for more usage patterns.

## License

MIT

