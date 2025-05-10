# app/components/chat_interface.py
import streamlit as st
from typing import List, Dict, Any

class ChatInterface:
    def __init__(self):
        if 'messages' not in st.session_state:
            st.session_state.messages = []
    
    def display_chat(self):
        """Display chat messages."""
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    def add_message(self, role: str, content: str):
        """Add a new message to the chat."""
        st.session_state.messages.append({"role": role, "content": content})
    
    def get_user_input(self) -> str:
        """Get user input from chat input."""
        return st.chat_input("Ask a question about your documents")