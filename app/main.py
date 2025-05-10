# app/main.py
import torch
torch.set_num_threads(1)

import streamlit as st
import os
import logging
from backend.document_processor.pdf_processor import DocumentProcessor
from backend.embeddings.embedding_manager import EmbeddingManager
from backend.llm.chat_manager import ChatManager
from app.components.file_uploader import FileUploader
from app.components.chat_interface import ChatInterface

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        # Initialize components
        document_processor = DocumentProcessor()
        embedding_manager = EmbeddingManager()
        chat_manager = ChatManager()
        file_uploader = FileUploader()
        chat_interface = ChatInterface()

        # Header
        st.title("📚 Document Q&A Chatbot")
        st.markdown("Upload your documents and ask questions about their content!")

        # Sidebar
        with st.sidebar:
            st.header("📄 Document Upload")
            st.markdown("Upload your PDF or DOCX files here.")
            
            # File upload
            saved_files = file_uploader.upload_files()
            
            if saved_files:
                with st.spinner("Processing documents..."):
                    for file_path in saved_files:
                        try:
                            chunks = document_processor.process_file(file_path)
                            if chunks:
                                embedding_manager.create_embeddings(chunks)
                                st.success(f"Processed {os.path.basename(file_path)}")
                            else:
                                st.warning(f"No content extracted from {os.path.basename(file_path)}")
                        except Exception as e:
                            st.error(f"Error processing {os.path.basename(file_path)}: {str(e)}")
                        finally:
                            # Clean up temporary file
                            if os.path.exists(file_path):
                                os.unlink(file_path)

        # Main chat interface
        st.header("💬 Chat")
        
        # Display chat history
        chat_interface.display_chat()
        
        # Get user input
        if question := chat_interface.get_user_input():
            # Add user message to chat
            chat_interface.add_message("user", question)
            
            # Get relevant context
            with st.spinner("Searching for relevant information..."):
                relevant_chunks = embedding_manager.search(question)
            
            if not relevant_chunks:
                st.warning("No relevant information found in the documents.")
                chat_interface.add_message("assistant", "I couldn't find any relevant information in the documents to answer your question.")
            else:
                # Generate response
                with st.spinner("Generating response..."):
                    response = chat_manager.generate_response(question, relevant_chunks)
                
                # Add assistant message to chat
                chat_interface.add_message("assistant", response)
                
                # Display sources
                with st.expander("View Sources"):
                    for chunk in relevant_chunks:
                        st.markdown(f"""
                        **Source:** {chunk['metadata']['source']}  
                        **Page:** {chunk['metadata'].get('page', 'N/A')}  
                        **Relevance:** {chunk['relevance_score']:.2f}
                        """)
                        st.markdown(chunk['text'])
                        st.markdown("---")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        logger.error(f"Application error: {str(e)}")

if __name__ == "__main__":
    main()