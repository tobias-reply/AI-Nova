#!/usr/bin/env python3
"""CLI integration for Claude Code SDK agent with pull_ai_nova.py script"""

import asyncio
import os
import sys
import argparse
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from .documentation_agent import DocumentationAgent

class CLIIntegration:
    """Integration between pull_ai_nova.py and Claude Code SDK agent"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.changed_files_file = self.project_root / ".claude_changed_files.txt"
        
    def read_changed_files(self) -> List[str]:
        """Read the list of changed files from .claude_changed_files.txt"""
        if not self.changed_files_file.exists():
            return []
        
        try:
            with open(self.changed_files_file, 'r') as f:
                files = [line.strip() for line in f if line.strip()]
            return files
        except Exception as e:
            print(f"Error reading changed files: {e}")
            return []
    
    def cleanup_changed_files(self) -> None:
        """Clean up the changed files tracking file"""
        try:
            if self.changed_files_file.exists():
                self.changed_files_file.unlink()
        except Exception as e:
            print(f"Warning: Could not clean up changed files file: {e}")

async def main():
    parser = argparse.ArgumentParser(description="Claude Code SDK Documentation Agent")
    parser.add_argument("--changed-files", action="store_true", 
                       help="Process files from .claude_changed_files.txt")
    parser.add_argument("--general-review", action="store_true",
                       help="Run general documentation review")
    parser.add_argument("--interactive", action="store_true",
                       help="Start interactive documentation session")
    parser.add_argument("--files", nargs="+", 
                       help="Specific files to review")
    parser.add_argument("--max-turns", type=int, default=5,
                       help="Maximum conversation turns (default: 5)")
    parser.add_argument("--model", default=None,
                       help="Claude model to use (auto-detects best model if not specified)")
    parser.add_argument("--project-root", default=".",
                       help="Project root directory (default: current directory)")
    
    args = parser.parse_args()
    
    # Validate that at least one mode is selected
    if not any([args.changed_files, args.general_review, args.interactive, args.files]):
        print("Error: You must specify one of --changed-files, --general-review, --interactive, or --files")
        parser.print_help()
        sys.exit(1)
    
    # Initialize CLI integration and agent
    cli = CLIIntegration(args.project_root)
    agent = DocumentationAgent(max_turns=args.max_turns, model=args.model)
    
    try:
        if args.interactive:
            # Interactive mode
            await agent.interactive_session(str(cli.project_root))
        
        elif args.changed_files:
            # Process changed files from pull_ai_nova.py
            changed_files = cli.read_changed_files()
            if not changed_files:
                print("No changed files found. Make sure to run 'python pull_ai_nova.py --claude' first.")
                sys.exit(1)
            
            print(f"Found {len(changed_files)} changed files:")
            for file in changed_files:
                print(f"  - {file}")
            
            result = await agent.process_changed_files(changed_files, str(cli.project_root))
            
            # Clean up after successful processing
            if result.get("status") == "success":
                cli.cleanup_changed_files()
        
        elif args.files:
            # Process specific files
            result = await agent.process_changed_files(args.files, str(cli.project_root))
        
        elif args.general_review:
            # General documentation review
            result = await agent.general_documentation_review(str(cli.project_root))
        
    except KeyboardInterrupt:
        print("\n👋 Documentation agent interrupted.")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())