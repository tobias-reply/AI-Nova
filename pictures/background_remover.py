#!/usr/bin/env python3
"""
Background Removal using Amazon Bedrock Nova Canvas
Simple background removal for professional photos
"""

import base64
import json
import os
import boto3
from pathlib import Path
from botocore.config import Config

class BackgroundRemover:
    def __init__(self, region_name: str = "us-east-1"):
        """Initialize Bedrock client"""
        self.client = boto3.client(
            "bedrock-runtime", 
            region_name=region_name,
            config=Config(read_timeout=300)
        )
        self.model_id = "amazon.nova-canvas-v1:0"
        
    def encode_image_to_base64(self, image_path: str) -> str:
        """Convert image file to base64 string"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def remove_background(self, image_path: str, output_path: str):
        """Remove background from image"""
        
        print(f"Removing background from: {os.path.basename(image_path)}")
        
        # Encode the input image
        base64_image = self.encode_image_to_base64(image_path)
        
        # Create background removal request
        body = json.dumps({
            "taskType": "BACKGROUND_REMOVAL",
            "backgroundRemovalParams": {
                "image": base64_image,
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
            
            # Extract and save the image with background removed
            base64_image_data = response_body.get("images")[0]
            image_bytes = base64.b64decode(base64_image_data.encode('ascii'))
            
            with open(output_path, "wb") as file:
                file.write(image_bytes)
            
            print(f"✓ Background removed, saved: {os.path.basename(output_path)}")
            return {"success": True, "output_path": output_path}
            
        except Exception as e:
            print(f"✗ Error removing background: {str(e)}")
            return {"success": False, "error": str(e)}

def main():
    """Main function to remove backgrounds from reference images"""
    
    # Set up paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    reference_pics_dir = os.path.join(script_dir, "reference_pics")
    output_dir = os.path.join(script_dir, "no_background")
    
    print("🎯 Background Removal Tool")
    print("   Amazon Bedrock Nova Canvas")
    print("=" * 40)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Find JPG and PNG files
    input_path = Path(reference_pics_dir)
    image_files = (list(input_path.glob("*.JPG")) + 
                  list(input_path.glob("*.jpg")) + 
                  list(input_path.glob("*.PNG")) + 
                  list(input_path.glob("*.png")))
    
    if not image_files:
        print("No JPG or PNG images found in reference_pics directory")
        return
    
    # Initialize background remover
    remover = BackgroundRemover()
    
    # Process each image
    results = []
    for i, image_file in enumerate(image_files, 1):
        output_filename = f"no_background_{i:02d}.png"
        output_path = os.path.join(output_dir, output_filename)
        
        result = remover.remove_background(str(image_file), output_path)
        results.append(result)
    
    # Print summary
    print("\n📊 Processing Summary:")
    print("=" * 40)
    
    successful = [r for r in results if r.get("success")]
    failed = [r for r in results if not r.get("success")]
    
    print(f"✓ Successfully processed: {len(successful)} images")
    print(f"✗ Failed to process: {len(failed)} images")
    
    if successful:
        print(f"\n🎉 Images with removed backgrounds saved to: {output_dir}")

if __name__ == "__main__":
    main()