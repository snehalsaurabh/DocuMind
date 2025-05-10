# setup.py
from setuptools import setup, find_packages

setup(
    name="llmchatbot",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'streamlit',
        'PyPDF2',
        'python-docx',
        'sentence-transformers',
        'faiss-cpu',
        'langchain',
        'numpy',
        'python-dotenv',
        'google-generativeai',
        'pyyaml'
    ],
)