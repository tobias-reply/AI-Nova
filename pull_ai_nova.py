#!/usr/bin/env python3
import subprocess
import os
import sys
import argparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def pull_ai_nova():
    """Pull latest changes from main branch and prepare documentation branch if needed"""
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
        
        # Track changed files and create documentation branch if there were updates
        changed_files = []
        doc_branch_info = None
        
        if current_head != new_head:
            print("Changes detected, tracking modified files...")
            # Get list of changed files between old and new HEAD
            git_diff = subprocess.run(['git', 'diff', '--name-only', current_head, new_head], 
                                    capture_output=True, text=True, check=True)
            # Convert relative paths to absolute paths
            changed_files = [os.path.abspath(f.strip()) for f in git_diff.stdout.splitlines() if f.strip()]
            
            print(f"Found {len(changed_files)} changed files:")
            for file in changed_files:
                print(f"  - {file}")
            
            # Create documentation branch
            commit_short = new_head[:8]
            doc_branch = f"documentation-{commit_short}"
            
            print(f"Creating documentation branch: {doc_branch}")
            subprocess.run(['git', 'checkout', '-b', doc_branch], check=True)
            
            # Save changed files list (absolute paths)
            with open('.claude_changed_files.txt', 'w') as f:
                f.write('\n'.join(changed_files))
            
            doc_branch_info = {
                'branch_name': doc_branch,
                'commit_id': new_head,
                'commit_short': commit_short,
                'changed_files_count': len(changed_files)
            }
            
            print(f"✅ Ready for documentation improvements on branch: {doc_branch}")
        else:
            print("No changes detected.")
        
        print("Successfully pulled latest changes from AI-Nova main branch!")
        return changed_files, doc_branch_info
        
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

def run_claude_workflow(prompt_file="prompt.txt", changed_files=None, doc_branch_info=None, use_sdk=True):
    """Run Claude documentation workflow using Claude Code SDK or legacy tools"""
    if use_sdk:
        return run_claude_sdk_workflow(changed_files, doc_branch_info)
    else:
        return run_legacy_claude_workflow(prompt_file, changed_files, doc_branch_info)

def commit_documentation_changes(doc_branch_info, changed_files):
    """Commit documentation changes and create pull request"""
    if not doc_branch_info:
        print("No documentation branch to commit to.")
        return
    
    try:
        print("\n📝 Committing documentation changes...")
        
        # Check if there are any changes to commit
        result = subprocess.run(['git', 'diff', '--cached'], capture_output=True, text=True)
        staged_changes = result.stdout.strip()
        
        result = subprocess.run(['git', 'diff'], capture_output=True, text=True)
        unstaged_changes = result.stdout.strip()
        
        if not staged_changes and not unstaged_changes:
            print("No documentation changes to commit.")
            return
        
        # Stage all changes
        subprocess.run(['git', 'add', '.'], check=True)
        
        # Create commit message
        commit_message = f"""Improve documentation for {doc_branch_info['changed_files_count']} changed files

Documentation improvements for commit {doc_branch_info['commit_short']}:
{chr(10).join([f'- {file}' for file in changed_files])}

Changes include:
- Added missing docstrings following standard conventions
- Added type hints where missing
- Added inline comments for complex logic
- Created #TODO comments for potential improvements

🤖 Generated with Claude Code Documentation Agent

Co-authored-by: Claude <noreply@anthropic.com>"""
        
        # Commit changes
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        print("✅ Documentation changes committed")
        
        # Push the branch
        print(f"📤 Pushing branch: {doc_branch_info['branch_name']}")
        subprocess.run(['git', 'push', '-u', 'origin', doc_branch_info['branch_name']], check=True)
        print("✅ Branch pushed to remote")
        
        # Create pull request using GitHub CLI
        create_documentation_pr(doc_branch_info, changed_files)
        
    except subprocess.CalledProcessError as e:
        print(f"Error committing documentation changes: {e}")
    except Exception as e:
        print(f"Unexpected error during commit: {e}")

