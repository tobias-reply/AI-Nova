#!/usr/bin/env python3
"""
Vocabulary Test Analyzer using Claude on AWS Bedrock
Analyzes vocabulary test images and provides scoring with explanations
"""

import base64
import json
import os
import boto3
from pathlib import Path


def encode_image(image_path: str) -> str:
    """
    Encode an image to base64 string

    Args:
        image_path: Path to the image file

    Returns:
        Base64 encoded string of the image
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def analyze_vocab_test(image_paths: list[str], prompt: str) -> dict:
    """
    Analyze vocabulary test images using Claude on AWS Bedrock

    Args:
        image_paths: List of paths to the vocabulary test images
        prompt: Analysis prompt to send to Claude

    Returns:
        Dictionary containing the analysis results
    """
    print(f"Analyzing {len(image_paths)} image(s)...")

    try:
        # Initialize AWS Bedrock client
        bedrock = boto3.client(
            service_name="bedrock-runtime",
            region_name=os.environ.get("AWS_REGION", "eu-central-1")
        )

        # Prepare the content with images
        content = []

        # Add all images to the content
        for image_path in image_paths:
            if not os.path.exists(image_path):
                print(f"⚠️  Image not found: {image_path}")
                continue

            print(f"Loading image: {image_path}")
            image_base64 = encode_image(image_path)

            content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": image_base64
                }
            })

        # Add the text prompt
        content.append({
            "type": "text",
            "text": prompt
        })

        # Prepare the request body
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4096,
            "messages": [
                {
                    "role": "user",
                    "content": content
                }
            ],
            "temperature": 0.5
        }

        print("Sending request to Claude on AWS Bedrock...")

        # Call Claude via AWS Bedrock
        response = bedrock.invoke_model(
            modelId="eu.anthropic.claude-3-7-sonnet-20250219-v1:0",
            body=json.dumps(request_body)
        )

        # Parse the response
        response_body = json.loads(response["body"].read())
        analysis = response_body["content"][0]["text"]

        print("✓ Analysis completed")

        return {
            "success": True,
            "analysis": analysis,
            "usage": response_body.get("usage", {})
        }

    except Exception as e:
        print(f"✗ Error during analysis: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


def main():
    """Main function to analyze vocabulary test images"""

    # ============================================================
    # CONFIGURATION
    # ============================================================
    prompt = "Please analyze this vocubalry test. Keep in mind this is from a german school written by non native speakers of the 11th grade (age ~16). Provide reasoning for the grading of each question, your pointing score and overall achievable points. Also leave a mark in the german grading system (1-6, with 1 being the best and 6 the worst, while is the last passing grade)."

    # Set up paths
    script_dir = Path(__file__).parent
    vocab_test_dir = script_dir / "vocab_test"

    # Get the two JPEG images from vocab_test directory
    image_paths = [
        vocab_test_dir / "WhatsApp Image 2025-10-15 at 22.13.46.jpeg",
        vocab_test_dir / "WhatsApp Image 2025-10-15 at 22.13.47.jpeg"
    ]
    # ============================================================

    print("📚 Vocabulary Test Analyzer")
    print("=" * 60)
    print(f"Analyzing images from: {vocab_test_dir}")
    print()

    # Convert to strings
    image_paths_str = [str(path) for path in image_paths]

    # Analyze the vocabulary test
    result = analyze_vocab_test(
        image_paths=image_paths_str,
        prompt=prompt
    )

    if result.get("success"):
        print()
        print("=" * 60)
        print("ANALYSIS RESULTS")
        print("=" * 60)
        print()
        print(result["analysis"])
        print()
        print("=" * 60)

        # Print token usage if available
        usage = result.get("usage", {})
        if usage:
            print(f"\nToken usage:")
            print(f"  Input tokens: {usage.get('input_tokens', 'N/A')}")
            print(f"  Output tokens: {usage.get('output_tokens', 'N/A')}")
    else:
        print(f"\n❌ Failed to analyze vocabulary test: {result.get('error')}")
        print("\nMake sure you have:")
        print("  1. AWS credentials configured (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)")
        print("  2. Access to AWS Bedrock with Claude models enabled")
        print("  3. Correct AWS region set (default: eu-central-1)")


if __name__ == "__main__":
    main()
