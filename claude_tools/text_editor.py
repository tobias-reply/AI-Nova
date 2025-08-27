#!/usr/bin/env python3
import os
import shutil
import json
from typing import Dict, Any, Optional

class TextEditor:
    def __init__(self, backup_dir: str = ".claude_backups"):
        self.backup_dir = backup_dir
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
    
    def _create_backup(self, file_path: str) -> str:
        """Create a backup of the file before editing"""
        if not os.path.exists(file_path):
            return ""
        
        backup_name = f"{os.path.basename(file_path)}.backup"
        backup_path = os.path.join(self.backup_dir, backup_name)
        shutil.copy2(file_path, backup_path)
        return backup_path
    
    def _validate_path(self, file_path: str) -> bool:
        """Validate file path to prevent directory traversal"""
        # Convert to absolute path and check if it's within allowed directories
        abs_path = os.path.abspath(file_path)
        current_dir = os.path.abspath(".")
        return abs_path.startswith(current_dir)
    
    def handle_command(self, command_data: Dict[str, Any]) -> Dict[str, str]:
        """Handle text editor commands from Claude"""
        try:
            command = command_data.get('command')
            file_path = command_data.get('path', '')
            
            if not self._validate_path(file_path):
                return {"error": "Invalid file path"}
            
            if command == 'view':
                return self._handle_view(file_path, command_data.get('view_range'))
            elif command == 'str_replace':
                return self._handle_str_replace(file_path, command_data.get('old_str'), command_data.get('new_str'))
            elif command == 'create':
                return self._handle_create(file_path, command_data.get('file_text'))
            elif command == 'insert':
                return self._handle_insert(file_path, command_data.get('insert_line', 0), command_data.get('new_str'))
            else:
                return {"error": f"Unknown command: {command}"}
                
        except Exception as e:
            return {"error": f"Command failed: {str(e)}"}
    
    def _handle_view(self, file_path: str, view_range: Optional[list] = None) -> Dict[str, str]:
        """Handle view command"""
        try:
            if os.path.isdir(file_path):
                # List directory contents
                items = os.listdir(file_path)
                content = "\n".join(sorted(items))
                return {"content": content}
            
            if not os.path.exists(file_path):
                return {"error": f"File not found: {file_path}"}
            
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            if view_range:
                start_line = max(1, view_range[0]) - 1  # Convert to 0-indexed
                end_line = len(lines) if view_range[1] == -1 else min(len(lines), view_range[1])
                lines = lines[start_line:end_line]
            
            # Add line numbers
            numbered_lines = [f"{i+1}: {line.rstrip()}" for i, line in enumerate(lines)]
            content = "\n".join(numbered_lines)
            
            return {"content": content}
            
        except Exception as e:
            return {"error": f"Failed to view file: {str(e)}"}
    
    def _handle_str_replace(self, file_path: str, old_str: str, new_str: str) -> Dict[str, str]:
        """Handle string replacement"""
        try:
            if not os.path.exists(file_path):
                return {"error": f"File not found: {file_path}"}
            
            # Create backup
            self._create_backup(file_path)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if old_str not in content:
                return {"error": "Text to replace not found"}
            
            # Check for multiple matches
            if content.count(old_str) > 1:
                return {"error": f"Multiple matches found ({content.count(old_str)}). Please provide more specific text."}
            
            new_content = content.replace(old_str, new_str)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return {"content": "Successfully replaced text at exactly one location."}
            
        except Exception as e:
            return {"error": f"Failed to replace text: {str(e)}"}
    
    def _handle_create(self, file_path: str, file_text: str) -> Dict[str, str]:
        """Handle file creation"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(file_text)
            
            return {"content": f"Successfully created file: {file_path}"}
            
        except Exception as e:
            return {"error": f"Failed to create file: {str(e)}"}
    
    def _handle_insert(self, file_path: str, insert_line: int, new_str: str) -> Dict[str, str]:
        """Handle text insertion"""
        try:
            if not os.path.exists(file_path):
                return {"error": f"File not found: {file_path}"}
            
            # Create backup
            self._create_backup(file_path)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Insert at specified line (0 = beginning, len(lines) = end)
            insert_pos = min(insert_line, len(lines))
            lines.insert(insert_pos, new_str + '\n')
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            
            return {"content": f"Successfully inserted text at line {insert_line}"}
            
        except Exception as e:
            return {"error": f"Failed to insert text: {str(e)}"}