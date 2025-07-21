import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from telegram.constants import ParseMode
import config
from gemini_client import GeminiClient

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize Gemini client
gemini_client = GeminiClient()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    user = update.effective_user
    welcome_message = f"""
🤖 Welcome to {config.BOT_NAME}, {user.first_name}!

I'm powered by Google's Gemini AI and ready to chat with you about anything!

💡 **Available Commands:**
• Just send me a message to start chatting
• `/help` - Show help information
• `/clear` - Clear conversation history
• `/history` - View conversation summary
• `/about` - About this bot

🎯 **Features:**
• AI-powered conversations
• Context-aware responses
• Conversation history management
• Safe and secure

Start chatting now! 🚀
    """
    
    keyboard = [
        [InlineKeyboardButton("💬 Start Chatting", callback_data="start_chat")],
        [InlineKeyboardButton("❓ Help", callback_data="help")],
        [InlineKeyboardButton("ℹ️ About", callback_data="about")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_message,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    help_text = """
🤖 **Bot Commands:**

💬 **Chat Commands:**
• Just send any message to chat with me
• I'll remember our conversation context

🛠️ **Utility Commands:**
• `/start` - Welcome message and main menu
• `/help` - Show this help message
• `/clear` - Clear our conversation history
• `/history` - View conversation summary
• `/about` - Learn more about this bot

💡 **Tips:**
• I can help with questions, creative writing, coding, and more
• Our conversation history helps me provide better responses
• Use `/clear` if you want to start fresh

Need help? Just ask! 😊
    """
    
    await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /clear command."""
    user_id = update.effective_user.id
    gemini_client.clear_conversation(user_id)
    
    await update.message.reply_text(
        "🧹 Conversation history cleared! We're starting fresh. 😊"
    )

async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /history command."""
    user_id = update.effective_user.id
    summary = gemini_client.get_conversation_summary(user_id)
    
    await update.message.reply_text(
        f"📚 **Conversation History:**\n\n{summary}",
        parse_mode=ParseMode.MARKDOWN
    )

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /about command."""
    about_text = """
🤖 **About This Bot**

**Name:** {bot_name}
**AI Model:** Google Gemini 1.5 Flash (Free)
**Features:**
• Advanced AI conversations
• Context-aware responses
• Multi-user support
• Conversation history management

**Technology Stack:**
• Python 3.8+
• python-telegram-bot
• Google Generative AI
• Asynchronous processing

**Capabilities:**
• Answer questions
• Creative writing
• Code assistance
• General conversation
• Problem solving

Built with ❤️ using cutting-edge AI technology!
    """.format(bot_name=config.BOT_NAME)
    
    await update.message.reply_text(about_text, parse_mode=ParseMode.MARKDOWN)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming text messages."""
    user = update.effective_user
    message_text = update.message.text
    user_id = user.id
    
    # Send typing indicator
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # Generate response using Gemini
        response = await gemini_client.generate_response(user_id, message_text)
        
        # Split long responses if needed
        if len(response) > config.MAX_MESSAGE_LENGTH:
            chunks = [response[i:i+config.MAX_MESSAGE_LENGTH] for i in range(0, len(response), config.MAX_MESSAGE_LENGTH)]
            for i, chunk in enumerate(chunks):
                if i == 0:
                    await update.message.reply_text(chunk)
                else:
                    await context.bot.send_message(chat_id=update.effective_chat.id, text=chunk)
        else:
            await update.message.reply_text(response)
            
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        await update.message.reply_text(
            "❌ Sorry, I encountered an error processing your message. Please try again."
        )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline button callbacks."""
    query = update.callback_query
    await query.answer()
    
    if query.data == "start_chat":
        await query.edit_message_text(
            "💬 Great! Just send me a message and I'll respond using Gemini AI. What would you like to chat about?"
        )
    elif query.data == "help":
        await query.edit_message_text(
            "🤖 **Bot Commands:**\n\n"
            "• Send any message to chat\n"
            "• `/help` - Show help\n"
            "• `/clear` - Clear history\n"
            "• `/history` - View history\n"
            "• `/about` - About bot",
            parse_mode=ParseMode.MARKDOWN
        )
    elif query.data == "about":
        await query.edit_message_text(
            f"🤖 **About {config.BOT_NAME}**\n\n"
            "Powered by Google Gemini 1.5 Flash AI\n"
            "Built with Python and python-telegram-bot\n"
            "Features: AI chat, context awareness, multi-user support",
            parse_mode=ParseMode.MARKDOWN
        )

async def main():
    """Main function to run the bot."""
    try:
        if not config.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables")
        
        # Create application
        application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("clear", clear_command))
        application.add_handler(CommandHandler("history", history_command))
        application.add_handler(CommandHandler("about", about_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        application.add_handler(CallbackQueryHandler(button_callback))
        
        logger.info("Starting bot...")
        
        # Start the bot
        await application.run_polling()
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())