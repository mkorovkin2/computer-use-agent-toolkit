/**
 * Workflow engine for custom tools and conditional logic.
 */

import { ToolDefinition, AgentContext } from "./types";
import { createCustomToolSchema } from "./tools";

export class WorkflowEngine {
  customTools: Map<string, ToolDefinition> = new Map();
  conditionalHandlers: Map<string, Array<{ condition: Function; handler: Function }>> = new Map();

  registerTool(name: string, description: string, func: Function): void {
    const inputSchema = {
      type: "object",
      properties: {},
    };

    this.customTools.set(name, {
      name,
      description,
      inputSchema,
      function: func,
    });
  }

  registerConditionalHandler(
    actionType: string,
    condition: (ctx: AgentContext, action: any) => boolean,
    handler: (ctx: AgentContext, action: any) => void
  ): void {
    if (!this.conditionalHandlers.has(actionType)) {
      this.conditionalHandlers.set(actionType, []);
    }
    this.conditionalHandlers.get(actionType)!.push({ condition, handler });
  }

  executeTool(toolName: string, args: Record<string, any>): any {
    const tool = this.customTools.get(toolName);
    if (!tool) {
      throw new Error(`Tool '${toolName}' not found`);
    }
    return tool.function(args);
  }

  checkConditionalHandlers(context: AgentContext, actionType: string, action: any): void {
    const handlers = this.conditionalHandlers.get(actionType);
    if (!handlers) return;

    for (const { condition, handler } of handlers) {
      try {
        if (condition(context, action)) {
          handler(context, action);
        }
      } catch (error) {
        console.error("Error in conditional handler:", error);
      }
    }
  }

  getToolSchemas(): Array<Record<string, any>> {
    return Array.from(this.customTools.values()).map((tool) => ({
      name: tool.name,
      description: tool.description,
      input_schema: tool.inputSchema,
    }));
  }

  hasTool(toolName: string): boolean {
    return this.customTools.has(toolName);
  }
}

