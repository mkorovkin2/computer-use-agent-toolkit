/**
 * Tool definitions for Claude computer use.
 */

export function createComputerToolSchema() {
  return {
    name: "computer",
    type: "computer_20241022",
    display_width_px: 1920,
    display_height_px: 1080,
    display_number: 1,
  };
}

export function createScreenshotTool() {
  return {
    name: "screenshot",
    description: "Take a screenshot of the current screen or a specific region",
    input_schema: {
      type: "object",
      properties: {
        region: {
          type: "object",
          description: "Optional region to capture",
          properties: {
            x: { type: "integer" },
            y: { type: "integer" },
            width: { type: "integer" },
            height: { type: "integer" },
          },
        },
      },
    },
  };
}

export function createMouseMoveTool() {
  return {
    name: "mouse_move",
    description: "Move the mouse cursor to specific coordinates",
    input_schema: {
      type: "object",
      properties: {
        x: { type: "integer", description: "X coordinate to move to" },
        y: { type: "integer", description: "Y coordinate to move to" },
        duration: { type: "number", description: "Duration of movement in seconds", default: 0.5 },
      },
      required: ["x", "y"],
    },
  };
}

export function createClickTool() {
  return {
    name: "click",
    description: "Click at specific coordinates",
    input_schema: {
      type: "object",
      properties: {
        x: { type: "integer", description: "X coordinate to click" },
        y: { type: "integer", description: "Y coordinate to click" },
        button: { type: "string", enum: ["left", "right", "middle"], default: "left" },
        clicks: { type: "integer", description: "Number of clicks", default: 1 },
      },
      required: ["x", "y"],
    },
  };
}

export function createTypeTool() {
  return {
    name: "type",
    description: "Type text using the keyboard",
    input_schema: {
      type: "object",
      properties: {
        text: { type: "string", description: "Text to type" },
        interval: { type: "number", description: "Interval between keystrokes", default: 0.0 },
      },
      required: ["text"],
    },
  };
}

export function createKeyTool() {
  return {
    name: "key",
    description: "Press a keyboard key",
    input_schema: {
      type: "object",
      properties: {
        key: { type: "string", description: "Key to press (e.g., 'enter', 'tab', 'escape')" },
      },
      required: ["key"],
    },
  };
}

export function createScrollTool() {
  return {
    name: "scroll",
    description: "Scroll in a direction",
    input_schema: {
      type: "object",
      properties: {
        direction: { type: "string", enum: ["up", "down", "left", "right"] },
        amount: { type: "integer", description: "Amount to scroll", default: 3 },
        x: { type: "integer", description: "Optional X coordinate" },
        y: { type: "integer", description: "Optional Y coordinate" },
      },
      required: ["direction"],
    },
  };
}

export function getDefaultTools() {
  return [
    createScreenshotTool(),
    createMouseMoveTool(),
    createClickTool(),
    createTypeTool(),
    createKeyTool(),
    createScrollTool(),
  ];
}

export function createCustomToolSchema(
  name: string,
  description: string,
  inputSchema: Record<string, any>
) {
  return { name, description, input_schema: inputSchema };
}

