/**
 * Type definitions for the Computer Use Agent SDK.
 */

export enum ActionType {
  SCREENSHOT = "screenshot",
  MOUSE_MOVE = "mouse_move",
  CLICK = "click",
  DOUBLE_CLICK = "double_click",
  TYPE = "type",
  KEY = "key",
  SCROLL = "scroll",
}

export enum ScrollDirection {
  UP = "up",
  DOWN = "down",
  LEFT = "left",
  RIGHT = "right",
}

export enum MouseButton {
  LEFT = "left",
  RIGHT = "right",
  MIDDLE = "middle",
}

export interface ScreenRegion {
  x: number;
  y: number;
  width: number;
  height: number;
}

export interface ActionResult {
  success: boolean;
  actionType: ActionType;
  error?: string;
  data?: Record<string, any>;
}

export interface AgentStep {
  iteration: number;
  action?: ActionType;
  reasoning?: string;
  result?: ActionResult;
  waitingForConfirmation?: boolean;
}

export class AgentContext {
  state: Record<string, any> = {};
  iteration: number = 0;
  actionHistory: ActionResult[] = [];
  lastScreenshot?: string;
  lastScreenshotText?: string;
}

export interface ToolDefinition {
  name: string;
  description: string;
  inputSchema: Record<string, any>;
  function: (...args: any[]) => any;
}

export type HookFunction = (context: AgentContext, ...args: any[]) => any;
export type ToolFunction = (...args: any[]) => any;

