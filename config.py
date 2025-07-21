import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Gemini API Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Bot Configuration
BOT_NAME = "Gemini Chat Bot"
MAX_MESSAGE_LENGTH = 4096  # Telegram's limit
MAX_HISTORY_LENGTH = 10    # Number of messages to keep in conversation history 