#!/usr/bin/env python3
"""
Simple Telegram Bot with Gemini AI
This version uses a minimal approach to avoid version conflicts.
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

async def main():
    """Main bot function."""
    if not TELEGRAM_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN not found in .env file")
        return
    
    if not GEMINI_API_KEY:
        print("❌ GEMINI_API_KEY not found in .env file")
        return
    
    try:
        # Try to import telegram with different approaches
        try:
            from telegram import Bot, Update
            from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
            from telegram.constants import ParseMode
            print("✅ Using python-telegram-bot")
        except ImportError as e:
            print(f"❌ python-telegram-bot import error: {e}")
            return
        
        # Create application directly without builder pattern
        application = Application(token=TELEGRAM_TOKEN)
        
        async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            """Handle /start command."""
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
            await update.message.reply_text(welcome, parse_mode=ParseMode.MARKDOWN)
        
        async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            """Handle /help command."""
            help_text = """
🤖 **Bot Commands:**

• Send any message to chat with me
• /start - Welcome message
• /help - Show this help
• /clear - Clear conversation history
• /about - About this bot

I can help with questions, writing, coding, and more!
            """
            await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)
        
        async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            """Handle /clear command."""
            user_id = update.effective_user.id
            clear_history(user_id)
            await update.message.reply_text("🧹 Conversation history cleared!")
        
        async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            """Handle /about command."""
            about_text = f"""
🤖 **About {BOT_NAME}**

• Powered by Google Gemini 1.5 Flash
• Built with Python and python-telegram-bot
• Features: AI chat, context awareness
• Free to use with Gemini API
            """
            await update.message.reply_text(about_text, parse_mode=ParseMode.MARKDOWN)
        
        async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
            """Handle incoming messages."""
            user_id = update.effective_user.id
            message_text = update.message.text
            
            # Send typing indicator
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
            
            try:
                # Generate response
                response = await generate_response(user_id, message_text)
                
                # Send response
                await update.message.reply_text(response)
                
            except Exception as e:
                logger.error(f"Error: {e}")
                await update.message.reply_text("❌ Sorry, I encountered an error. Please try again.")
        
        # Add handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("clear", clear_command))
        application.add_handler(CommandHandler("about", about_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        print("🚀 Starting bot...")
        print("💡 Press Ctrl+C to stop")
        
        # Start bot with simple polling
        await application.initialize()
        await application.start()
        await application.updater.start_polling()
        
        # Keep running
        try:
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            print("\n👋 Stopping bot...")
            await application.updater.stop()
            await application.stop()
            await application.shutdown()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        logger.error(f"Bot error: {e}")

if __name__ == "__main__":
    print("🤖 Simple Telegram Gemini Bot")
    print("=" * 40)
    asyncio.run(main()) 