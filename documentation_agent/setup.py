#!/usr/bin/env python3
"""
Setup script for Documentation Agent
"""

import os
import subprocess
import sys
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 11):
        print("❌ Python 3.11+ required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    return True

def install_python_deps():
    """Install Python dependencies"""
    try:
        print("📦 Installing Python dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Python dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install Python dependencies")
        return False

def check_node_and_install_cli():
    """Check Node.js and install Claude Code CLI"""
    try:
        # Check Node.js
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Node.js not found. Please install Node.js 18+")
            return False
        
        node_version = result.stdout.strip()
        print(f"✅ Node.js {node_version}")
        
        # Install Claude Code CLI
        print("🚀 Installing Claude Code CLI...")
        subprocess.check_call(["npm", "install", "-g", "@anthropic-ai/claude-code"])
        print("✅ Claude Code CLI installed")
        return True
        
    except subprocess.CalledProcessError:
        print("❌ Failed to install Claude Code CLI")
        return False
    except FileNotFoundError:
        print("❌ Node.js not found. Please install Node.js 18+")
        return False

def setup_env_file():
    """Set up environment file"""
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if env_file.exists():
        print("⚠️  .env file already exists, skipping")
        return True
    
    if env_example.exists():
        print("📝 Creating .env file from template...")
        with open(env_example) as f:
            content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✅ .env file created")
        print("📝 Please edit .env file to configure your settings")
        return True
    
    print("❌ .env.example not found")
    return False

def validate_setup():
    """Validate the setup"""
    try:
        from agent import DocumentationAgent
        print("✅ Documentation agent can be imported")
        
        # Test configuration loading
        agent = DocumentationAgent()
        print("✅ Agent configuration loaded successfully")
        return True
        
    except Exception as e:
        print(f"❌ Setup validation failed: {e}")
        return False

def main():
    print("🚀 Setting up Documentation Agent...")
    print("=" * 50)
    
    steps = [
        ("Checking Python version", check_python_version),
        ("Installing Python dependencies", install_python_deps),
        ("Installing Claude Code CLI", check_node_and_install_cli),
        ("Setting up environment file", setup_env_file),
        ("Validating setup", validate_setup),
    ]
    
    success = True
    for step_name, step_func in steps:
        print(f"\n{step_name}...")
        if not step_func():
            success = False
            print(f"❌ Failed: {step_name}")
            break
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Edit .env file with your AWS profile/API key")
        print("2. Run: python config.py --validate")
        print("3. Test: python cli.py --files test_agent.py")
    else:
        print("❌ Setup failed. Please fix the issues above and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()