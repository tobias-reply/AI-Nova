# Documentation Agent - Claude Code SDK

A self-contained, transferable Claude Code SDK agent that automatically improves code documentation while preserving functional code integrity.

For more information consult:
https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-overview#authentication

## 📁 What's Included

This folder contains everything needed to run a documentation agent:

```
documentation_agent/
├── agent.py              # Main DocumentationAgent class
├── cli.py               # Command-line interface  
├── config.py            # Configuration utilities
├── system_prompt.txt    # Editable system prompt
├── requirements.txt     # Python dependencies
├── .env.example         # Environment configuration template
└── README.md           # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt

# Install Claude Code CLI (required)
npm install -g @anthropic-ai/claude-code
```

### 2. Configure Authentication

**Option A: Amazon Bedrock (Recommended)**
```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your settings
# Set AWS_PROFILE and AWS_REGION

# Configure AWS credentials
aws configure --profile your-profile-name
```

**Option B: Direct Anthropic API**
```bash
# Set in .env file
echo "CLAUDE_CODE_USE_BEDROCK=0" > .env
echo "ANTHROPIC_API_KEY=your_api_key_here" >> .env
```

### 3. Validate Configuration

```bash
python config.py --validate
```

### 4. Run the Agent

```bash
# Process specific files
python cli.py --files file1.py file2.js

# General documentation review
python cli.py --general-review

# Interactive session
python cli.py --interactive
```

## 🎯 Agent Capabilities

### What It Does
- ✅ **Adds missing docstrings** following language conventions
- ✅ **Adds type hints** where missing (Python, TypeScript)
- ✅ **Adds inline comments** for complex logic
- ✅ **Creates #TODO comments** for code issues it identifies
- ✅ **Documentation-only focus** - never modifies functional code

### What It Won't Do
- ❌ **No functional code changes** - preserves business logic
- ❌ **No dangerous operations** - restricted to safe file operations
- ❌ **No external network calls** - uses only local tools

### Available Tools
- **Read**: View file contents and directory listings
- **Write**: Create new documentation files
- **Edit**: Make precise edits to existing files
- **Glob**: Find files by patterns
- **Grep**: Search file contents

## 🔧 Configuration

### System Prompt

Edit `system_prompt.txt` to customize the agent's behavior:
```txt
You are a documentation assistant with access to development tools.

IMPORTANT RESTRICTIONS:
- You must ONLY work on documentation tasks
- DO NOT modify any functional code
- If you see code that needs changes, create a #TODO comment instead
...
```

### Environment Variables

Key configuration options in `.env`:

```bash
# Authentication Method
CLAUDE_CODE_USE_BEDROCK=1              # Use Bedrock (1) or Anthropic API (0)

# AWS Configuration (for Bedrock)
AWS_PROFILE=your-profile               # AWS profile to use
AWS_REGION=us-east-1                   # AWS region

# Compatibility Settings
DISABLE_PROMPT_CACHING=1               # Disable for Bedrock compatibility
MAX_THINKING_TOKENS=0                  # Disable thinking mode
CLAUDE_CODE_MAX_OUTPUT_TOKENS=4096     # Output token limit

# Model Override (optional)
ANTHROPIC_MODEL=us.anthropic.claude-3-5-sonnet-20240620-v1:0
```

### CLI Options

```bash
python cli.py [OPTIONS]

Options:
  --files FILE [FILE ...]       Process specific files
  --general-review              Review entire project
  --interactive                 Start interactive session
  --max-turns N                 Maximum conversation turns (default: 5)
  --model MODEL                 Override model selection
  --system-prompt PATH          Custom system prompt file
  --project-root PATH           Project root directory
```

## 🏗️ How to Create Your Own Agent

This documentation agent serves as a template for creating other Claude Code SDK agents. Here's how to adapt it:

### 1. Core Agent Structure

```python
from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions

class YourAgent:
    def __init__(self, model=None, system_prompt_file="system_prompt.txt"):
        self.model = model or self._get_default_model()
        self.system_prompt = self._load_system_prompt()
    
    async def _run_agent(self, prompt: str, project_root: str):
        options = ClaudeCodeOptions(
            system_prompt=self.system_prompt,
            model=self.model,
            cwd=project_root,
            allowed_tools=["Read", "Write", "Edit"],  # Choose your tools
            permission_mode="acceptEdits"
        )
        
        async with ClaudeSDKClient(options=options) as client:
            await client.query(prompt)
            # Process responses...
```

### 2. Key Components to Customize

