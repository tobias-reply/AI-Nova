#!/usr/bin/env python3
"""
CLI interface for the Documentation Agent
"""

import asyncio
import argparse
import sys
from pathlib import Path
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from agent import DocumentationAgent

def main():
    parser = argparse.ArgumentParser(description="Claude Code SDK Documentation Agent")
    parser.add_argument("--files", nargs="+", 
                       help="Specific files to review")
    parser.add_argument("--general-review", action="store_true",
                       help="Run general documentation review")
    parser.add_argument("--interactive", action="store_true",
                       help="Start interactive documentation session")
    parser.add_argument("--max-turns", type=int, default=5,
                       help="Maximum conversation turns (default: 5)")
    parser.add_argument("--model", default=None,
                       help="Claude model to use (auto-detects best model if not specified)")
    parser.add_argument("--system-prompt", default="system_prompt.txt",
                       help="Path to system prompt file")
    parser.add_argument("--project-root", default=".",
                       help="Project root directory (default: current directory)")
    
    args = parser.parse_args()
    
    # Validate that at least one mode is selected
    if not any([args.general_review, args.interactive, args.files]):
        print("Error: You must specify one of --general-review, --interactive, or --files")
        parser.print_help()
        sys.exit(1)
    
    # Initialize agent
    agent = DocumentationAgent(
        max_turns=args.max_turns, 
        model=args.model,
        system_prompt_file=args.system_prompt
    )
    
    try:
        if args.interactive:
            # Interactive mode
            asyncio.run(agent.interactive_session(args.project_root))
        
        elif args.files:
            # Process specific files
            result = asyncio.run(agent.process_files(args.files, args.project_root))
            print(f"\nResult: {result['status']}")
            if result.get('cost'):
                print(f"Cost: ${result['cost']:.4f}")
        
        elif args.general_review:
            # General documentation review
            result = asyncio.run(agent.general_review(args.project_root))
            print(f"\nResult: {result['status']}")
            if result.get('cost'):
                print(f"Cost: ${result['cost']:.4f}")
        
    except KeyboardInterrupt:
        print("\n👋 Documentation agent interrupted.")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()