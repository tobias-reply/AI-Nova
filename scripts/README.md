# Issue Revision Automation

This workflow automatically revises GitHub issues that contain "WIP" using AWS Bedrock and Claude.

## Setup

### 1. Required GitHub Repository Secrets

Add these secrets to your GitHub repository settings:

- `AWS_ACCESS_KEY_ID`: Your AWS access key ID
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret access key  
- `AWS_REGION`: AWS region (e.g., `us-east-1`)

### 2. AWS Permissions

Your AWS credentials need permissions for:
- `bedrock:InvokeModel` for the Claude model: `anthropic.claude-3-sonnet-20240229-v1:0`

### 3. Dependencies

The workflow will automatically install required dependencies:
- `@aws-sdk/client-bedrock-runtime`
- `@octokit/rest`

## How it Works

1. When a new issue is opened, the workflow triggers
2. The handler checks if the issue description contains "WIP"
3. If found, it sends the description to Claude with:
   - A system prompt for issue revision guidelines
   - Project context about the Innovator codebase
   - The original issue description
4. Claude returns a revised, well-structured issue description
5. The workflow automatically updates the GitHub issue

## Files

- `.github/workflows/issue-revision.yml`: GitHub Actions workflow
- `scripts/issue-handler.js`: Main handler script
- `scripts/system-prompt.txt`: LLM system prompt for revision guidelines
- `scripts/project-context.txt`: Project-specific context for better revisions

## Customization

You can modify:
- `system-prompt.txt`: Adjust revision guidelines and formatting preferences
- `project-context.txt`: Update project description and technical details
- The Claude model ID in `issue-handler.js` if needed
- The trigger condition (currently checks for "WIP" string)