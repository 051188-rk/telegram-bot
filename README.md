# 🤖 Telegram Bot with Gemini AI

A powerful Telegram bot powered by Google's Gemini AI for intelligent text conversations. This bot provides context-aware responses, conversation history management, and a user-friendly interface.

## ✨ Features

- **AI-Powered Conversations**: Powered by Google Gemini 1.5 Flash (Free)
- **Context Awareness**: Remembers conversation history for better responses
- **Multi-User Support**: Handles multiple users simultaneously
- **Conversation Management**: Clear history and view conversation summaries
- **Interactive UI**: Inline buttons and rich formatting
- **Error Handling**: Robust error handling and user feedback
- **Asynchronous Processing**: Fast and responsive
- **Free API Usage**: Works with free Gemini API keys

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- Google Gemini API Key (from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd telegram-gemini-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. **Run the bot**
   ```bash
   python bot.py
   ```

## 🔧 Setup Guide

### Getting Telegram Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the bot token provided

### Getting Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key

## 📱 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message and main menu |
| `/help` | Show help information |
| `/clear` | Clear conversation history |
| `/history` | View conversation summary |
| `/about` | About this bot |

## 💬 Usage

1. **Start the bot**: Send `/start` to get the welcome message
2. **Start chatting**: Send any message to begin a conversation
3. **Manage history**: Use `/clear` to reset or `/history` to view
4. **Get help**: Use `/help` for command information

## 🏗️ Project Structure

```
telegram-gemini-bot/
├── bot.py              # Main bot application
├── gemini_client.py    # Gemini API client
├── config.py           # Configuration and environment variables
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🔧 Configuration

You can customize the bot behavior by modifying `config.py`:

- `BOT_NAME`: The name of your bot
- `MAX_MESSAGE_LENGTH`: Maximum message length (Telegram limit: 4096)
- `MAX_HISTORY_LENGTH`: Number of messages to keep in conversation history

## 🛠️ Development

### Adding New Features

1. **New Commands**: Add handlers in `bot.py`
2. **AI Enhancements**: Modify `gemini_client.py`
3. **Configuration**: Update `config.py`

### Error Handling

The bot includes comprehensive error handling:
- API errors are caught and user-friendly messages are sent
- Logging is configured for debugging
- Graceful shutdown on interruption

## 🔒 Security

- API keys are stored in environment variables
- No sensitive data is logged
- User conversations are kept in memory only
- Input validation and sanitization

## 📊 Logging

The bot logs important events:
- Bot startup and shutdown
- Message processing
- API errors
- User interactions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter issues:

1. Check that all API keys are correctly set
2. Ensure Python 3.8+ is installed
3. Verify all dependencies are installed
4. Check the logs for error messages

## 🎯 Future Enhancements

- [ ] Image generation support
- [ ] Voice message processing
- [ ] Multi-language support
- [ ] Conversation export
- [ ] User preferences
- [ ] Rate limiting
- [ ] Database storage for conversations

---

**Built with ❤️ using Python, Telegram Bot API, and Google Gemini AI (Free)** 