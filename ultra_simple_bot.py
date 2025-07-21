#!/usr/bin/env python3
"""
Ultra Simple Telegram Bot with Gemini AI
This version uses the most basic approach possible to avoid all version conflicts.
"""

import os
import asyncio
import logging
import requests
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
BOT_NAME = "Gemini Chat Bot"

# Initialize Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

# Store conversations
conversations = {}

async def generate_response(user_id, message):
    """Generate response using Gemini."""
    try:
        # Add to conversation history
        if user_id not in conversations:
            conversations[user_id] = []
        
        conversations[user_id].append({"role": "user", "content": message})
        
        # Keep only last 10 messages
        if len(conversations[user_id]) > 20:
            conversations[user_id] = conversations[user_id][-20:]
        
        # Create chat session
        chat = model.start_chat(history=conversations[user_id][:-1])
        response = await chat.send_message_async(message)
        
        # Add bot response to history
        conversations[user_id].append({"role": "model", "content": response.text})
        
        return response.text
    except Exception as e:
        logger.error(f"Gemini error: {e}")
        return f"Sorry, I encountered an error: {str(e)}"

def clear_history(user_id):
    """Clear conversation history."""
    if user_id in conversations:
        conversations[user_id] = []

def send_telegram_message(chat_id, text):
    """Send message using Telegram API directly."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, data=data)
        return response.json()
    except Exception as e:
        logger.error(f"Telegram API error: {e}")
        return None

def get_updates(offset=None):
    """Get updates from Telegram API directly."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    params = {"timeout": 30}
    if offset:
        params["offset"] = offset
    
    try:
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        logger.error(f"Get updates error: {e}")
        return None

async def main():
    """Main bot function using direct API calls."""
    if not TELEGRAM_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN not found in .env file")
        return
    
    if not GEMINI_API_KEY:
        print("❌ GEMINI_API_KEY not found in .env file")
        return
    
    print("🤖 Ultra Simple Telegram Gemini Bot")
    print("=" * 40)
    print("🚀 Starting bot...")
    print("💡 Press Ctrl+C to stop")
    
    offset = None
    
    try:
        while True:
            # Get updates
            updates = get_updates(offset)
            
            if updates and updates.get("ok") and updates.get("result"):
                for update in updates["result"]:
                    offset = update["update_id"] + 1
                    
                    if "message" in update:
                        message = update["message"]
                        chat_id = message["chat"]["id"]
                        user_id = message["from"]["id"]
                        
                        if "text" in message:
                            text = message["text"]
                            
                            # Handle commands
                            if text.startswith("/start"):
                                welcome = f"""
🤖 Welcome to {BOT_NAME}!

I'm powered by Google's Gemini AI and ready to chat!

Commands:
• Just send a message to chat
• /help - Show help
• /clear - Clear history
• /about - About this bot

Start chatting now! 🚀
                                """
                                send_telegram_message(chat_id, welcome)
                                
                            elif text.startswith("/help"):
                                help_text = """
🤖 **Bot Commands:**

• Send any message to chat with me
• /start - Welcome message
• /help - Show this help
• /clear - Clear conversation history
• /about - About this bot

I can help with questions, writing, coding, and more!
                                """
                                send_telegram_message(chat_id, help_text)
                                
                            elif text.startswith("/clear"):
                                clear_history(user_id)
                                send_telegram_message(chat_id, "🧹 Conversation history cleared!")
                                
                            elif text.startswith("/about"):
                                about_text = f"""
🤖 **About {BOT_NAME}**

• Powered by Google Gemini 1.5 Flash
• Built with Python and direct Telegram API
• Features: AI chat, context awareness
• Free to use with Gemini API
                                """
                                send_telegram_message(chat_id, about_text)
                                
                            else:
                                # Generate AI response
                                response = await generate_response(user_id, text)
                                send_telegram_message(chat_id, response)
            
            # Wait a bit before next poll
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
        return
    except asyncio.CancelledError:
        print("\n👋 Bot stopped")
        return
    except Exception as e:
        print(f"❌ Error: {e}")
        logger.error(f"Bot error: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}") 