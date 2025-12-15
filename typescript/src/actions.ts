/**
 * Action executor module for performing mouse and keyboard actions.
 */

import robot from "robotjs";
import { ActionResult, ActionType, MouseButton, ScrollDirection, ScreenRegion } from "./types";

export class ActionExecutor {
  private allowedRegion?: ScreenRegion;
  private safetyDelay: number;
  private confirmationMode: string;
  private rateLimitDelay: number;
  private lastActionTime: number = 0;

  constructor(
    allowedRegion?: ScreenRegion,
    safetyDelay: number = 0.1,
    confirmationMode: string = "auto",
    rateLimitDelay: number = 0.05
  ) {
    this.allowedRegion = allowedRegion;
    this.safetyDelay = safetyDelay;
    this.confirmationMode = confirmationMode;
    this.rateLimitDelay = rateLimitDelay;
  }

  private checkAllowed(x: number, y: number): boolean {
    if (!this.allowedRegion) {
      return true;
    }

    return (
      this.allowedRegion.x <= x &&
      x <= this.allowedRegion.x + this.allowedRegion.width &&
      this.allowedRegion.y <= y &&
      y <= this.allowedRegion.y + this.allowedRegion.height
    );
  }

  private async rateLimit(): Promise<void> {
    const elapsed = Date.now() - this.lastActionTime;
    if (elapsed < this.rateLimitDelay * 1000) {
      await new Promise((resolve) => setTimeout(resolve, this.rateLimitDelay * 1000 - elapsed));
    }
    this.lastActionTime = Date.now();
  }

  private async executeWithSafety(
    actionFunc: () => any,
    actionType: ActionType
  ): Promise<ActionResult> {
    if (this.confirmationMode === "dry-run") {
      return {
        success: true,
        actionType,
        data: { dryRun: true },
      };
    }

    await this.rateLimit();

    try {
      const result = actionFunc();
      await new Promise((resolve) => setTimeout(resolve, this.safetyDelay * 1000));
      return {
        success: true,
        actionType,
        data: result,
      };
    } catch (error) {
      return {
        success: false,
        actionType,
        error: String(error),
      };
    }
  }

  async mouseMove(x: number, y: number, duration: number = 0.5): Promise<ActionResult> {
    if (!this.checkAllowed(x, y)) {
      return {
        success: false,
        actionType: ActionType.MOUSE_MOVE,
        error: `Coordinates (${x}, ${y}) outside allowed region`,
      };
    }

    return this.executeWithSafety(() => {
      robot.moveMouse(x, y);
      return { x, y };
    }, ActionType.MOUSE_MOVE);
  }

  async click(
    x: number,
    y: number,
    button: MouseButton = MouseButton.LEFT,
    clicks: number = 1
  ): Promise<ActionResult> {
    if (!this.checkAllowed(x, y)) {
      return {
        success: false,
        actionType: ActionType.CLICK,
        error: `Coordinates (${x}, ${y}) outside allowed region`,
      };
    }

    return this.executeWithSafety(() => {
      robot.moveMouse(x, y);
      for (let i = 0; i < clicks; i++) {
        robot.mouseClick(button);
      }
      return { x, y, button, clicks };
    }, ActionType.CLICK);
  }

  async doubleClick(x: number, y: number): Promise<ActionResult> {
    return this.click(x, y, MouseButton.LEFT, 2);
  }

  async typeText(text: string, interval: number = 0.0): Promise<ActionResult> {
    return this.executeWithSafety(() => {
      robot.typeString(text);
      return { text, length: text.length };
    }, ActionType.TYPE);
  }

  async pressKey(key: string): Promise<ActionResult> {
    return this.executeWithSafety(() => {
      robot.keyTap(key);
      return { key };
    }, ActionType.KEY);
  }

  async scroll(
    direction: ScrollDirection,
    amount: number = 3,
    x?: number,
    y?: number
  ): Promise<ActionResult> {
    if (x !== undefined && y !== undefined && !this.checkAllowed(x, y)) {
      return {
        success: false,
        actionType: ActionType.SCROLL,
        error: `Coordinates (${x}, ${y}) outside allowed region`,
      };
    }

    return this.executeWithSafety(() => {
      if (x !== undefined && y !== undefined) {
        robot.moveMouse(x, y);
      }

      const scrollAmount = direction === ScrollDirection.UP || direction === ScrollDirection.LEFT
        ? -amount
        : amount;

      robot.scrollMouse(0, scrollAmount);
      return { direction, amount };
    }, ActionType.SCROLL);
  }

  getMousePosition(): { x: number; y: number } {
    const pos = robot.getMousePos();
    return { x: pos.x, y: pos.y };
  }

  getScreenSize(): { width: number; height: number } {
    const size = robot.getScreenSize();
    return { width: size.width, height: size.height };
  }
}

