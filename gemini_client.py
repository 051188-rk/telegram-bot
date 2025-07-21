import google.generativeai as genai
from typing import List, Dict, Optional
import config

class GeminiClient:
    def __init__(self):
        """Initialize the Gemini client with API key."""
        if not config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.conversations: Dict[int, List[Dict]] = {}
    
    def add_message_to_history(self, user_id: int, role: str, content: str):
        """Add a message to the conversation history for a specific user."""
        if user_id not in self.conversations:
            self.conversations[user_id] = []
        
        self.conversations[user_id].append({
            'role': role,
            'content': content
        })
        
        # Keep only the last MAX_HISTORY_LENGTH messages
        if len(self.conversations[user_id]) > config.MAX_HISTORY_LENGTH * 2:
            self.conversations[user_id] = self.conversations[user_id][-config.MAX_HISTORY_LENGTH * 2:]
    
    def clear_conversation(self, user_id: int):
        """Clear conversation history for a specific user."""
        if user_id in self.conversations:
            self.conversations[user_id] = []
    
    async def generate_response(self, user_id: int, message: str) -> str:
        """Generate a response using Gemini API."""
        try:
            # Add user message to history
            self.add_message_to_history(user_id, 'user', message)
            
            # Get conversation history
            history = self.conversations.get(user_id, [])
            
            # Create chat session
            chat = self.model.start_chat(history=history[:-1] if history else [])
            
            # Generate response
            response = await chat.send_message_async(message)
            
            # Add bot response to history
            self.add_message_to_history(user_id, 'model', response.text)
            
            return response.text
            
        except Exception as e:
            error_message = f"Sorry, I encountered an error: {str(e)}"
            print(f"Gemini API Error: {e}")
            return error_message
    
    def get_conversation_summary(self, user_id: int) -> str:
        """Get a summary of the current conversation."""
        if user_id not in self.conversations or not self.conversations[user_id]:
            return "No conversation history."
        
        messages = self.conversations[user_id]
        summary = f"Conversation has {len(messages)} messages:\n"
        
        for i, msg in enumerate(messages[-5:], 1):  # Show last 5 messages
            role = "You" if msg['role'] == 'user' else "Bot"
            content = msg['content'][:50] + "..." if len(msg['content']) > 50 else msg['content']
            summary += f"{i}. {role}: {content}\n"
        
        return summary 