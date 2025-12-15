# Computer Use Agent - TypeScript SDK

A powerful SDK for building computer use agents with Claude AI. Take screenshots, analyze them with Claude's vision capabilities, and execute real-world actions like clicks, typing, and scrolling.

## Installation

```bash
npm install computer-use-agent
```

## Quick Start

```typescript
import { ComputerUseAgent } from "computer-use-agent";

// Initialize agent
const agent = new ComputerUseAgent({
  apiKey: "your-anthropic-api-key",
  model: "claude-sonnet-4-20250514",
});

// Run agent with a goal
const result = await agent.run(
  "Open Chrome and navigate to github.com",
  10
);

console.log(`Success: ${result.success}`);
```

## Features

- 🖼️ **Screen Capture** - Capture full screen, windows, or custom regions
- 🤖 **Claude Integration** - Leverage Claude's vision and reasoning
- 🖱️ **Action Execution** - Click, type, scroll with safety controls
- 🔧 **Custom Tools** - Register your own tools
- 🎣 **Workflow Hooks** - Hook into the agent loop
- ✅ **Cross-Platform** - Works on macOS, Windows, and Linux

## Example: Custom Tools

```typescript
const agent = new ComputerUseAgent({ apiKey: "..." });

// Register custom tool
agent.tool("check_weather", "Check weather for a city", (args) => {
  return { temp: 72, condition: "sunny" };
});

// Run with custom tool access
await agent.run("Check the weather and display it on screen", 10);
```

## Example: Workflow Hooks

```typescript
// Log all actions
agent.onBeforeAction((context, action) => {
  console.log("About to execute:", action);
});

// Track metrics
agent.onAfterAction((context, action, result) => {
  if (!result.success) {
    console.log("Action failed:", result.error);
  }
});
```

## Documentation

See the main [README.md](../README.md) for full documentation.

## License

MIT

