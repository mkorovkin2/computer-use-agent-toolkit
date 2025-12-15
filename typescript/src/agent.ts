/**
 * Main agent class that orchestrates the computer use agent loop.
 */

import Anthropic from "@anthropic-ai/sdk";
import { ScreenCapture } from "./screen";
import { ActionExecutor } from "./actions";
import { WorkflowEngine } from "./workflow";
import { HookRegistry } from "./hooks";
import { getDefaultTools } from "./tools";
import {
  ActionResult,
  ActionType,
  AgentContext,
  AgentStep,
  MouseButton,
  ScreenRegion,
  ScrollDirection,
} from "./types";

export interface ComputerUseAgentConfig {
  apiKey: string;
  model?: string;
  screenRegion?: ScreenRegion;
  allowedActionRegion?: ScreenRegion;
  safetyDelay?: number;
  confirmationMode?: string;
  maxTokens?: number;
}

export class ComputerUseAgent {
  private client: Anthropic;
  private screen: ScreenCapture;
  private executor: ActionExecutor;
  private workflow: WorkflowEngine;
  private hooks: HookRegistry;
  private context: AgentContext;
  private messages: any[] = [];
  private model: string;
  private maxTokens: number;

  constructor(config: ComputerUseAgentConfig) {
    this.client = new Anthropic({ apiKey: config.apiKey });
    this.screen = new ScreenCapture(config.screenRegion);
    this.executor = new ActionExecutor(
      config.allowedActionRegion,
      config.safetyDelay ?? 0.1,
      config.confirmationMode ?? "auto"
    );
    this.workflow = new WorkflowEngine();
    this.hooks = new HookRegistry();
    this.context = new AgentContext();
    this.model = config.model ?? "claude-sonnet-4-20250514";
    this.maxTokens = config.maxTokens ?? 4096;
  }

  get state(): Record<string, any> {
    return this.context.state;
  }

  tool(name: string, description: string, func: Function): void {
    this.workflow.registerTool(name, description, func);
  }

  onBeforeScreenshot(func: (context: AgentContext) => void): void {
    this.hooks.registerBeforeScreenshot(func);
  }

  onAfterScreenshot(func: (context: AgentContext, image: any) => void): void {
    this.hooks.registerAfterScreenshot(func);
  }

  onBeforeAction(func: (context: AgentContext, action: any) => void): void {
    this.hooks.registerBeforeAction(func);
  }

  onAfterAction(func: (context: AgentContext, action: any, result: any) => void): void {
    this.hooks.registerAfterAction(func);
  }

  onToolCall(toolName: string | null, func: (context: AgentContext, ...args: any[]) => void): void {
    this.hooks.registerOnToolCall(toolName, func);
  }

  onIterationStart(func: (context: AgentContext, iteration: number) => void): void {
    this.hooks.registerOnIterationStart(func);
  }

  onIterationEnd(func: (context: AgentContext, iteration: number) => void): void {
    this.hooks.registerOnIterationEnd(func);
  }

  when(
    actionType: string,
    condition: (ctx: AgentContext, action: any) => boolean,
    handler: (ctx: AgentContext, action: any) => void
  ): void {
    this.workflow.registerConditionalHandler(actionType, condition, handler);
  }

  callTool(toolName: string, args: Record<string, any>): any {
    return this.workflow.executeTool(toolName, args);
  }

  private buildTools(): any[] {
    return [...getDefaultTools(), ...this.workflow.getToolSchemas()];
  }

  private async takeScreenshot(): Promise<string> {
    this.hooks.triggerBeforeScreenshot(this.context);
    const imageB64 = await this.screen.captureBase64();
    this.context.lastScreenshot = imageB64;
    this.hooks.triggerAfterScreenshot(this.context, imageB64);
    return imageB64;
  }

