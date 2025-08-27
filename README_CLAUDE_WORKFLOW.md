# Claude Documentation Workflow Integration

This repository includes an integrated Claude documentation workflow that automatically improves documentation for changed files using Anthropic's Claude Code SDK and legacy text editor tools.

## Setup

1. **Install Python dependencies with uv:**
   ```bash
   uv sync
   ```

2. **Install Claude Code CLI (required for SDK):**
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```

3. **Choose your authentication method:**

   **Option A: Amazon Bedrock (Recommended)**
   ```bash
   # Configure for Bedrock (uses your AWS account)
   echo "CLAUDE_CODE_USE_BEDROCK=1" >> .env
   aws configure  # Set up AWS credentials
   ```
   📖 **See [BEDROCK_SETUP.md](BEDROCK_SETUP.md) for detailed Bedrock setup guide**

   **Option B: Direct Anthropic API**
   ```bash
   echo "ANTHROPIC_API_KEY=your_api_key_here" >> .env
   ```

## Usage

### Basic Git Pull (Original Functionality)
```bash
uv run python pull_ai_nova.py
```

### Pull + Run Claude Code SDK Agent
```bash
uv run python pull_ai_nova.py --claude
```

### Interactive Documentation Session
```bash
uv run python pull_ai_nova.py --interactive
```

### Run Documentation Agent Only (No Git Pull)
```bash
uv run python pull_ai_nova.py --claude-only
```

### Use Legacy Workflow (Custom Text Editor Tools)
```bash
uv run python pull_ai_nova.py --claude --legacy
```

### Direct Claude Code SDK Usage
```bash
# Process specific files
uv run python -m claude_code_tools.cli_integration --files file1.py file2.js

# General documentation review
uv run python -m claude_code_tools.cli_integration --general-review
```

## How It Works

1. **Change Tracking**: When pulling from main, the script tracks which files have changed
2. **Documentation Focus**: Claude is restricted to ONLY documentation tasks:
   - Adding/improving docstrings and comments
   - Adding type hints where missing  
   - Creating #TODO comments for code issues (without modifying functional code)
3. **Text Editor Tool**: Claude can view and edit files with precise string replacement
4. **Safety Features**: Automatic backups before edits and path validation

## Documentation Workflow

The workflow specifically focuses on documentation improvements:

1. **Pulls latest changes and identifies modified files**
2. **Claude reviews only the changed files for documentation**
3. **Adds missing docstrings following standard conventions**
4. **Adds inline comments for complex or non-obvious code**
5. **Adds type hints where missing**
6. **Creates #TODO comments for any code issues found**
7. **Never modifies functional code - only documentation**

## Customizing the Documentation Prompt

The default `prompt.txt` focuses on documentation tasks. You can customize it but should maintain the documentation-only restriction. The prompt automatically receives the list of changed files.

## File Structure

```
.
├── pull_ai_nova.py          # Main script
├── prompt.txt               # Default prompt file
├── claude_tools/            # Claude integration package
│   ├── __init__.py
│   ├── claude_client.py     # API client
│   └── text_editor.py       # Text editor tool implementation
├── requirements.txt         # Python dependencies
├── .claude_backups/         # Automatic backups (created when needed)
└── claude_conversation.log  # Conversation history (created after runs)
```

## Example Workflow

1. Pull latest changes and run Claude documentation workflow:
   ```bash
   uv run python pull_ai_nova.py --claude
   ```

2. The script will:
   - Pull from main and identify changed files (e.g., `src/utils.py`, `app/components/Button.tsx`)
   - Pass the changed files list to Claude
   - Claude examines only those files for documentation improvements
   - Adds missing docstrings, comments, and type hints
   - Creates #TODO comments for any code issues found
   - Logs everything to `claude_conversation.log`

3. Review the documentation changes and conversation log
4. Commit the improved documentation

## Troubleshooting

- **API Key Issues**: Make sure `ANTHROPIC_API_KEY` is set correctly
- **Import Errors**: Install dependencies with `pip install -r requirements.txt`
- **Permission Errors**: Ensure the script has read/write access to the repository
- **File Not Found**: Check that `prompt.txt` exists or specify a different prompt file

## Security Considerations

- The text editor tool operates with your file system permissions
- All file operations are restricted to the current directory and subdirectories
- Backups are automatically created before any modifications
- Review all changes before committing to version control