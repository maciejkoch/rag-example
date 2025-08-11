#!/usr/bin/env python3
"""
Script to show where Python packages are installed
"""

import sys
import site
import subprocess

def main():
    print("🐍 Python Package Installation Info")
    print("=" * 50)
    
    # Show Python executable location
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    print()
    
    # Show site-packages directories
    print("📦 Package installation directories:")
    for path in sys.path:
        if 'site-packages' in path:
            print(f"  - {path}")
    print()
    
    # Show user site directory
    print(f"👤 User site directory: {site.getusersitepackages()}")
    print()
    
    # Check if in virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("🌐 Currently in a VIRTUAL ENVIRONMENT")
        print(f"Virtual env prefix: {sys.prefix}")
    else:
        print("🌍 Using GLOBAL Python installation")
    print()
    
    # Show installed packages
    print("📋 Currently installed packages:")
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'list'], 
                              capture_output=True, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"Error listing packages: {e}")

if __name__ == "__main__":
    main()