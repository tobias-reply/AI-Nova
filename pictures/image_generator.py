#!/usr/bin/env python3
"""
Image Generator using Amazon Bedrock Nova Canvas
Generate images from text prompts
"""

import base64
import json
import os
import random
import boto3
from pathlib import Path
from botocore.config import Config

class BedrockImageGenerator:
    def __init__(self, region_name: str = "us-east-1"):
        """Initialize Bedrock client"""
        self.client = boto3.client(
            "bedrock-runtime",
            region_name=region_name,
            config=Config(read_timeout=300)
        )
        self.model_id = "amazon.nova-canvas-v1:0"

    def generate_image(self, prompt: str, output_path: str,
                      negative_prompt: str = "bad quality, low res, blurry",
                      width: int = 1024, height: int = 1024,
                      cfg_scale: float = 7.0):
        """
        Generate an image from a text prompt

        Args:
            prompt: In the style of a business friendly cartoon, that is neither too colourful nor to boring: Create an elderly lady being interviewed in a nice looking living room with some plants and a lot of wood. She is wearing a nice blouse and has a warm smile, with a cane leaning on her chair. The interviewer is a young man in a medical suit holding a notepad. The lighting is warm and inviting, with soft shadows and a cozy atmosphere.
            output_path: Path where the generated image will be saved
            negative_prompt: Things to avoid in the generated image
            width: Image width (default 1024)
            height: Image height (default 1024)
            cfg_scale: How closely to follow the prompt (default 7.0)
        """

        print(f"Generating image from prompt: '{prompt[:60]}...'")

        # Generate random seed for reproducibility
        seed = random.randint(0, 858993460)

        # Create text-to-image request
        body = json.dumps({
            "taskType": "TEXT_IMAGE",
            "textToImageParams": {
                "text": prompt,
                "negativeText": negative_prompt
            },
            "imageGenerationConfig": {
                "numberOfImages": 1,
                "height": height,
                "width": width,
                "cfgScale": cfg_scale,
                "seed": seed
            }
        })

        try:
            # Invoke the model
            response = self.client.invoke_model(
                body=body,
                modelId=self.model_id,
                accept="application/json",
                contentType="application/json"
            )

            response_body = json.loads(response.get("body").read())

            # Check for errors
            if response_body.get("error"):
                raise Exception(f"Model error: {response_body.get('error')}")

            # Extract and save the generated image
            base64_image_data = response_body.get("images")[0]
            image_bytes = base64.b64decode(base64_image_data.encode('ascii'))

            with open(output_path, "wb") as file:
                file.write(image_bytes)

            print(f"✓ Image saved: {output_path}")
            print(f"  Seed: {seed} (use this to reproduce the same image)")
            return {"success": True, "output_path": output_path, "seed": seed}

        except Exception as e:
            print(f"✗ Error generating image: {str(e)}")
            return {"success": False, "error": str(e)}

def main():
    """Main function to generate an image"""

    # ============================================================
    # ADJUST YOUR PROMPT HERE:
    # ============================================================
    prompt = "In the style of a business friendly cartoon, with little facial features and minimalistic design, that is neither too colourful nor to boring: Create an elderly lady being interviewed in a nice looking living room with some plants and a lot of wood. She is wearing a nice blouse and has a warm smile, with a cane leaning on her chair. The interviewer is a young man in a medical suit holding a notepad. The lighting is warm and inviting, with soft shadows and a cozy atmosphere."
    # Optional: Things to avoid in the image
    negative_prompt = "bad quality, low resolution, blurry, distorted, ugly, very realistic"

    # Image dimensions (1024x1024 is recommended)
    width = 1024
    height = 1024

    # CFG Scale: How closely to follow the prompt (1.0-10.0, recommended: 6.0-8.0)
    cfg_scale = 7.0
    # ============================================================

    # Set up paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "generated_images")

    print("🎨 Amazon Bedrock Nova Canvas - Image Generator")
    print("=" * 60)

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Generate output filename with timestamp
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"generated_{timestamp}.png"
    output_path = os.path.join(output_dir, output_filename)

    # Initialize generator
    generator = BedrockImageGenerator()

    # Generate image
    result = generator.generate_image(
        prompt=prompt,
        output_path=output_path,
        negative_prompt=negative_prompt,
        width=width,
        height=height,
        cfg_scale=cfg_scale
    )

    if result.get("success"):
        print(f"\n🎉 Success! Image saved to: {output_path}")
    else:
        print(f"\n❌ Failed to generate image: {result.get('error')}")

if __name__ == "__main__":
    main()
