#!/usr/bin/env python3
"""
Startup script for the Clothing Swap Platform
"""

import os
import sys
import subprocess
from pathlib import Path

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path(".env")
    if not env_file.exists():
        env_content = """# Database Configuration
DATABASE_URL=sqlite:///./swap_app.db

# Security
SECRET_KEY=your-secret-key-here-change-in-production

# Gemini AI API Key
GEMINI_API_KEY=your-gemini-api-key-here
"""
        with open(env_file, "w") as f:
            f.write(env_content)
        print("✅ Created .env file")
        print("⚠️  Please update GEMINI_API_KEY in .env file")

def create_directories():
    """Create necessary directories"""
    directories = ["static", "static/uploads"]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    print("✅ Created static directories")

def install_dependencies():
    """Install required dependencies"""
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False
    return True

def main():
    print("🚀 Setting up Clothing Swap Platform...")
    
    # Create directories
    create_directories()
    
    # Create .env file
    create_env_file()
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed. Please install dependencies manually.")
        return
    
    print("\n🎉 Setup complete!")
    print("\n📋 Next steps:")
    print("1. Update GEMINI_API_KEY in .env file")
    print("2. Run: python -c \"from app.main import *; Base.metadata.create_all(bind=engine)\"")
    print("3. Start server: uvicorn app.main:app --reload")
    print("\n📖 API docs will be available at: http://localhost:8000/docs")

if __name__ == "__main__":
    main() 