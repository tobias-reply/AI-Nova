#!/usr/bin/env python3
import subprocess
import os
import sys
import argparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def pull_ai_nova():
    """Pull latest changes from main branch of AI-Nova repository"""
    repo_path = "/Users/t.kapp/Projects/Reply/claude/AI-Nova"
    
    if not os.path.exists(repo_path):
        print(f"Error: Repository path {repo_path} does not exist")
        sys.exit(1)
    
    try:
        # Change to repository directory
        os.chdir(repo_path)
        
        # Check if it's a git repository
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: {repo_path} is not a git repository")
            sys.exit(1)
        
        # Get current HEAD to compare changes
        current_head = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True, check=True)
        current_head = current_head.stdout.strip()
        
        # Fetch latest changes
        print("Fetching latest changes...")
        subprocess.run(['git', 'fetch', 'origin'], check=True)
        
        # Switch to main branch
        print("Switching to main branch...")
        subprocess.run(['git', 'checkout', 'main'], check=True)
        
        # Pull latest changes
        print("Pulling latest changes from main...")
        result = subprocess.run(['git', 'pull', 'origin', 'main'], check=True)
        
        # Get new HEAD after pull
        new_head = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True, check=True)
        new_head = new_head.stdout.strip()
        
        # Track changed files if there were updates
        changed_files = []
        if current_head != new_head:
            print("Changes detected, tracking modified files...")
            # Get list of changed files between old and new HEAD
            git_diff = subprocess.run(['git', 'diff', '--name-only', current_head, new_head], 
                                    capture_output=True, text=True, check=True)
            changed_files = [f.strip() for f in git_diff.stdout.splitlines() if f.strip()]
            
            # Save changed files list
            with open('.claude_changed_files.txt', 'w') as f:
                f.write('\n'.join(changed_files))
            
            print(f"Found {len(changed_files)} changed files:")
            for file in changed_files:
                print(f"  - {file}")
        else:
            print("No changes detected.")
        
        print("Successfully pulled latest changes from AI-Nova main branch!")
        return changed_files
        
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

def run_claude_workflow(prompt_file="prompt.txt", changed_files=None):
    """Run Claude with text editor tools after pulling changes"""
    try:
        from claude_tools import ClaudeClient
        
        # Load changed files list if not provided
        if changed_files is None:
            if os.path.exists('.claude_changed_files.txt'):
                with open('.claude_changed_files.txt', 'r') as f:
                    changed_files = [line.strip() for line in f if line.strip()]
            else:
                changed_files = []
        
        # Load prompt from file
        if os.path.exists(prompt_file):
            with open(prompt_file, 'r') as f:
                prompt_template = f.read().strip()
        else:
            prompt_template = "Please review the following files for documentation improvements: {changed_files}"
        
        # Format prompt with changed files
        if changed_files:
            changed_files_text = "\n".join([f"- {file}" for file in changed_files])
            prompt = prompt_template.format(changed_files=changed_files_text)
            print(f"\nStarting Claude documentation workflow for {len(changed_files)} changed files...")
        else:
            prompt = prompt_template.replace("{changed_files}", "No changed files detected.")
            print("\nNo changed files found. Running general documentation review...")
        
        print("=" * 50)
        
        # Initialize Claude client
        client = ClaudeClient()
        
        # Run the conversation
        result = client.chat_with_tools(prompt)
        
        print("=" * 50)
        print("Claude documentation workflow completed!")
        print(f"Full conversation saved to: claude_conversation.log")
        
        # Clean up changed files list
        if os.path.exists('.claude_changed_files.txt'):
            os.remove('.claude_changed_files.txt')
        
    except ImportError:
        print("Error: claude_tools package not found. Please install required dependencies.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        print("Please set your ANTHROPIC_API_KEY environment variable.")
        sys.exit(1)
    except Exception as e:
        print(f"Error running Claude workflow: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Pull AI-Nova changes and optionally run Claude documentation workflow")
    parser.add_argument("--claude", action="store_true", help="Run Claude documentation workflow after pulling")
    parser.add_argument("--prompt", default="prompt.txt", help="Path to prompt file (default: prompt.txt)")
    parser.add_argument("--claude-only", action="store_true", help="Run only Claude workflow, skip git pull")
    
    args = parser.parse_args()
    
    changed_files = []
    if not args.claude_only:
        changed_files = pull_ai_nova()
    
    if args.claude or args.claude_only:
        run_claude_workflow(args.prompt, changed_files)

if __name__ == "__main__":
    main()