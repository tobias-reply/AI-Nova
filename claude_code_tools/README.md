# Claude Code Tools - Documentation Agent

This folder contains Claude Code SDK-based tools for automated documentation improvement integrated with the AI-Nova project workflow.

## Overview

The Claude Code Tools provide a sophisticated documentation agent that uses the official Claude Code SDK to:
- Automatically improve documentation for changed files
- Add missing docstrings and type hints
- Add helpful inline comments
- Create TODO comments for code issues
- Run interactive documentation sessions

## Features

### 🤖 Documentation Agent
- **Smart file processing**: Focuses only on files that have changed
- **Documentation-only**: Never modifies functional code
- **Multiple modes**: Changed files, general review, interactive sessions
- **Advanced tools**: Uses Claude's built-in Read, Write, Edit, Glob, and Grep tools
- **Cost tracking**: Provides cost and duration metrics

### 🔧 Integration with pull_ai_nova.py
- **Seamless workflow**: Automatically processes files changed during git pull
- **Fallback support**: Falls back to legacy tools if SDK is unavailable
- **Multiple modes**: SDK mode (default) and legacy mode

## Installation

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Install Claude Code CLI (required for SDK):**
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```

3. **Set your API key in .env:**
   ```bash
   ANTHROPIC_API_KEY=your_api_key_here
   ```

## Usage

### Via pull_ai_nova.py (Recommended)

```bash
# Pull changes and run SDK agent
uv run python pull_ai_nova.py --claude

# Interactive documentation session
uv run python pull_ai_nova.py --interactive

# Use legacy workflow instead of SDK
uv run python pull_ai_nova.py --claude --legacy

# SDK agent only (no git pull)
uv run python pull_ai_nova.py --claude-only
```

### Direct CLI Usage

```bash
# Process changed files (from .claude_changed_files.txt)
uv run python -m claude_code_tools.cli_integration --changed-files

# General documentation review
uv run python -m claude_code_tools.cli_integration --general-review

# Interactive session
uv run python -m claude_code_tools.cli_integration --interactive

# Process specific files
uv run python -m claude_code_tools.cli_integration --files file1.py file2.js

# Custom model and settings
uv run python -m claude_code_tools.cli_integration --changed-files --model claude-3-opus-20240229 --max-turns 3
```

### Programmatic Usage

```python
import asyncio
from claude_code_tools import DocumentationAgent

async def main():
    agent = DocumentationAgent()
    
    # Process changed files
    changed_files = ["src/utils.py", "app/components/Button.tsx"]
    result = await agent.process_changed_files(changed_files)
    
    print(f"Cost: ${result['cost']:.4f}")
    print(f"Duration: {result['duration_ms']/1000:.1f}s")

asyncio.run(main())
```

## Agent Capabilities

### 📝 Documentation Tasks
- **Docstrings**: Adds Python, JavaScript, and TypeScript docstrings following standard conventions
- **Type hints**: Adds missing Python type hints and TypeScript types
- **Comments**: Adds inline comments for complex or non-obvious code
- **TODO comments**: Creates `#TODO` comments for code issues without modifying functional code

### 🛠️ Available Tools
- **Read**: View file contents and directory listings
- **Write**: Create new documentation files
- **Edit**: Make precise edits to existing files
- **Glob**: Find files by patterns
- **Grep**: Search file contents

### 🚫 Restrictions
- **No functional code changes**: Only documentation improvements
- **No dangerous tools**: Bash and WebSearch are disabled
- **Safe operations**: Auto-accepts documentation edits only

## Configuration

### Agent Configuration
```python
agent = DocumentationAgent(
    max_turns=5,  # Maximum conversation turns
    model="claude-3-5-sonnet-20241022"  # Claude model to use
)
```

### CLI Options
- `--max-turns N`: Set maximum conversation turns
- `--model MODEL`: Choose Claude model
- `--project-root PATH`: Set project root directory

## Examples

### Example 1: Processing Changed Files
```bash
# After git pull with changes
uv run python pull_ai_nova.py --claude
```

Output:
```
🤖 Starting Claude Code SDK agent for 3 changed files...
==================================================
[Using tool: Read]
Examining dynamodb_test.py...

[Using tool: Edit]
Adding docstring to write_to_dynamodb function...

[Using tool: Edit]
Adding type hints and TODO comment for error handling...

==================================================
✅ Claude Code SDK agent completed successfully!
💰 Cost: $0.0234
⏱️  Duration: 12.3s
```

### Example 2: Interactive Session
```bash
uv run python pull_ai_nova.py --interactive
```

```
🤖 Starting interactive documentation session...
Type 'exit' or 'quit' to end the session
==================================================

📝 What documentation task would you like me to help with? Add docstrings to all functions in src/

[Using tool: Glob]
Finding Python files in src/...

[Using tool: Read]
Examining src/utils.py...

[Using tool: Edit]
Adding docstring to calculate_total function...
```

## File Structure

```
claude_code_tools/
├── __init__.py                 # Package initialization
├── documentation_agent.py     # Main DocumentationAgent class
├── cli_integration.py         # CLI interface
└── README.md                  # This file
```

## Troubleshooting

### Common Issues

1. **"CLI not found" error**
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```

2. **Import errors**
   ```bash
   uv sync  # Ensure all dependencies are installed
   ```

3. **API key issues**
   - Check `.env` file exists and contains `ANTHROPIC_API_KEY`
   - Verify the key is valid

4. **Permission errors**
   - Agent runs with `acceptEdits` mode for documentation changes
   - No dangerous operations are allowed

### Debugging

Enable verbose output:
```bash
# Check if Claude Code CLI is available
claude-code --version

# Test SDK import
uv run python -c "from claude_code_sdk import ClaudeSDKClient; print('SDK available')"

# Run with error details
uv run python -m claude_code_tools.cli_integration --changed-files --verbose
```

## Performance

- **Typical costs**: $0.01-0.05 per file depending on size and complexity
- **Speed**: 5-15 seconds per file
- **Efficiency**: Only processes files that have actually changed
- **Smart caching**: Reuses context between related files

## Contributing

When adding new features:
1. Maintain documentation-only restriction
2. Add appropriate error handling
3. Include cost and performance metrics
4. Test both SDK and legacy fallback modes
5. Update this README with new capabilities