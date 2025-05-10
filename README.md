# DocuMind 📚

A powerful document Q&A system that processes multiple large documents and provides intelligent responses using advanced AI technology.

## 🌟 Features

- **Multi-Document Processing**: Handle multiple PDF and DOCX files simultaneously
- **Advanced Embedding System**: Uses state-of-the-art sentence transformers for semantic search
- **Intelligent Q&A**: Powered by Google's Gemini 1.5 Pro model for accurate responses
- **Context-Aware**: Maintains document context and provides source citations
- **User-Friendly Interface**: Clean and intuitive Streamlit-based UI
- **Efficient Storage**: FAISS-based vector storage for quick retrieval
- **Scalable Architecture**: Modular design for easy extension and maintenance

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package installer)
- Google Cloud API key for Gemini

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/DocuMind.git
cd DocuMind
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory:
```bash
GOOGLE_API_KEY=<your_google_api_key>
```

5. Run the application:
```bash
streamlit run app/main.py
```


## 💡 Usage

1. **Upload Documents**:
   - Use the sidebar to upload PDF or DOCX files
   - Multiple files can be uploaded simultaneously
   - Wait for processing to complete

2. **Ask Questions**:
   - Type your question in the chat interface
   - The system will search through all documents
   - Get answers with source citations

3. **View Sources**:
   - Click on the "View Sources" expander
   - See which documents contributed to the answer
   - Check relevance scores and page numbers

## 🔧 Configuration

The `config.yaml` file allows you to customize:
- Embedding model settings
- Chunk size and overlap
- Vector store parameters
- Supported file types
- Retrieval settings

## ��️ Technical Details

### Key Technologies

- **Streamlit**: Web interface
- **Sentence Transformers**: Document embeddings
- **FAISS**: Vector similarity search
- **Gemini 1.5 Pro**: LLM for response generation
- **PyPDF2 & python-docx**: Document processing

### Performance Considerations

- Documents are processed in chunks for memory efficiency
- Embeddings are cached for faster subsequent queries
- Vector search is optimized for quick retrieval
- Batch processing for large documents

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


