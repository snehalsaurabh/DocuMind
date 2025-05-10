# backend/embeddings/embedding_manager.py
import os
import logging
from sentence_transformers import SentenceTransformer
import numpy as np
import pickle
import yaml
from backend.embeddings.vector_store import VectorStore

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmbeddingManager:
    def __init__(self, model_name: str = None):
        try:
            self.model_name = model_name or 'sentence-transformers/all-MiniLM-L6-v2'
            logger.info(f"Initializing embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            self.dimension = self.model.get_sentence_embedding_dimension()
            
            # Ensure directories exist
            os.makedirs("data/processed", exist_ok=True)
            
            self.vector_store = VectorStore(self.dimension, "data/processed/faiss_index.bin")
            self.chunks = []
            self.embeddings_file = "data/processed/embeddings.pkl"
            self._load_embeddings()
            logger.info("Embedding manager initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing embedding manager: {str(e)}")
            raise

    def _load_embeddings(self):
        """Load existing embeddings and chunks if available."""
        try:
            if os.path.exists(self.embeddings_file):
                logger.info(f"Loading existing embeddings from {self.embeddings_file}")
                with open(self.embeddings_file, 'rb') as f:
                    self.chunks = pickle.load(f)
                logger.info(f"Loaded {len(self.chunks)} chunks")
            else:
                logger.info("No existing embeddings found")
                self.chunks = []
        except Exception as e:
            logger.error(f"Error loading embeddings: {str(e)}")
            self.chunks = []

    def _save_embeddings(self):
        """Save chunks to disk."""
        try:
            logger.info(f"Saving {len(self.chunks)} chunks to {self.embeddings_file}")
            with open(self.embeddings_file, 'wb') as f:
                pickle.dump(self.chunks, f)
            logger.info("Embeddings saved successfully")
        except Exception as e:
            logger.error(f"Error saving embeddings: {str(e)}")
            raise

    def create_embeddings(self, chunks):
        try:
            if not chunks:
                logger.warning("No chunks provided for embedding")
                return
            
            logger.info(f"Creating embeddings for {len(chunks)} chunks")
            texts = [chunk['text'] for chunk in chunks]
            
            # Process in smaller batches to avoid memory issues
            batch_size = 32
            all_embeddings = []
            
            for i in range(0, len(texts), batch_size):
                batch_texts = texts[i:i + batch_size]
                batch_embeddings = self.model.encode(batch_texts)
                all_embeddings.extend(batch_embeddings)
            
            embeddings_array = np.array(all_embeddings)
            self.vector_store.add(embeddings_array)
            self.chunks.extend(chunks)
            self._save_embeddings()
            logger.info("Embeddings created and saved successfully")
        except Exception as e:
            logger.error(f"Error creating embeddings: {str(e)}")
            raise

    def search(self, query, k=5):
        try:
            logger.info(f"Searching for query: {query}")
            query_embedding = self.model.encode([query])
            distances, indices = self.vector_store.search(np.array(query_embedding), k)
            
            results = []
            for i, idx in enumerate(indices[0]):
                if idx < len(self.chunks):
                    result = self.chunks[idx].copy()
                    result['relevance_score'] = float(1 / (1 + distances[0][i]))
                    results.append(result)
            
            logger.info(f"Found {len(results)} relevant chunks")
            return results
        except Exception as e:
            logger.error(f"Error during search: {str(e)}")
            return []

    def clear_embeddings(self):
        """Clear all stored embeddings and chunks."""
        try:
            self.chunks = []
            if os.path.exists(self.embeddings_file):
                os.remove(self.embeddings_file)
            if os.path.exists(self.vector_store.index_path):
                os.remove(self.vector_store.index_path)
            logger.info("Embeddings cleared successfully")
        except Exception as e:
            logger.error(f"Error clearing embeddings: {str(e)}")
            raise