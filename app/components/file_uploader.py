# app/components/file_uploader.py
import streamlit as st
import os
from typing import List
import tempfile

class FileUploader:
    def __init__(self):
        self.supported_types = {
            'pdf': 'application/pdf',
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        }
    
    def upload_files(self) -> List[str]:
        """Handle file uploads and return list of saved file paths."""
        uploaded_files = st.file_uploader(
            "Upload Documents",
            type=list(self.supported_types.keys()),
            accept_multiple_files=True
        )
        
        if not uploaded_files:
            return []
        
        saved_files = []
        for uploaded_file in uploaded_files:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                saved_files.append(tmp_file.name)
        
        return saved_files