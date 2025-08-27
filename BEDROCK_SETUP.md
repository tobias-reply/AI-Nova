# Amazon Bedrock Setup Guide

This guide helps you configure Amazon Bedrock for the Claude Code SDK, which allows you to use Claude through your AWS account instead of direct Anthropic API credits.

## 🎯 Benefits of Using Bedrock

- **Use your AWS account**: No separate Anthropic API credits needed
- **Enterprise features**: AWS security, compliance, and logging
- **Cost management**: AWS billing and cost controls
- **Regional deployment**: Choose your preferred AWS region

## 📋 Prerequisites

1. **AWS Account** with Bedrock access
2. **AWS CLI** configured or AWS credentials
3. **Bedrock Claude models** enabled in your AWS region

## 🚀 Step 1: Enable Claude Models in Bedrock

1. **Go to AWS Bedrock Console:**
   ```
   https://console.aws.amazon.com/bedrock/
   ```

2. **Navigate to Model Access** (left sidebar)

3. **Request access to Claude models:**
   - Click "Edit" or "Manage model access"
   - Find Anthropic Claude models:
     - `Claude 3.5 Sonnet`
     - `Claude 3 Opus` (if available)
     - `Claude 3 Haiku`
   - Select the models you want
   - Click "Request model access"

4. **Wait for approval** (usually immediate for most accounts)

## 🔑 Step 2: Configure AWS Credentials

### Option A: AWS CLI (Recommended)

1. **Install AWS CLI** (if not already installed):
   ```bash
   # macOS
   brew install awscli
   
   # Or download from AWS
   curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
   sudo installer -pkg AWSCLIV2.pkg -target /
   ```

2. **Configure AWS credentials:**
   ```bash
   aws configure
   ```
   
   Enter:
   - **AWS Access Key ID**: Your access key
   - **AWS Secret Access Key**: Your secret key
   - **Default region name**: `us-east-1` (or your preferred region)
   - **Default output format**: `json`

3. **Test the configuration:**
   ```bash
   aws bedrock list-foundation-models --region us-east-1
   ```

### Option B: Environment Variables

Add to your `.env` file:
```bash
# Amazon Bedrock Configuration
CLAUDE_CODE_USE_BEDROCK=1

# AWS Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_DEFAULT_REGION=us-east-1
```

### Option C: IAM Roles (for EC2/ECS)

If running on AWS infrastructure, use IAM roles instead of credentials.

## 📍 Step 3: Choose Your Region

Supported regions for Claude in Bedrock:
- `us-east-1` (N. Virginia) - **Recommended**
- `us-west-2` (Oregon)
- `ap-southeast-1` (Singapore)
- `eu-central-1` (Frankfurt)

Update your region in `.env`:
```bash
AWS_DEFAULT_REGION=us-east-1
```

## 🔧 Step 4: Test the Configuration

1. **Test AWS credentials:**
   ```bash
   uv run python -c "
   import boto3
   try:
       client = boto3.client('bedrock', region_name='us-east-1')
       models = client.list_foundation_models()
       claude_models = [m for m in models['modelSummaries'] if 'claude' in m['modelId'].lower()]
       print(f'✅ Found {len(claude_models)} Claude models in Bedrock')
       for model in claude_models[:3]:
           print(f'   - {model[\"modelId\"]}')
   except Exception as e:
       print(f'❌ AWS Bedrock test failed: {e}')
   "
   ```

2. **Test Claude Code SDK with Bedrock:**
   ```bash
   uv run python -c "from claude_code_tools import DocumentationAgent; agent = DocumentationAgent()"
   ```

3. **Run a simple test:**
   ```bash
   uv run python -m claude_code_tools.cli_integration --files dynamodb_test.py
   ```

## 💰 Cost Information

### Bedrock Pricing (pay-per-token):
- **Claude 3.5 Sonnet**: ~$3 per million input tokens, ~$15 per million output tokens
- **Claude 3 Haiku**: ~$0.25 per million input tokens, ~$1.25 per million output tokens
- **Typical documentation task**: $0.01-0.05 per file

### Cost Control:
- Set up AWS budgets and alerts
- Use CloudWatch to monitor usage
- Consider using Claude 3 Haiku for simpler tasks

## 🛠️ Step 5: Update Your Workflow

Your `.env` should look like:
```bash
# Amazon Bedrock Configuration
CLAUDE_CODE_USE_BEDROCK=1
AWS_DEFAULT_REGION=us-east-1

# AWS credentials are handled by AWS CLI or IAM roles
# No ANTHROPIC_API_KEY needed for Bedrock mode
```

## 🔄 Usage

All existing commands work the same:
```bash
# Pull and run documentation agent via Bedrock
uv run python pull_ai_nova.py --claude

# Interactive session via Bedrock  
uv run python pull_ai_nova.py --interactive

# Direct usage via Bedrock
uv run python -m claude_code_tools.cli_integration --general-review
```

## 🚨 Troubleshooting

### Common Issues:

1. **"Model not found" error:**
   - Ensure Claude models are enabled in Bedrock console
   - Check you're using the correct region

2. **"Access denied" error:**
   - Verify AWS credentials are configured
   - Ensure your AWS account has Bedrock permissions
   - Check IAM policies include Bedrock access

3. **"No credentials" error:**
   - Run `aws configure` to set up credentials
   - Or set AWS environment variables in `.env`

4. **"Region not supported" error:**
   - Use a supported region like `us-east-1`
   - Update `AWS_DEFAULT_REGION` in your `.env`

### Debug Commands:

```bash
# Check AWS configuration
aws configure list

# List available regions
aws bedrock list-foundation-models --region us-east-1 --query 'modelSummaries[?contains(modelId, `claude`)].modelId'

# Test Bedrock access
aws bedrock invoke-model --region us-east-1 --model-id anthropic.claude-3-sonnet-20240229-v1:0 --body '{"prompt":"Hello","max_tokens_to_sample":10}' output.json
```

## 🎉 Success!

Once configured, you'll see:
```
🔧 Using Amazon Bedrock for Claude Code SDK
   AWS credentials: Using default profile (AWS CLI)
   AWS Region: us-east-1
```

Your documentation agent now uses Bedrock instead of direct Anthropic API credits!