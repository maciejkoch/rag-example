#!/usr/bin/env python3
"""
Setup script for the Simple RAG System
"""

import os
import subprocess
import sys


def create_virtual_environment():
    """Create virtual environment if it doesn't exist"""
    venv_path = "venv"
    if os.path.exists(venv_path):
        print("✅ Virtual environment already exists")
        return True
    
    print("🔨 Creating virtual environment...")
    try:
        subprocess.check_call([sys.executable, "-m", "venv", venv_path])
        print("✅ Virtual environment created successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating virtual environment: {e}")
        return False


def get_venv_python():
    """Get the python executable from virtual environment"""
    if os.name == 'nt':  # Windows
        return os.path.join("venv", "Scripts", "python.exe")
    else:  # macOS/Linux
        return os.path.join("venv", "bin", "python")


def install_requirements():
    """Install the required packages in virtual environment"""
    print("📦 Installing requirements in virtual environment...")
    
    venv_python = get_venv_python()
    if not os.path.exists(venv_python):
        print("❌ Virtual environment python not found. Please run setup again.")
        return False
    
    try:
        subprocess.check_call([venv_python, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False


def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = ".env"
    env_example = ".env.example"
    
    if os.path.exists(env_file):
        print("✅ .env file already exists")
        return True
    
    if os.path.exists(env_example):
        # Copy from example
        with open(env_example, 'r') as f:
            content = f.read()
        with open(env_file, 'w') as f:
            f.write(content)
        print("📝 Created .env file from .env.example")
    else:
        # Create basic .env file
        with open(env_file, 'w') as f:
            f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
        print("📝 Created basic .env file")
    
    print("⚠️  Please edit .env and add your OpenAI API key!")
    return True


def main():
    """Main setup function"""
    print("🚀 Setting up Simple RAG System...")
    print("=" * 50)
    
    # Create virtual environment
    if not create_virtual_environment():
        print("❌ Setup failed during virtual environment creation")
        return False
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed during package installation")
        return False
    
    # Create .env file
    if not create_env_file():
        print("❌ Setup failed during .env creation")
        return False
    
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit .env file and add your OpenAI API key")
    print("2. Activate virtual environment:")
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\activate")
    else:  # macOS/Linux
        print("   source venv/bin/activate")
    print("3. Run: python rag_system.py (for demo)")
    print("4. Or run: python interactive_demo.py (for interactive mode)")
    print("\n🔗 Get your OpenAI API key: https://platform.openai.com/api-keys")
    print("\n💡 Packages are installed in: venv/lib/python3.x/site-packages/")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)