  private async executeTool(toolName: string, toolInput: Record<string, any>): Promise<ActionResult> {
    const modifiedInput = this.hooks.triggerOnToolCall(this.context, toolName, toolInput);

    // Check custom tools
    if (this.workflow.hasTool(toolName)) {
      try {
        const result = this.workflow.executeTool(toolName, modifiedInput);
        return {
          success: true,
          actionType: ActionType.SCREENSHOT,
          data: { result },
        };
      } catch (error) {
        return {
          success: false,
          actionType: ActionType.SCREENSHOT,
          error: String(error),
        };
      }
    }

    // Handle built-in tools
    let result: ActionResult;

    switch (toolName) {
      case "screenshot":
        const imageB64 = await this.takeScreenshot();
        result = {
          success: true,
          actionType: ActionType.SCREENSHOT,
          data: { image: imageB64 },
        };
        break;

      case "mouse_move":
        const action1 = this.hooks.triggerBeforeAction(this.context, modifiedInput);
        result = await this.executor.mouseMove(action1.x, action1.y, action1.duration ?? 0.5);
        this.hooks.triggerAfterAction(this.context, modifiedInput, result);
        this.workflow.checkConditionalHandlers(this.context, "mouse_move", modifiedInput);
        break;

      case "click":
        const action2 = this.hooks.triggerBeforeAction(this.context, modifiedInput);
        result = await this.executor.click(
          action2.x,
          action2.y,
          action2.button ?? MouseButton.LEFT,
          action2.clicks ?? 1
        );
        this.hooks.triggerAfterAction(this.context, modifiedInput, result);
        this.workflow.checkConditionalHandlers(this.context, "click", modifiedInput);
        break;

      case "type":
        const action3 = this.hooks.triggerBeforeAction(this.context, modifiedInput);
        result = await this.executor.typeText(action3.text, action3.interval ?? 0.0);
        this.hooks.triggerAfterAction(this.context, modifiedInput, result);
        this.workflow.checkConditionalHandlers(this.context, "type", modifiedInput);
        break;

      case "key":
        const action4 = this.hooks.triggerBeforeAction(this.context, modifiedInput);
        result = await this.executor.pressKey(action4.key);
        this.hooks.triggerAfterAction(this.context, modifiedInput, result);
        this.workflow.checkConditionalHandlers(this.context, "key", modifiedInput);
        break;

      case "scroll":
        const action5 = this.hooks.triggerBeforeAction(this.context, modifiedInput);
        result = await this.executor.scroll(
          action5.direction as ScrollDirection,
          action5.amount ?? 3,
          action5.x,
          action5.y
        );
        this.hooks.triggerAfterAction(this.context, modifiedInput, result);
        this.workflow.checkConditionalHandlers(this.context, "scroll", modifiedInput);
        break;

      default:
        result = {
          success: false,
          actionType: ActionType.SCREENSHOT,
          error: `Unknown tool: ${toolName}`,
        };
    }

    return result;
  }

  async run(
    goal: string,
    maxIterations: number = 20,
    systemPrompt?: string
  ): Promise<Record<string, any>> {
    this.context = new AgentContext();
    this.messages = [];

    const initialScreenshot = await this.takeScreenshot();

    this.messages.push({
      role: "user",
      content: [
        {
          type: "image",
          source: {
            type: "base64",
            media_type: "image/png",
            data: initialScreenshot,
          },
        },
        {
          type: "text",
          text: goal,
        },
      ],
    });

    const system =
      systemPrompt ||
      "You are a computer use agent. You can see the screen and take actions " +
        "like clicking, typing, and scrolling. Analyze what you see and take " +
        "appropriate actions to achieve the given goal.";

    for (let iteration = 0; iteration < maxIterations; iteration++) {
      this.context.iteration = iteration;
      this.hooks.triggerOnIterationStart(this.context, iteration);

      try {
        const response = await this.client.messages.create({
          model: this.model,
          max_tokens: this.maxTokens,
          system,
          messages: this.messages,
          tools: this.buildTools(),
        });

        this.messages.push({
          role: "assistant",
          content: response.content,
        });

        if (response.stop_reason === "end_turn") {
          this.hooks.triggerOnIterationEnd(this.context, iteration);
          break;
        }

        if (response.stop_reason === "tool_use") {
          const toolResults: any[] = [];

          for (const block of response.content) {
            if (block.type === "tool_use") {
              const result = await this.executeTool(block.name, block.input);
              this.context.actionHistory.push(result);

              const toolResultContent: any[] = [];

              if (result.success) {
                if (block.name === "screenshot" && result.data) {
                  toolResultContent.push({
                    type: "image",
                    source: {
                      type: "base64",
                      media_type: "image/png",
                      data: result.data.image,
                    },
                  });
                } else {
                  toolResultContent.push({
                    type: "text",
                    text: `Success: ${JSON.stringify(result.data)}`,
                  });
                }
              } else {
                toolResultContent.push({
                  type: "text",
                  text: `Error: ${result.error}`,
                });
              }

              toolResults.push({
                type: "tool_result",
                tool_use_id: block.id,
                content: toolResultContent,
              });
            }
          }

          this.messages.push({
            role: "user",
            content: toolResults,
          });
        }

        this.hooks.triggerOnIterationEnd(this.context, iteration);
      } catch (error) {
        return {
          success: false,
          error: String(error),
          iteration,
          state: this.context.state,
        };
      }
    }

    return {
      success: true,
      iterations: this.context.iteration + 1,
      state: this.context.state,
      actionHistory: this.context.actionHistory,
    };
  }
}

