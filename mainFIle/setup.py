#!/usr/bin/env python3
"""
Setup script for Bengali ChatBot
"""
import subprocess
import sys
import os

def install_requirements():
    """Install required Python packages"""
    print("📦 Installing Python packages...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Python packages installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        return False
    return True

def check_ollama():
    """Check if Ollama is installed"""
    print("🔍 Checking Ollama installation...")
    try:
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Ollama is installed!")
            return True
        else:
            print("❌ Ollama is not working properly")
            return False
    except FileNotFoundError:
        print("❌ Ollama is not installed")
        print("Please install Ollama from: https://ollama.ai/")
        return False

def setup_ollama_model():
    """Setup Ollama model"""
    print("🤖 Setting up Ollama model...")
    try:
        print("Pulling llama3.1 model (this may take a while)...")
        subprocess.check_call(['ollama', 'pull', 'llama3.1'])
        print("✅ Ollama model setup complete!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to setup Ollama model: {e}")
        return False

def main():
    print("🚀 Setting up Bengali ChatBot...")
    print("=" * 50)
    
    # Install Python packages
    if not install_requirements():
        sys.exit(1)
    
    # Check Ollama
    if not check_ollama():
        print("\n📋 To complete setup:")
        print("1. Install Ollama from https://ollama.ai/")
        print("2. Run: ollama pull llama3.1")
        print("3. Run: python app.py")
        sys.exit(1)
    
    # Setup Ollama model
    if not setup_ollama_model():
        print("\n📋 Manual steps needed:")
        print("1. Run: ollama pull llama3.1")
        print("2. Run: python app.py")
        sys.exit(1)
    
    print("\n🎉 Setup complete!")
    print("📋 To start the chatbot:")
    print("1. Run: ollama run llama3.1")
    print("2. In another terminal, run: python app.py")
    print("3. Open browser to: http://localhost:5000")

if __name__ == "__main__":
    main()
