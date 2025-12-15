/**
 * Screen capture module for taking screenshots.
 */

import screenshot from "screenshot-desktop";
import sharp from "sharp";
import { ScreenRegion } from "./types";

export class ScreenCapture {
  private region?: ScreenRegion;
  private monitor: number;

  constructor(region?: ScreenRegion, monitor: number = 0) {
    this.region = region;
    this.monitor = monitor;
  }

  async capture(): Promise<Buffer> {
    const img = await screenshot({ screen: this.monitor });
    
    if (this.region) {
      // Crop to region
      return sharp(img)
        .extract({
          left: this.region.x,
          top: this.region.y,
          width: this.region.width,
          height: this.region.height,
        })
        .toBuffer();
    }
    
    return img;
  }

  async captureBase64(format: string = "PNG"): Promise<string> {
    const img = await this.capture();
    const buffer = await sharp(img).png().toBuffer();
    return buffer.toString("base64");
  }

  async captureWithMetadata(): Promise<{ image: Buffer; metadata: any }> {
    const image = await this.capture();
    const metadata = await sharp(image).metadata();
    
    return {
      image,
      metadata: {
        width: metadata.width,
        height: metadata.height,
        format: metadata.format,
        region: this.region,
        monitor: this.monitor,
      },
    };
  }

  async getScreenSize(): Promise<{ width: number; height: number }> {
    const img = await screenshot({ screen: this.monitor });
    const metadata = await sharp(img).metadata();
    return {
      width: metadata.width || 1920,
      height: metadata.height || 1080,
    };
  }
}

