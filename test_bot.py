#!/usr/bin/env python3
"""
Test script for the Telegram Gemini Bot
This script tests the configuration and API connections before running the main bot.
"""

import asyncio
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_configuration():
    """Test if all required configuration is present."""
    print("🔧 Testing Configuration...")
    
    # Check environment variables
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    if not telegram_token:
        print("❌ TELEGRAM_BOT_TOKEN not found in environment variables")
        return False
    else:
        print("✅ TELEGRAM_BOT_TOKEN found")
    
    if not gemini_key:
        print("❌ GEMINI_API_KEY not found in environment variables")
        return False
    else:
        print("✅ GEMINI_API_KEY found")
    
    return True

async def test_gemini_api():
    """Test Gemini API connection."""
    print("\n🤖 Testing Gemini API...")
    
    try:
        import google.generativeai as genai
        
        # Configure Gemini
        gemini_key = os.getenv('GEMINI_API_KEY')
        genai.configure(api_key=gemini_key)
        
        # Test with a simple prompt using free model
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = await model.generate_content_async("Hello! Please respond with 'API test successful' if you can see this message.")
        
        if response.text:
            print("✅ Gemini API connection successful")
            print(f"📝 Response: {response.text}")
            return True
        else:
            print("❌ Gemini API returned empty response")
            return False
            
    except Exception as e:
        print(f"❌ Gemini API test failed: {e}")
        return False

def test_dependencies():
    """Test if all required dependencies are installed."""
    print("\n📦 Testing Dependencies...")
    
    required_packages = [
        'telegram',
        'google.generativeai',
        'dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Please install missing packages with: pip install -r requirements.txt")
        return False
    
    return True

def test_telegram_bot():
    """Test Telegram bot setup."""
    print("\n🤖 Testing Telegram Bot Setup...")
    
    try:
        from telegram.ext import Application
        from telegram.constants import ParseMode
        print("✅ python-telegram-bot is properly installed")
        return True
    except Exception as e:
        print(f"❌ Telegram bot test failed: {e}")
        return False

async def main():
    """Run all tests."""
    print("🚀 Starting Telegram Gemini Bot Tests...\n")
    
    # Test dependencies
    if not test_dependencies():
        print("\n❌ Dependency test failed. Please install missing packages.")
        sys.exit(1)
    
    # Test configuration
    if not test_configuration():
        print("\n❌ Configuration test failed. Please check your .env file.")
        sys.exit(1)
    
    # Test Telegram bot setup
    if not test_telegram_bot():
        print("\n❌ Telegram bot test failed. Please check python-telegram-bot installation.")
        sys.exit(1)
    
    # Test Gemini API
    if not await test_gemini_api():
        print("\n❌ Gemini API test failed. Please check your API key.")
        sys.exit(1)
    
    print("\n🎉 All tests passed! Your bot is ready to run.")
    print("💡 Run 'python run_bot.py' to start the bot.")

if __name__ == "__main__":
    asyncio.run(main()) 