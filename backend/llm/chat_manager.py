# backend/llm/chat_manager.py
import google.generativeai as genai
from typing import List, Dict, Any
import os
from dotenv import load_dotenv
import yaml
import logging
from backend.llm.prompt_template import build_prompt

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class ChatManager:
    def __init__(self):
        try:
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                raise ValueError("GEMINI_API_KEY not found in environment variables")
            
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('models/gemini-1.5-pro')
            self.chat = self.model.start_chat(history=[])
            logger.info("Chat manager initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing chat manager: {str(e)}")
            raise

    def generate_response(self, question: str, context_chunks: List[Dict[str, Any]]) -> str:
        try:
            if not context_chunks:
                logger.warning("No context chunks provided for response generation")
                return "I couldn't find any relevant information in the documents to answer your question."

            logger.info(f"Generating response for question: {question}")
            context = "\n\n".join([
                f"Source: {chunk['metadata']['source']}\n"
                f"Page: {chunk['metadata'].get('page', 'N/A')}\n"
                f"Content: {chunk['text']}"
                for chunk in context_chunks
            ])
            
            prompt = build_prompt(context, question)
            response = self.chat.send_message(prompt)
            
            logger.info("Response generated successfully")
            return response.text
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return f"I encountered an error while generating the response: {str(e)}"