def create_documentation_pr(doc_branch_info, changed_files):
    """Create pull request for documentation changes"""
    try:
        print("🔄 Creating pull request...")
        
        # Check if gh CLI is available
        result = subprocess.run(['gh', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ GitHub CLI (gh) not found. Please install it to create pull requests automatically.")
            print(f"You can manually create a PR for branch: {doc_branch_info['branch_name']}")
            return
        
        pr_title = f"📝 Documentation improvements for {doc_branch_info['commit_short']}"
        
        pr_body = f"""## 📝 Documentation Improvements

This PR adds comprehensive documentation for {doc_branch_info['changed_files_count']} files that were changed in commit `{doc_branch_info['commit_short']}`.

### 📁 Files Updated:
{chr(10).join([f'- `{file}`' for file in changed_files])}

### ✨ Improvements Made:
- ✅ **Added missing docstrings** following Python/JavaScript/TypeScript conventions
- ✅ **Added type hints** where missing  
- ✅ **Added inline comments** for complex or non-obvious code
- ✅ **Created #TODO comments** for potential code improvements
- ✅ **No functional code changes** - documentation only

### 🤖 Generated by Claude Code Documentation Agent

This PR was automatically generated by the Claude Code SDK Documentation Agent, which focuses exclusively on improving code documentation while preserving all functional logic.

### 🔍 Review Checklist:
- [ ] Documentation follows project conventions
- [ ] Type hints are accurate
- [ ] Comments are helpful and clear
- [ ] No functional code was modified
- [ ] TODO comments are reasonable"""
        
        # Create the PR
        subprocess.run([
            'gh', 'pr', 'create',
            '--title', pr_title,
            '--body', pr_body,
            '--base', 'main',
            '--head', doc_branch_info['branch_name']
        ], check=True)
        
        print("✅ Pull request created successfully!")
        
        # Get PR URL
        result = subprocess.run([
            'gh', 'pr', 'view', 
            '--json', 'url',
            '--jq', '.url'
        ], capture_output=True, text=True, check=True)
        
        pr_url = result.stdout.strip()
        print(f"🔗 PR URL: {pr_url}")
        
    except subprocess.CalledProcessError as e:
        print(f"Error creating pull request: {e}")
        print(f"You can manually create a PR for branch: {doc_branch_info['branch_name']}")
    except Exception as e:
        print(f"Unexpected error creating PR: {e}")

def run_claude_sdk_workflow(changed_files=None, doc_branch_info=None):
    """Run Claude Code SDK documentation agent"""
    try:
        import subprocess
        import sys
        
        # Build command for CLI integration
        cmd = [sys.executable, "-m", "claude_code_tools.cli_integration"]
        
        if changed_files:
            # Write changed files for the agent to process
            with open('.claude_changed_files.txt', 'w') as f:
                f.write('\n'.join(changed_files))
            cmd.append("--changed-files")
            print(f"\n🤖 Starting Claude Code SDK agent for {len(changed_files)} changed files...")
        else:
            cmd.append("--general-review")
            print("\n🤖 Starting Claude Code SDK agent for general documentation review...")
        
        print("=" * 50)
        
        # Run the agent
        result = subprocess.run(cmd, cwd=".", check=False)
        
        if result.returncode == 0:
            print("=" * 50)
            print("✅ Claude Code SDK agent completed successfully!")
            
            # Commit changes and create PR if we're on a documentation branch
            if doc_branch_info:
                commit_documentation_changes(doc_branch_info, changed_files)
        else:
            print("=" * 50)
            print(f"⚠️ Claude Code SDK agent finished with exit code: {result.returncode}")
        
    except ImportError:
        print("Error: claude_code_tools not found. Using legacy workflow...")
        return run_legacy_claude_workflow("prompt.txt", changed_files, doc_branch_info)
    except Exception as e:
        print(f"Error running Claude Code SDK workflow: {e}")
        print("Falling back to legacy workflow...")
        return run_legacy_claude_workflow("prompt.txt", changed_files, doc_branch_info)

def run_legacy_claude_workflow(prompt_file="prompt.txt", changed_files=None, doc_branch_info=None):
    """Legacy Claude workflow using custom text editor tools"""
    try:
        from claude_tools import ClaudeClient
        
        # Load changed files list if not provided
        if changed_files is None:
            if os.path.exists('.claude_changed_files.txt'):
                with open('.claude_changed_files.txt', 'r') as f:
                    changed_files = [line.strip() for line in f if line.strip()]
            else:
                changed_files = []
        
        # Ensure all paths are absolute
        changed_files = [os.path.abspath(f) if not os.path.isabs(f) else f for f in changed_files]
        
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
            print(f"\nStarting legacy Claude workflow for {len(changed_files)} changed files...")
        else:
            prompt = prompt_template.replace("{changed_files}", "No changed files detected.")
            print("\nNo changed files found. Running general documentation review...")
        
        print("=" * 50)
        
        # Initialize Claude client
        client = ClaudeClient()
        
        # Run the conversation
        result = client.chat_with_tools(prompt)
        
        print("=" * 50)
        print("Legacy Claude documentation workflow completed!")
        print(f"Full conversation saved to: claude_conversation.log")
        
        # Commit changes and create PR if we're on a documentation branch
        if doc_branch_info:
            commit_documentation_changes(doc_branch_info, changed_files)
        
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
        print(f"Error running legacy Claude workflow: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Pull AI-Nova changes and optionally run Claude documentation workflow")
    parser.add_argument("--claude", action="store_true", help="Run Claude documentation workflow after pulling")
    parser.add_argument("--prompt", default="prompt.txt", help="Path to prompt file (default: prompt.txt)")
    parser.add_argument("--claude-only", action="store_true", help="Run only Claude workflow, skip git pull")
    parser.add_argument("--legacy", action="store_true", help="Use legacy Claude workflow instead of Claude Code SDK")
    parser.add_argument("--interactive", action="store_true", help="Start interactive Claude Code SDK session")
    
    args = parser.parse_args()
    
    changed_files = []
    doc_branch_info = None
    
    if not args.claude_only:
        changed_files, doc_branch_info = pull_ai_nova()
    
    if args.interactive:
        # Interactive mode with Claude Code SDK
        try:
            import subprocess
            import sys
            cmd = [sys.executable, "-m", "claude_code_tools.cli_integration", "--interactive"]
            subprocess.run(cmd, cwd=".", check=True)
        except Exception as e:
            print(f"Error running interactive mode: {e}")
    elif args.claude or args.claude_only:
        use_sdk = not args.legacy
        run_claude_workflow(args.prompt, changed_files, doc_branch_info, use_sdk)

if __name__ == "__main__":
    main()