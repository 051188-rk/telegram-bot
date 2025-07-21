#!/usr/bin/env python3
"""
Terminal Chat with Gemini AI
Test the AI directly in the terminal without Telegram.
"""

import os
import asyncio
import logging
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
BOT_NAME = "Gemini Chat Bot"

# Initialize Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    print("❌ GEMINI_API_KEY not found in .env file")
    exit(1)

# Store conversation history
conversation_history = []

async def generate_response(message):
    """Generate response using Gemini."""
    try:
        # Add user message to history
        conversation_history.append({"role": "user", "content": message})
        
        # Keep only last 20 messages
        if len(conversation_history) > 20:
            conversation_history.pop(0)
        
        # Create chat session
        chat = model.start_chat(history=conversation_history[:-1])
        response = await chat.send_message_async(message)
        
        # Add bot response to history
        conversation_history.append({"role": "model", "content": response.text})
        
        return response.text
    except Exception as e:
        logger.error(f"Gemini error: {e}")
        return f"Sorry, I encountered an error: {str(e)}"

def clear_history():
    """Clear conversation history."""
    global conversation_history
    conversation_history = []
    print("🧹 Conversation history cleared!")

def show_help():
    """Show help information."""
    help_text = """
🤖 **Terminal Chat Commands:**

• Just type your message and press Enter to chat
• /help - Show this help message
• /clear - Clear conversation history
• /about - About this bot
• /quit or /exit - Exit the chat

I can help with questions, writing, coding, and more!
    """
    print(help_text)

def show_about():
    """Show about information."""
    about_text = f"""
🤖 **About {BOT_NAME}**

• Powered by Google Gemini 1.5 Flash
• Terminal-based chat interface
• Features: AI chat, context awareness
• Free to use with Gemini API

Built with Python and Google Generative AI
    """
    print(about_text)

async def main():
    """Main chat function."""
    print("🤖 Terminal Chat with Gemini AI")
    print("=" * 40)
    print("🚀 Starting chat...")
    print("💡 Type /help for commands, /quit to exit")
    print("-" * 40)
    
    try:
        while True:
            # Get user input
            user_input = input("You: ").strip()
            
            # Handle commands
            if user_input.lower() in ['/quit', '/exit', 'quit', 'exit']:
                print("👋 Goodbye!")
                break
            elif user_input.lower() == '/help':
                show_help()
                continue
            elif user_input.lower() == '/clear':
                clear_history()
                continue
            elif user_input.lower() == '/about':
                show_about()
                continue
            elif user_input.startswith('/'):
                print("❌ Unknown command. Type /help for available commands.")
                continue
            elif not user_input:
                continue
            
            # Generate AI response
            print("🤖 Thinking...")
            response = await generate_response(user_input)
            print(f"Bot: {response}")
            print("-" * 40)
            
    except KeyboardInterrupt:
        print("\n👋 Chat stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        logger.error(f"Chat error: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Chat stopped by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}") 