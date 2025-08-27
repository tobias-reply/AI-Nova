#!/usr/bin/env python3
"""
Documentation Agent - Claude Code SDK Agent for automated documentation improvements
"""

import asyncio
import os
from typing import List, Optional, Dict, Any
from datetime import datetime
from dotenv import load_dotenv
from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions

# Load environment variables
load_dotenv()

class DocumentationAgent:
    """Claude Code SDK agent for automated documentation improvements"""
    
    def __init__(self, max_turns: int = 5, model: str = None, system_prompt_file: str = "system_prompt.txt"):
        self.max_turns = max_turns
        self.system_prompt_file = system_prompt_file
        # Use simple, reliable model for Bedrock or default for API
        self.model = model or self._get_default_model()
        self.system_prompt = self._load_system_prompt()
        self._check_configuration()

    def _load_system_prompt(self) -> str:
        """Load system prompt from file"""
        try:
            # Try relative to this file first
            script_dir = os.path.dirname(os.path.abspath(__file__))
            prompt_path = os.path.join(script_dir, self.system_prompt_file)
            
            if os.path.exists(prompt_path):
                with open(prompt_path, 'r') as f:
                    return f.read().strip()
            
            # Try current working directory
            if os.path.exists(self.system_prompt_file):
                with open(self.system_prompt_file, 'r') as f:
                    return f.read().strip()
            
            print(f"⚠️  System prompt file '{self.system_prompt_file}' not found, using default")
            return self._get_default_system_prompt()
            
        except Exception as e:
            print(f"⚠️  Error loading system prompt: {e}")
            return self._get_default_system_prompt()

    def _get_default_system_prompt(self) -> str:
        """Fallback system prompt"""
        return """You are a documentation assistant. Add docstrings, comments, and type hints to code without modifying functional logic."""

    def _get_default_model(self) -> str:
        """Get default model based on authentication method"""
        use_bedrock = os.getenv('CLAUDE_CODE_USE_BEDROCK', '').lower() in ['1', 'true', 'yes']
        
        if use_bedrock:
            # Use Claude 3.5 Sonnet inference profile for Bedrock
            region = os.getenv('AWS_REGION', 'us-east-1')
            if region == 'eu-central-1':
                return "eu.anthropic.claude-3-5-sonnet-20240620-v1:0"
            else:
                return "us.anthropic.claude-3-5-sonnet-20240620-v1:0"
        else:
            # Default for direct Anthropic API
            return "claude-3-5-sonnet-20241022"

    def _check_configuration(self):
        """Check and display current authentication configuration"""
        use_bedrock = os.getenv('CLAUDE_CODE_USE_BEDROCK', '').lower() in ['1', 'true', 'yes']
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        
        if use_bedrock:
            print("🔧 Using Amazon Bedrock for Claude Code SDK")
            # Check AWS configuration
            aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
            aws_profile = os.getenv('AWS_PROFILE', 'default')
            aws_region = os.getenv('AWS_REGION', os.getenv('AWS_DEFAULT_REGION', 'us-east-1'))
            
            if aws_access_key:
                print(f"   AWS Region: {aws_region}")
                print("   AWS credentials: Environment variables")
            else:
                print(f"   AWS credentials: Profile '{aws_profile}' (AWS CLI)")
                print(f"   AWS Region: {aws_region}")
            
            # Test AWS connection
            self._test_aws_connection()
        elif anthropic_key:
            print("🔧 Using Anthropic API directly")
            print(f"   API Key: {anthropic_key[:20]}...")
        else:
            print("⚠️  No authentication configured!")
            print("   Set CLAUDE_CODE_USE_BEDROCK=1 for Bedrock, or ANTHROPIC_API_KEY for direct API")

    def _test_aws_connection(self):
        """Test AWS connection and Bedrock access"""
        try:
            import boto3
            from botocore.exceptions import NoCredentialsError, ClientError
            
            print("   Testing AWS connection...")
            
            # Test basic AWS connection
            session = boto3.Session(profile_name=os.getenv('AWS_PROFILE'))
            sts = session.client('sts')
            identity = sts.get_caller_identity()
            print(f"   ✅ AWS Identity: {identity.get('Arn', 'Unknown')}")
            
            # Test Bedrock access
            region = os.getenv('AWS_REGION', os.getenv('AWS_DEFAULT_REGION', 'us-east-1'))
            bedrock = session.client('bedrock', region_name=region)
            models = bedrock.list_foundation_models()
            claude_models = [m for m in models['modelSummaries'] if 'claude' in m['modelId'].lower()]
            
            if claude_models:
                print(f"   ✅ Bedrock access: Found {len(claude_models)} Claude models")
                print(f"   🤖 Using model: {self.model}")
            else:
                print("   ⚠️  No Claude models found in Bedrock")
                print("      Make sure Claude models are enabled in the Bedrock console")
                
        except NoCredentialsError:
            print("   ❌ No AWS credentials found")
            print("      Run 'aws configure' or set AWS environment variables")
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'Unknown')
            print(f"   ❌ AWS Error ({error_code}): {e}")
            if error_code == 'AccessDeniedException':
                print("      Check your AWS permissions for Bedrock access")
        except Exception as e:
            print(f"   ❌ Connection test failed: {e}")

    async def process_files(self, files: List[str], project_root: str = ".") -> Dict[str, Any]:
        """Process a list of files for documentation improvements"""
        if not files:
            print("No files to process.")
            return {"status": "no_files", "files_processed": 0}

        # Create the prompt with file list
        files_text = "\n".join([f"- {file}" for file in files])
        prompt = f"""I have the following files that need documentation review:

{files_text}

Please examine each file and improve its documentation. Focus on:
1. Adding missing docstrings to functions and classes
2. Adding type hints where they're missing
3. Adding comments for complex or non-obvious code sections
4. Creating #TODO comments for any code issues you identify
5. Ensuring documentation follows Python/JavaScript/TypeScript conventions

Start by examining the first file and work through each one systematically."""

        return await self._run_agent(prompt, project_root)

    async def general_review(self, project_root: str = ".") -> Dict[str, Any]:
        """Run a general documentation review of the project"""
        prompt = """Please perform a general documentation review of this project:

1. Look for files that are missing documentation
2. Identify functions/classes without proper docstrings
3. Find areas where inline comments would be helpful
4. Check for missing type hints
5. Look for any code issues and create #TODO comments

Focus on the most important files first (main modules, core functionality)."""

        return await self._run_agent(prompt, project_root)

    async def _run_agent(self, prompt: str, project_root: str) -> Dict[str, Any]:
        """Run the Claude agent with the given prompt"""
        results = {
            "status": "success", 
            "messages": [],
            "cost": 0.0,
            "duration_ms": 0,
            "session_id": None
        }

        start_time = datetime.now()
        
        try:
            print("🤖 Initializing Claude Code SDK client...")
            
            # Create client with timeout
            options = ClaudeCodeOptions(
                system_prompt=self.system_prompt,
                max_turns=self.max_turns,
                model=self.model,
                cwd=project_root,
                allowed_tools=["Read", "Write", "Edit", "Glob", "Grep"],
                disallowed_tools=["Bash", "WebSearch"],
                permission_mode="acceptEdits"
            )
            
            print(f"📋 Configuration:")
            print(f"   Model: {self.model}")
            print(f"   Max turns: {self.max_turns}")
            print(f"   Working directory: {project_root}")
            print(f"   Tools: Read, Write, Edit, Glob, Grep")
            print(f"   Bedrock mode: {os.getenv('CLAUDE_CODE_USE_BEDROCK', 'false')}")
            
            async with ClaudeSDKClient(options=options) as client:
                print("✅ Client connected successfully")
                print("🚀 Sending query to Claude...")
                print("=" * 50)
                
                # Send query with timeout
                query_task = asyncio.create_task(client.query(prompt))
                await asyncio.wait_for(query_task, timeout=30.0)
                print("✅ Query sent successfully")

                # Process response with timeout and better error handling
                message_text = []
                response_count = 0
                
                try:
                    print("📡 Receiving response...")
                    async for message in client.receive_response():
                        response_count += 1
                        print(f"📨 Processing message {response_count}...")
                        
                        if hasattr(message, 'content'):
                            for block in message.content:
                                if hasattr(block, 'type'):
                                    if block.type == 'tool_use':
                                        tool_info = f"[Using tool: {block.name}]"
                                        print(f"\n🔧 {tool_info}")
                                        message_text.append(tool_info)
                                        if hasattr(block, 'input'):
                                            print(f"   Input: {str(block.input)[:100]}...")
                                if hasattr(block, 'text'):
                                    print(block.text, end='', flush=True)
                                    message_text.append(block.text)

                        # Check for different message types
                        message_type = type(message).__name__
                        print(f"\n📋 Message type: {message_type}")
                        
                        if message_type == "ResultMessage":
                            print("✅ Received final result message")
                            results.update({
                                "cost": getattr(message, 'total_cost_usd', 0.0),
                                "duration_ms": getattr(message, 'duration_ms', 0),
                                "session_id": getattr(message, 'session_id', None),
                                "messages": message_text
                            })
                            break
                        elif message_type == "ErrorMessage":
                            error_msg = getattr(message, 'error', 'Unknown error')
                            print(f"❌ Received error message: {error_msg}")
                            raise Exception(f"Claude returned error: {error_msg}")
                        
                        # Safety timeout per message
                        elapsed = (datetime.now() - start_time).total_seconds()
                        if elapsed > 300:  # 5 minute total timeout
                            print(f"⏰ Timeout after {elapsed:.1f}s - stopping")
                            break
                
                except asyncio.TimeoutError:
                    print("⏰ Response timeout - the agent may still be processing")
                    results.update({"status": "timeout", "error": "Response timeout"})
                    return results
                
                elapsed = (datetime.now() - start_time).total_seconds()
                print(f"\n" + "=" * 50)
                print(f"✅ Documentation agent completed!")
                print(f"💰 Cost: ${results['cost']:.4f}")
                print(f"⏱️  Duration: {elapsed:.1f}s")
                print(f"📨 Messages processed: {response_count}")
                
                return results

        except asyncio.TimeoutError:
            print("⏰ Timeout during query sending")
            results.update({
                "status": "timeout",
                "error": "Query timeout after 30 seconds"
            })
            return results
        except Exception as e:
            elapsed = (datetime.now() - start_time).total_seconds()
            print(f"❌ Agent failed after {elapsed:.1f}s: {str(e)}")
            print(f"🔍 Error type: {type(e).__name__}")
            
            # More detailed error information
            if "bedrock" in str(e).lower():
                print("💡 This appears to be a Bedrock-related error")
                print("   Check: AWS credentials, region, model access")
            elif "permission" in str(e).lower():
                print("💡 This appears to be a permission error")
                print("   Check: AWS IAM permissions for Bedrock")
            elif "model" in str(e).lower():
                print("💡 This appears to be a model-related error")  
                print("   Check: Model availability and access in Bedrock console")
            
            results.update({
                "status": "error",
                "error": str(e),
                "error_type": type(e).__name__
            })
            return results

    async def interactive_session(self, project_root: str = ".") -> None:
        """Start an interactive documentation session"""
        print("🤖 Starting interactive documentation session...")
        print("Type 'exit' or 'quit' to end the session")
        print("=" * 50)

        async with ClaudeSDKClient(
            options=ClaudeCodeOptions(
                system_prompt=self.system_prompt,
                max_turns=10,
                model=self.model,
                cwd=project_root,
                allowed_tools=["Read", "Write", "Edit", "Glob", "Grep"],
                disallowed_tools=["Bash", "WebSearch"],
                permission_mode="acceptEdits"
            )
        ) as client:
            
            while True:
                try:
                    user_input = input("\n📝 What documentation task would you like me to help with? ")
                    
                    if user_input.lower() in ['exit', 'quit', 'q']:
                        print("👋 Ending documentation session.")
                        break
                    
                    if not user_input.strip():
                        continue
                    
                    await client.query(user_input)
                    
                    async for message in client.receive_response():
                        if hasattr(message, 'content'):
                            for block in message.content:
                                if hasattr(block, 'type'):
                                    if block.type == 'tool_use':
                                        print(f"\n[Using tool: {block.name}]")
                                if hasattr(block, 'text'):
                                    print(block.text, end='', flush=True)
                        
                        if type(message).__name__ == "ResultMessage":
                            print(f"\n💰 Cost: ${message.total_cost_usd:.4f}")
                            break
                
                except KeyboardInterrupt:
                    print("\n👋 Session interrupted.")
                    break
                except Exception as e:
                    print(f"\n❌ Error: {str(e)}")
                    continue