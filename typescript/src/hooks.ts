/**
 * Hook system for workflow customization.
 */

import { AgentContext, HookFunction } from "./types";

export class HookRegistry {
  beforeScreenshot: HookFunction[] = [];
  afterScreenshot: HookFunction[] = [];
  beforeAction: HookFunction[] = [];
  afterAction: HookFunction[] = [];
  onToolCall: Map<string, HookFunction[]> = new Map();
  onIterationStart: HookFunction[] = [];
  onIterationEnd: HookFunction[] = [];

  registerBeforeScreenshot(func: HookFunction): void {
    this.beforeScreenshot.push(func);
  }

  registerAfterScreenshot(func: HookFunction): void {
    this.afterScreenshot.push(func);
  }

  registerBeforeAction(func: HookFunction): void {
    this.beforeAction.push(func);
  }

  registerAfterAction(func: HookFunction): void {
    this.afterAction.push(func);
  }

  registerOnToolCall(toolName: string | null, func: HookFunction): void {
    const key = toolName || "*";
    if (!this.onToolCall.has(key)) {
      this.onToolCall.set(key, []);
    }
    this.onToolCall.get(key)!.push(func);
  }

  registerOnIterationStart(func: HookFunction): void {
    this.onIterationStart.push(func);
  }

  registerOnIterationEnd(func: HookFunction): void {
    this.onIterationEnd.push(func);
  }

  triggerBeforeScreenshot(context: AgentContext): void {
    this.beforeScreenshot.forEach((hook) => hook(context));
  }

  triggerAfterScreenshot(context: AgentContext, image: any): void {
    this.afterScreenshot.forEach((hook) => hook(context, image));
  }

  triggerBeforeAction(context: AgentContext, action: any): any {
    let modifiedAction = action;
    this.beforeAction.forEach((hook) => {
      const result = hook(context, modifiedAction);
      if (result !== undefined) {
        modifiedAction = result;
      }
    });
    return modifiedAction;
  }

  triggerAfterAction(context: AgentContext, action: any, result: any): void {
    this.afterAction.forEach((hook) => hook(context, action, result));
  }

  triggerOnToolCall(context: AgentContext, toolName: string, args: Record<string, any>): any {
    let modifiedArgs = args;

    // Specific tool hooks
    if (this.onToolCall.has(toolName)) {
      this.onToolCall.get(toolName)!.forEach((hook) => {
        const result = hook(context, modifiedArgs);
        if (result !== undefined) {
          modifiedArgs = result;
        }
      });
    }

    // Wildcard hooks
    if (this.onToolCall.has("*")) {
      this.onToolCall.get("*")!.forEach((hook) => {
        const result = hook(context, toolName, modifiedArgs);
        if (result !== undefined) {
          modifiedArgs = result;
        }
      });
    }

    return modifiedArgs;
  }

  triggerOnIterationStart(context: AgentContext, iteration: number): void {
    this.onIterationStart.forEach((hook) => hook(context, iteration));
  }

  triggerOnIterationEnd(context: AgentContext, iteration: number): void {
    this.onIterationEnd.forEach((hook) => hook(context, iteration));
  }
}

