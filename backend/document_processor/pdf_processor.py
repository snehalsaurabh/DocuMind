# backend/document_processor/pdf_processor.py
import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter
import docx
import os
from typing import List, Dict, Any
import logging
from backend.document_processor.text_processor import clean_text

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
    
    def process_pdf(self, file_path: str) -> List[Dict[str, Any]]:
        """Process PDF files and return chunks with metadata."""
        try:
            logger.info(f"Processing PDF: {file_path}")
            reader = PyPDF2.PdfReader(file_path)
            chunks = []
            
            for page_num, page in enumerate(reader.pages):
                text = clean_text(page.extract_text())
                if text.strip():
                    page_chunks = self.text_splitter.split_text(text)
                    for chunk in page_chunks:
                        chunks.append({
                            'text': chunk,
                            'metadata': {
                                'source': os.path.basename(file_path),
                                'page': page_num + 1,
                                'type': 'pdf'
                            }
                        })
            
            logger.info(f"Successfully processed PDF: {file_path}")
            return chunks
        except Exception as e:
            logger.error(f"Error processing PDF {file_path}: {str(e)}")
            raise

    def process_docx(self, file_path: str) -> List[Dict[str, Any]]:
        """Process DOCX files and return chunks with metadata."""
        try:
            logger.info(f"Processing DOCX: {file_path}")
            doc = docx.Document(file_path)
            text = clean_text("\n".join([paragraph.text for paragraph in doc.paragraphs]))
            chunks = self.text_splitter.split_text(text)
            
            return [{
                'text': chunk,
                'metadata': {
                    'source': os.path.basename(file_path),
                    'type': 'docx'
                }
            } for chunk in chunks]
        except Exception as e:
            logger.error(f"Error processing DOCX {file_path}: {str(e)}")
            raise

    def process_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Process any supported file type."""
        try:
            logger.info(f"Processing file: {file_path}")
            file_extension = os.path.splitext(file_path)[1].lower()
            
            if file_extension == '.pdf':
                return self.process_pdf(file_path)
            elif file_extension == '.docx':
                return self.process_docx(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_extension}")
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {str(e)}")
            raise