**System Prompt** (`system_prompt.txt`):
- Define the agent's role and restrictions
- Specify what tasks it should/shouldn't do
- Include examples if helpful

**Tool Selection**:
- `Read`, `Write`, `Edit`, `Glob`, `Grep` - File operations
- `Bash` - Command execution (use carefully)
- `WebSearch` - Web searches
- Custom MCP tools

**Permission Mode**:
- `"default"` - Prompt for dangerous operations
- `"acceptEdits"` - Auto-accept file edits
- `"plan"` - Plan mode (read-only)
- `"bypassPermissions"` - Allow all (use carefully)

### 3. Common Agent Patterns

**Code Review Agent**:
```python
system_prompt = "You are a code reviewer. Find bugs, security issues, and suggest improvements."
allowed_tools = ["Read", "Grep", "WebSearch"]
permission_mode = "plan"  # Read-only
```

**Refactoring Agent**:
```python
system_prompt = "You are a refactoring expert. Improve code structure without changing behavior."
allowed_tools = ["Read", "Write", "Edit", "Bash"]
permission_mode = "default"  # Ask before dangerous operations
```

**Testing Agent**:
```python
system_prompt = "You are a testing expert. Create comprehensive tests for existing code."
allowed_tools = ["Read", "Write", "Edit", "Bash"]
permission_mode = "acceptEdits"  # Auto-accept test file edits
```

### 4. Authentication Patterns

**Bedrock Configuration**:
```python
def _get_default_model(self):
    region = os.getenv('AWS_REGION', 'us-east-1')
    if region.startswith('eu-'):
        return "eu.anthropic.claude-3-5-sonnet-20240620-v1:0"
    else:
        return "us.anthropic.claude-3-5-sonnet-20240620-v1:0"
```

**API Configuration**:
```python
def _get_default_model(self):
    return "claude-3-5-sonnet-20241022"
```

## 📊 Cost Management

### Typical Costs (Bedrock)
- **Small files** (< 100 lines): $0.01 - $0.02
- **Medium files** (100-500 lines): $0.02 - $0.05  
- **Large files** (500+ lines): $0.05 - $0.10

### Cost Control
- Use `--max-turns` to limit conversation length
- Set `CLAUDE_CODE_MAX_OUTPUT_TOKENS` appropriately
- Consider using Haiku model for simple tasks
- Monitor costs through AWS billing dashboard

## 🛠️ Troubleshooting

### Common Issues

**"Model not found" error:**
```bash
# Check available models
python config.py --validate

# Update model in .env
ANTHROPIC_MODEL=us.anthropic.claude-3-5-sonnet-20240620-v1:0
```

**"No credentials" error:**
```bash
# For Bedrock
aws configure --profile your-profile
export AWS_PROFILE=your-profile

# For API
export ANTHROPIC_API_KEY=your-key
```

**"Thinking not supported" error:**
```bash
# Add to .env
MAX_THINKING_TOKENS=0
```

### Debug Mode

Add verbose logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🚀 Advanced Usage

### Custom Tool Integration

```python
# Add MCP servers
options = ClaudeCodeOptions(
    system_prompt=self.system_prompt,
    mcp_servers={
        "custom_tool": {
            "command": "npx",
            "args": ["@your/custom-mcp-server"]
        }
    }
)
```

### Multi-Model Strategy

```python
# Use different models for different tasks
def _get_model_for_task(self, task_type):
    if task_type == "simple":
        return "us.anthropic.claude-3-5-haiku-20241022-v1:0"
    else:
        return "us.anthropic.claude-3-5-sonnet-20240620-v1:0"
```

### Batch Processing

```python
async def process_batch(self, file_batches):
    results = []
    for batch in file_batches:
        result = await self.process_files(batch)
        results.append(result)
        await asyncio.sleep(1)  # Rate limiting
    return results
```

## 📝 Contributing

To extend this agent:

1. **Fork the code** - Copy this entire folder
2. **Modify system_prompt.txt** - Define your agent's role
3. **Update agent.py** - Customize the main logic
4. **Extend cli.py** - Add new command-line options
5. **Test thoroughly** - Ensure safety restrictions work
6. **Document changes** - Update this README

## 🔒 Security Considerations

- **Review system prompts** carefully - they define agent behavior
- **Test with non-production code** first
- **Use `plan` mode** for read-only exploration
- **Limit tool access** to minimum necessary
- **Monitor costs** and set billing alerts
- **Review all changes** before committing to version control

## 📄 License

This agent template is provided as-is for educational and development purposes. Modify freely for your needs.