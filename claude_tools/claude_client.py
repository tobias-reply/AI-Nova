#!/usr/bin/env python3
import os
import json
import requests
from typing import Dict, List, Any, Optional
from .text_editor import TextEditor

class ClaudeClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
        
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.model = "claude-4-opus-20241022"  # Claude 4 model
        self.text_editor = TextEditor()
        
    def _make_request(self, messages: List[Dict], tools: List[Dict]) -> Dict:
        """Make request to Claude API"""
        headers = {
            "content-type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01"
        }
        
        data = {
            "model": self.model,
            "max_tokens": 4096,
            "tools": tools,
            "messages": messages
        }
        
        response = requests.post(self.base_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    
    def chat_with_tools(self, initial_prompt: str, max_iterations: int = 10) -> str:
        """Chat with Claude using text editor tools"""
        tools = [{
            "type": "text_editor_20250728",
            "name": "str_replace_based_edit_tool",
            "max_characters": 10000
        }]
        
        messages = [{
            "role": "user",
            "content": initial_prompt
        }]
        
        conversation_log = []
        
        for iteration in range(max_iterations):
            print(f"Claude iteration {iteration + 1}...")
            
            try:
                response = self._make_request(messages, tools)
                
                # Add assistant's response to messages
                messages.append({
                    "role": "assistant",
                    "content": response["content"]
                })
                
                # Log the response
                conversation_log.append(f"=== Claude Response {iteration + 1} ===")
                for content in response["content"]:
                    if content["type"] == "text":
                        conversation_log.append(content["text"])
                        print(content["text"])
                
                # Check if Claude used tools
                tool_results = []
                used_tools = False
                
                for content in response["content"]:
                    if content["type"] == "tool_use":
                        used_tools = True
                        tool_name = content["name"]
                        tool_input = content["input"]
                        tool_id = content["id"]
                        
                        print(f"Executing tool: {tool_name} with {tool_input}")
                        conversation_log.append(f"Tool used: {tool_name} - {tool_input}")
                        
                        # Execute the tool
                        if tool_name == "str_replace_based_edit_tool":
                            result = self.text_editor.handle_command(tool_input)
                            
                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": tool_id,
                                "content": result.get("content", result.get("error", "Unknown error"))
                            })
                            
                            conversation_log.append(f"Tool result: {result}")
                
                # If tools were used, continue the conversation with results
                if used_tools:
                    messages.append({
                        "role": "user",
                        "content": tool_results
                    })
                else:
                    # No tools used, conversation is complete
                    break
                    
            except Exception as e:
                error_msg = f"Error in iteration {iteration + 1}: {str(e)}"
                print(error_msg)
                conversation_log.append(error_msg)
                break
        
        # Save conversation log
        with open("claude_conversation.log", "w") as f:
            f.write("\n".join(conversation_log))
        
        return "\n".join(conversation_log)