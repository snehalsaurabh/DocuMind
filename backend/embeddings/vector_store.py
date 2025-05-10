# backend/embeddings/vector_store.py
import faiss
import numpy as np
import os
import logging

os.makedirs("data/processed", exist_ok=True)
logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, dimension: int, index_path: str):
        self.index_path = index_path
        try:
            if os.path.exists(index_path):
                logger.info(f"Loading existing FAISS index from {index_path}")
                self.index = faiss.read_index(index_path)
            else:
                logger.info(f"Creating new FAISS index with dimension {dimension}")
                self.index = faiss.IndexFlatL2(dimension)
        except Exception as e:
            logger.error(f"Error initializing vector store: {str(e)}")
            self.index = faiss.IndexFlatL2(dimension)

    def add(self, embeddings: np.ndarray):
        try:
            self.index.add(embeddings.astype('float32'))
            self.save()
        except Exception as e:
            logger.error(f"Error adding embeddings to vector store: {str(e)}")
            raise

    def search(self, query_embedding: np.ndarray, k: int = 5):
        try:
            return self.index.search(query_embedding.astype('float32'), k)
        except Exception as e:
            logger.error(f"Error searching vector store: {str(e)}")
            raise

    def save(self):
        try:
            faiss.write_index(self.index, self.index_path)
        except Exception as e:
            logger.error(f"Error saving vector store: {str(e)}")
            raise