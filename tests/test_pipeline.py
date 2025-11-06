"""
Basic tests for Local RAG Pipeline
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rag_pipeline import LocalRAGPipeline, Document


def test_document_creation():
    """Test Document dataclass creation"""
    doc = Document(
        content="Test content",
        metadata={"source": "test.txt"},
        doc_id="test_1"
    )
    assert doc.content == "Test content"
    assert doc.metadata["source"] == "test.txt"
    assert doc.doc_id == "test_1"


def test_pipeline_initialization():
    """Test RAG pipeline initialization"""
    # This test will be skipped in CI due to model downloads
    pytest.skip("Skipping model download test")
    
    rag = LocalRAGPipeline(
        embedding_model="all-MiniLM-L6-v2",
        llm_model="microsoft/phi-2",
        storage_path="./test_storage"
    )
    assert rag.embedding_model is not None
    assert rag.storage_path.exists()


def test_text_splitting():
    """Test document chunking"""
    pytest.skip("Requires pipeline initialization")
    
    rag = LocalRAGPipeline()
    text = "This is a test. " * 100  # Create long text
    chunks = rag.text_splitter.split_text(text)
    assert len(chunks) > 1


def test_document_loading():
    """Test document loading functionality"""
    pytest.skip("Requires test documents")
    
    # Create test document
    test_dir = Path("./test_docs")
    test_dir.mkdir(exist_ok=True)
    test_file = test_dir / "test.txt"
    test_file.write_text("Test document content")
    
    rag = LocalRAGPipeline()
    documents = rag.load_documents(str(test_dir))
    
    assert len(documents) > 0
    assert documents[0].content == "Test document content"
    
    # Cleanup
    test_file.unlink()
    test_dir.rmdir()


def test_vector_index_build():
    """Test vector index building"""
    pytest.skip("Requires pipeline initialization")
    
    rag = LocalRAGPipeline()
    
    # Create test documents
    docs = [
        Document(content="Test 1", metadata={}, doc_id="1"),
        Document(content="Test 2", metadata={}, doc_id="2"),
    ]
    
    rag.build_vector_index(docs)
    assert rag.vector_index is not None


def test_knowledge_graph_build():
    """Test knowledge graph building"""
    pytest.skip("Requires pipeline initialization")
    
    rag = LocalRAGPipeline()
    
    # Create test documents
    docs = [
        Document(content="Python is great", metadata={}, doc_id="1"),
        Document(content="Machine learning uses Python", metadata={}, doc_id="2"),
    ]
    
    rag.build_knowledge_graph(docs)
    assert rag.knowledge_graph.number_of_nodes() > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
