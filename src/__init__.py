"""
Local RAG Pipeline

A production-ready RAG system combining vector search and knowledge graphs.
"""

__version__ = "1.0.0"
__author__ = "Local RAG Pipeline Contributors"
__license__ = "MIT"

from .rag_pipeline import LocalRAGPipeline, Document

__all__ = ["LocalRAGPipeline", "Document"]
