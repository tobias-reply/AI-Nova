#!/usr/bin/env python3
"""
Configuration utilities for the Documentation Agent
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_bedrock_config() -> Dict[str, Any]:
    """Get recommended Bedrock configuration"""
    return {
        'CLAUDE_CODE_USE_BEDROCK': '1',
        'AWS_REGION': 'us-east-1',  # Change to your preferred region
        'AWS_PROFILE': 'default',   # Change to your AWS profile
        'DISABLE_PROMPT_CACHING': '1',
        'CLAUDE_CODE_MAX_OUTPUT_TOKENS': '4096',
        'MAX_THINKING_TOKENS': '0',  # Disable thinking for compatibility
    }

def get_anthropic_api_config() -> Dict[str, Any]:
    """Get configuration for direct Anthropic API"""
    return {
        'ANTHROPIC_API_KEY': 'your-api-key-here',
        'CLAUDE_CODE_USE_BEDROCK': '0',
    }

def print_env_setup():
    """Print environment setup instructions"""
    print("Environment Setup Options:")
    print()
    print("Option 1: Amazon Bedrock (Recommended)")
    print("=" * 40)
    bedrock_config = get_bedrock_config()
    for key, value in bedrock_config.items():
        print(f"export {key}={value}")
    print()
    print("Requirements:")
    print("- AWS account with Bedrock access")
    print("- Claude models enabled in Bedrock console")
    print("- AWS credentials configured (aws configure)")
    print()
    
    print("Option 2: Direct Anthropic API")
    print("=" * 30)
    api_config = get_anthropic_api_config()
    for key, value in api_config.items():
        print(f"export {key}={value}")
    print()
    print("Requirements:")
    print("- Anthropic API key from console.anthropic.com")
    print("- API credits for usage")

def validate_config():
    """Validate current configuration"""
    use_bedrock = os.getenv('CLAUDE_CODE_USE_BEDROCK', '').lower() in ['1', 'true', 'yes']
    
    if use_bedrock:
        print("✅ Bedrock mode enabled")
        
        # Check required Bedrock environment variables
        required_vars = ['AWS_REGION']
        missing_vars = []
        
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            print(f"❌ Missing required environment variables: {missing_vars}")
            return False
        
        # Check AWS profile or credentials
        aws_profile = os.getenv('AWS_PROFILE')
        aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
        
        if not aws_profile and not aws_access_key:
            print("⚠️  No AWS_PROFILE or AWS_ACCESS_KEY_ID found")
            print("   Run 'aws configure' or set AWS environment variables")
        
        return True
    
    else:
        print("✅ Direct API mode enabled")
        
        # Check Anthropic API key
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            print("❌ Missing ANTHROPIC_API_KEY")
            return False
        
        return True

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Documentation Agent Configuration")
    parser.add_argument("--validate", action="store_true", help="Validate current configuration")
    parser.add_argument("--setup", action="store_true", help="Print setup instructions")
    
    args = parser.parse_args()
    
    if args.validate:
        validate_config()
    elif args.setup:
        print_env_setup()
    else:
        parser.print_help()