#!/usr/bin/env python3
"""
Launcher script for the Telegram Gemini Bot
This script provides a user-friendly way to start the bot with proper error handling.
"""

import asyncio
import sys
import os
from dotenv import load_dotenv

def check_env_file():
    """Check if .env file exists and create example if not."""
    if not os.path.exists('.env'):
        print("⚠️  .env file not found!")
        print("Creating .env.example file...")
        
        with open('.env.example', 'w') as f:
            f.write("# Telegram Bot Token (get from @BotFather)\n")
            f.write("TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here\n\n")
            f.write("# Google Gemini API Key\n")
            f.write("GEMINI_API_KEY=your_gemini_api_key_here\n")
        
        print("📝 Created .env.example file")
        print("📋 Please:")
        print("   1. Copy .env.example to .env")
        print("   2. Add your actual API keys to .env")
        print("   3. Run this script again")
        return False
    
    return True

def print_banner():
    """Print a nice banner."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                    🤖 TELEGRAM GEMINI BOT 🤖                  ║
║                                                              ║
║  Powered by Google Gemini AI & Python Telegram Bot API      ║
║  Intelligent conversations with context awareness            ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

async def main():
    """Main launcher function."""
    print_banner()
    
    # Load environment variables
    load_dotenv()
    
    # Check if .env file exists
    if not check_env_file():
        sys.exit(1)
    
    # Check if API keys are set
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    if not telegram_token or telegram_token == 'your_telegram_bot_token_here':
        print("❌ Please set your TELEGRAM_BOT_TOKEN in the .env file")
        print("💡 Get it from @BotFather on Telegram")
        sys.exit(1)
    
    if not gemini_key or gemini_key == 'your_gemini_api_key_here':
        print("❌ Please set your GEMINI_API_KEY in the .env file")
        print("💡 Get it from https://makersuite.google.com/app/apikey")
        sys.exit(1)
    
    print("✅ Configuration looks good!")
    print("🚀 Starting the bot...")
    print("💡 Press Ctrl+C to stop the bot\n")
    
    try:
        # Import and run the bot
        from bot import main as bot_main
        await bot_main()
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting bot: {e}")
        print("💡 Try running 'python test_bot.py' to diagnose issues")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())