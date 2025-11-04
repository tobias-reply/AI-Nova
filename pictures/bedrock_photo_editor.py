#!/usr/bin/env python3
"""
Professional Photo Editor using Amazon Bedrock Nova Canvas INPAINTING
Simple lighting fixes for professional business photos
"""

import base64
import json
import os
import random
import boto3
from pathlib import Path
from botocore.config import Config
import logging

class BedrockPhotoEditor:
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
    
    def process_image_inpainting(self, image_path: str, output_path: str):
        """Process single image using inpainting for professional lighting"""
        
        print(f"Processing: {os.path.basename(image_path)}")
        
        # Encode the input image
        base64_image = self.encode_image_to_base64(image_path)
        
        # Professional photo editing prompt
        edit_prompt = "You are a professional photo editor creating a professional headshot. Fix lighting for business photo quality with minimal face enhancement."
        
        # Generate random seed
        seed = random.randint(0, 858993460)
        
        # Create inpainting request
        body = json.dumps({
            "taskType": "INPAINTING",
            "inPaintingParams": {
                "text": edit_prompt,
                "negativeText": "bad quality, low res, harsh lighting",
                "image": base64_image,
                "maskPrompt": "lighting, shadows, face"
            },
            "imageGenerationConfig": {
                "numberOfImages": 1,
                "height": 1024,
                "width": 1024,
                "cfgScale": 6.0,
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
            
            # Extract and save the enhanced image
            base64_image_data = response_body.get("images")[0]
            image_bytes = base64.b64decode(base64_image_data.encode('ascii'))
            
            with open(output_path, "wb") as file:
                file.write(image_bytes)
            
            print(f"✓ Enhanced image saved: {os.path.basename(output_path)}")
            return {"success": True, "output_path": output_path, "seed": seed}
            
        except Exception as e:
            print(f"✗ Error processing image: {str(e)}")
            return {"success": False, "error": str(e)}

def main():
    """Main function to process reference images"""
    
    # Set up paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    reference_pics_dir = os.path.join(script_dir, "reference_pics")
    output_dir = os.path.join(script_dir, "professional_headshots")
    
    print("🎯 Professional Photo Editor - INPAINTING Mode")
    print("   Simple lighting fixes for business photos")
    print("=" * 50)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Find JPG files
    input_path = Path(reference_pics_dir)
    image_files = list(input_path.glob("*.JPG")) + list(input_path.glob("*.jpg"))
    
    if not image_files:
        print("No JPG images found in reference_pics directory")
        return
    
    # Initialize editor
    editor = BedrockPhotoEditor()
    
    # Process each image
    results = []
    for i, image_file in enumerate(image_files, 1):
        output_filename = f"enhanced_professional_{i:02d}.png"
        output_path = os.path.join(output_dir, output_filename)
        
        result = editor.process_image_inpainting(str(image_file), output_path)
        results.append(result)
    
    # Print summary
    print("\n📊 Processing Summary:")
    print("=" * 50)
    
    successful = [r for r in results if r.get("success")]
    failed = [r for r in results if not r.get("success")]
    
    print(f"✓ Successfully processed: {len(successful)} images")
    print(f"✗ Failed to process: {len(failed)} images")
    
    if successful:
        print(f"\n🎉 Enhanced photos saved to: {output_dir}")

if __name__ == "__main__":
    main()