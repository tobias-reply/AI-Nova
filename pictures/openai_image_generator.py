#!/usr/bin/env python3
"""
Image Generator using OpenAI
Generate images from text prompts
"""

import base64
import os
from datetime import datetime
from openai import OpenAI

def generate_image(prompt: str, output_path: str, reference_image_path: str = None,
                   size: str = "1024x1024", quality: str = "high"):
    """
    Generate an image from a text prompt using OpenAI

    Args:
        prompt: Text description of the image to generate
        output_path: Path where the generated image will be saved
        reference_image_path: Optional path to reference image for style consistency
        size: Image dimensions (e.g., "1024x1024", "1024x1536", "1536x1024")
        quality: Rendering quality ("low", "medium", "high", or "auto")
    """
    print(f"Generating image from prompt: '{prompt[:60]}...'")
    print(f"Size: {size}, Quality: {quality}")

    if reference_image_path:
        print(f"Using reference image: {reference_image_path}")

    try:
        # Initialize OpenAI client (uses OPENAI_API_KEY env variable)
        client = OpenAI()

        # Prepare the prompt - add style reference instruction if reference image provided
        enhanced_prompt = prompt
        if reference_image_path and os.path.exists(reference_image_path):
            enhanced_prompt = f"Using the exact same art style, color palette, line work, and aesthetic as the reference, create: {prompt}"

        # Generate image using the responses API with configuration
        response = client.responses.create(
            model="gpt-4o",
            input=enhanced_prompt,
            tools=[{
                "type": "image_generation",
                "size": size,
                "quality": quality
            }],
        )

        # Extract the image data
        image_data = [
            output.result
            for output in response.output
            if output.type == "image_generation_call"
        ]

        if image_data:
            # Save the image
            image_base64 = image_data[0]
            with open(output_path, "wb") as f:
                f.write(base64.b64decode(image_base64))

            print(f"✓ Image saved: {output_path}")
            return {"success": True, "output_path": output_path}
        else:
            print("✗ No image data received from API")
            return {"success": False, "error": "No image data in response"}

    except Exception as e:
        print(f"✗ Error generating image: {str(e)}")
        return {"success": False, "error": str(e)}

def main():
    """Main function to generate an image"""

    # ============================================================
    # ADJUST YOUR PROMPT HERE:
    # ============================================================
    prompt = "In the style of a business friendly cartoon, with little facial features and minimalistic design, that is neither too colourful nor too boring: Show a man falling asleep on a typewriter, with headphones on and a huge stack of paperwork next to him on the desk. He is alone in kind of a therapist room with lots of wood and some plants. He is also bald. The lighting is warm and inviting, with soft shadows and a cozy atmosphere."

    # Optional: Set a reference image to match the style
    # Example: "generated_images/openai_generated_20251011_153436.png"
    reference_image = "generated_images/openai_generated_20251011_153436.png"
    # ============================================================

    # Set up paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "generated_images")

    # Handle reference image path
    reference_path = None
    if reference_image:
        reference_path = os.path.join(script_dir, reference_image)
        if not os.path.exists(reference_path):
            print(f"⚠️  Reference image not found: {reference_path}")
            print("Proceeding without reference image...")
            reference_path = None

    print("🎨 OpenAI Image Generator")
    print("=" * 60)

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Generate output filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"openai_generated_{timestamp}.png"
    output_path = os.path.join(output_dir, output_filename)

    # Generate image
    result = generate_image(
        prompt=prompt,
        output_path=output_path,
        reference_image_path=reference_path
    )

    if result.get("success"):
        print(f"\n🎉 Success! Image saved to: {output_path}")
    else:
        print(f"\n❌ Failed to generate image: {result.get('error')}")

if __name__ == "__main__":
    main()
