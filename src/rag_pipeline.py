"""
Local RAG Pipeline with Vector + Graph Search
Combines semantic search with knowledge graph relationships for enhanced retrieval
"""

import os
import json
import pickle
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
import numpy as np
from collections import defaultdict

# Document processing
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    TextLoader,
    PDFMinerLoader,
    Docx2txtLoader,
    UnstructuredMarkdownLoader,
    CSVLoader,
)

# Embeddings (local)
from sentence_transformers import SentenceTransformer

# Vector store
import faiss

# Graph database
import networkx as nx

# LLM (local)
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch


@dataclass
class Document:
    """Document representation"""

    content: str
    metadata: Dict[str, Any]
    embedding: Optional[np.ndarray] = None
    doc_id: str = ""


class LocalRAGPipeline:
    """
    Local RAG pipeline combining vector search and graph-based retrieval
    """

    def __init__(
        self,
        embedding_model: str = "all-MiniLM-L6-v2",
        llm_model: str = "microsoft/phi-2",
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        storage_path: str = "./rag_storage",
    ):
        """
        Initialize the RAG pipeline

        Args:
            embedding_model: HuggingFace model for embeddings
            llm_model: HuggingFace model for generation
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
            storage_path: Path to store indices and graphs
        """
        print("Initializing RAG Pipeline...")

        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)

        # Initialize embedding model
        print(f"Loading embedding model: {embedding_model}")
        self.embedding_model = SentenceTransformer(embedding_model)
        self.embedding_dim = self.embedding_model.get_sentence_embedding_dimension()

        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

        # Initialize vector store (FAISS)
        self.vector_index = None
        self.documents: List[Document] = []

        # Initialize knowledge graph
        self.knowledge_graph = nx.DiGraph()

        # Initialize LLM
        print(f"Loading LLM: {llm_model}")
        self.tokenizer = AutoTokenizer.from_pretrained(
            llm_model, trust_remote_code=True
        )
        self.llm = AutoModelForCausalLM.from_pretrained(
            llm_model,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto" if torch.cuda.is_available() else None,
            trust_remote_code=True,
        )

        # Set padding token if not set
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        print("RAG Pipeline initialized successfully!")

    def load_documents(self, document_path: str) -> List[Document]:
        """
        Load documents from a directory or file

        Args:
            document_path: Path to documents

        Returns:
            List of loaded documents
        """
        path = Path(document_path)
        documents = []

        if path.is_file():
            docs = self._load_single_file(path)
            documents.extend(docs)
        elif path.is_dir():
            for file_path in path.rglob("*"):
                if file_path.is_file():
                    try:
                        docs = self._load_single_file(file_path)
                        documents.extend(docs)
                    except Exception as e:
                        print(f"Error loading {file_path}: {e}")

        print(f"Loaded {len(documents)} document chunks")
        return documents

    def _load_single_file(self, file_path: Path) -> List[Document]:
        """Load a single file based on extension"""
        extension = file_path.suffix.lower()

        loaders = {
            ".txt": TextLoader,
            ".pdf": PDFMinerLoader,
            ".docx": Docx2txtLoader,
            ".md": UnstructuredMarkdownLoader,
            ".csv": CSVLoader,
        }

        if extension not in loaders:
            return []

        try:
            loader = loaders[extension](str(file_path))
            raw_docs = loader.load()

            # Split into chunks
            chunks = []
            for doc in raw_docs:
                splits = self.text_splitter.split_text(doc.page_content)
                for i, split in enumerate(splits):
                    chunks.append(
                        Document(
                            content=split,
                            metadata={
                                "source": str(file_path),
                                "chunk_id": i,
                                "total_chunks": len(splits),
                            },
                            doc_id=f"{file_path.stem}_{i}",
                        )
                    )

            return chunks
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return []

    def build_vector_index(self, documents: List[Document]):
        """
        Build FAISS vector index from documents

        Args:
            documents: List of documents to index
        """
        print("Building vector index...")

        self.documents = documents

        # Generate embeddings
        texts = [doc.content for doc in documents]
        embeddings = self.embedding_model.encode(
            texts, show_progress_bar=True, batch_size=32
        )

        # Store embeddings in documents
        for doc, emb in zip(documents, embeddings):
            doc.embedding = emb

        # Create FAISS index
        self.vector_index = faiss.IndexFlatL2(self.embedding_dim)
        self.vector_index.add(embeddings.astype("float32"))

        print(f"Vector index built with {len(documents)} documents")

    def build_knowledge_graph(self, documents: List[Document]):
        """
        Build knowledge graph from documents
        Extracts entities and relationships

        Args:
            documents: List of documents
        """
        print("Building knowledge graph...")

        # Simple entity extraction (can be enhanced with NER)
        for doc in documents:
            # Add document as a node
            self.knowledge_graph.add_node(
                doc.doc_id,
                content=doc.content[:200],  # Store preview
                type="document",
                metadata=doc.metadata,
            )

            # Extract simple co-occurrence relationships
            # In production, use NER and relation extraction
            words = doc.content.split()
            entities = [w for w in words if len(w) > 5 and w[0].isupper()]

            # Add entities and relationships
            for entity in set(entities):
                if not self.knowledge_graph.has_node(entity):
                    self.knowledge_graph.add_node(entity, type="entity")

                self.knowledge_graph.add_edge(doc.doc_id, entity, relation="contains")

            # Link documents with same source
            for other_doc in documents:
                if doc.doc_id != other_doc.doc_id and doc.metadata.get(
                    "source"
                ) == other_doc.metadata.get("source"):
                    self.knowledge_graph.add_edge(
                        doc.doc_id, other_doc.doc_id, relation="same_source"
                    )

        print(
            f"Knowledge graph built with {self.knowledge_graph.number_of_nodes()} nodes "
            f"and {self.knowledge_graph.number_of_edges()} edges"
        )

    def vector_search(self, query: str, top_k: int = 5) -> List[Tuple[Document, float]]:
        """
        Perform vector similarity search

        Args:
            query: Query string
            top_k: Number of results to return

        Returns:
            List of (document, score) tuples
        """
        if self.vector_index is None:
            raise ValueError("Vector index not built. Call build_vector_index first.")

        # Encode query
        query_embedding = self.embedding_model.encode([query])[0]

        # Search
        distances, indices = self.vector_index.search(
            query_embedding.reshape(1, -1).astype("float32"), top_k
        )

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.documents):
                results.append((self.documents[idx], float(dist)))

        return results

    def graph_search(self, query: str, top_k: int = 5) -> List[Document]:
        """
        Perform graph-based search
        Uses graph structure to find relevant documents

        Args:
            query: Query string
            top_k: Number of results to return

        Returns:
            List of relevant documents
        """
        # First, find relevant entities in query
        query_words = query.split()
        query_entities = [w for w in query_words if len(w) > 3]

        # Find nodes related to query entities
        relevant_nodes = set()
        for entity in query_entities:
            if self.knowledge_graph.has_node(entity):
                # Add the entity itself
                relevant_nodes.add(entity)
                # Add neighbors
                relevant_nodes.update(self.knowledge_graph.neighbors(entity))

        # Score documents by graph connectivity
        doc_scores = defaultdict(float)
        for node in relevant_nodes:
            if self.knowledge_graph.nodes[node].get("type") == "document":
                # Score based on centrality and connections
                doc_scores[node] = (
                    self.knowledge_graph.degree(node) * 0.5
                    + nx.pagerank(self.knowledge_graph).get(node, 0) * 0.5
                )

        # Get top documents
        top_doc_ids = sorted(
            doc_scores.keys(), key=lambda x: doc_scores[x], reverse=True
        )[:top_k]

        # Return document objects
        doc_map = {doc.doc_id: doc for doc in self.documents}
        return [doc_map[doc_id] for doc_id in top_doc_ids if doc_id in doc_map]

    def hybrid_search(
        self,
        query: str,
        top_k: int = 5,
        vector_weight: float = 0.7,
        graph_weight: float = 0.3,
    ) -> List[Document]:
        """
        Combine vector and graph search with weighted scoring

        Args:
            query: Query string
            top_k: Number of results to return
            vector_weight: Weight for vector search
            graph_weight: Weight for graph search

        Returns:
            List of top documents
        """
        # Vector search results
        vector_results = self.vector_search(query, top_k * 2)
        vector_scores = {doc.doc_id: (1 / (1 + score)) for doc, score in vector_results}

        # Graph search results
        graph_results = self.graph_search(query, top_k * 2)
        graph_scores = {
            doc.doc_id: 1.0 / (i + 1) for i, doc in enumerate(graph_results)
        }

        # Combine scores
        all_doc_ids = set(vector_scores.keys()) | set(graph_scores.keys())
        combined_scores = {}

        for doc_id in all_doc_ids:
            v_score = vector_scores.get(doc_id, 0)
            g_score = graph_scores.get(doc_id, 0)
            combined_scores[doc_id] = vector_weight * v_score + graph_weight * g_score

        # Get top documents
        top_doc_ids = sorted(
            combined_scores.keys(), key=lambda x: combined_scores[x], reverse=True
        )[:top_k]

        doc_map = {doc.doc_id: doc for doc in self.documents}
        return [doc_map[doc_id] for doc_id in top_doc_ids if doc_id in doc_map]

    def generate_answer(
        self, query: str, context_docs: List[Document], max_length: int = 200
    ) -> str:
        """
        Generate answer using retrieved context

        Args:
            query: User query
            context_docs: Retrieved documents for context
            max_length: Maximum length of generated answer

        Returns:
            Generated answer
        """
        # Prepare context
        context = "\n\n".join(
            [
                f"Document {i + 1}: {doc.content}"
                for i, doc in enumerate(context_docs[:3])  # Use top 3 docs
            ]
        )

        # Create prompt
        prompt = f"""Based on the following context, answer the question.

Context:
{context}

Question: {query}

Answer:"""

        # Generate
        inputs = self.tokenizer(
            prompt, return_tensors="pt", truncation=True, max_length=1024
        )
        if torch.cuda.is_available():
            inputs = {k: v.cuda() for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.llm.generate(
                **inputs,
                max_new_tokens=max_length,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
            )

        answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Extract just the answer part
        if "Answer:" in answer:
            answer = answer.split("Answer:")[-1].strip()

        return answer

    def query(
        self, question: str, search_type: str = "hybrid", top_k: int = 5
    ) -> Dict[str, Any]:
        """
        Main query interface

        Args:
            question: User question
            search_type: Type of search ('vector', 'graph', or 'hybrid')
            top_k: Number of documents to retrieve

        Returns:
            Dictionary with answer and retrieved documents
        """
        # Retrieve documents
        if search_type == "vector":
            results = self.vector_search(question, top_k)
            retrieved_docs = [doc for doc, _ in results]
        elif search_type == "graph":
            retrieved_docs = self.graph_search(question, top_k)
        else:  # hybrid
            retrieved_docs = self.hybrid_search(question, top_k)

        # Generate answer
        answer = self.generate_answer(question, retrieved_docs)

        return {
            "question": question,
            "answer": answer,
            "retrieved_documents": [
                {"content": doc.content, "metadata": doc.metadata, "doc_id": doc.doc_id}
                for doc in retrieved_docs
            ],
            "search_type": search_type,
        }

    def save(self):
        """Save the RAG pipeline to disk"""
        print("Saving RAG pipeline...")

        # Save documents
        with open(self.storage_path / "documents.pkl", "wb") as f:
            pickle.dump(self.documents, f)

        # Save vector index
        if self.vector_index is not None:
            faiss.write_index(
                self.vector_index, str(self.storage_path / "vector_index.faiss")
            )

        # Save knowledge graph
        nx.write_gpickle(
            self.knowledge_graph, self.storage_path / "knowledge_graph.gpickle"
        )

        print(f"Pipeline saved to {self.storage_path}")

    def load(self):
        """Load the RAG pipeline from disk"""
        print("Loading RAG pipeline...")

        # Load documents
        with open(self.storage_path / "documents.pkl", "rb") as f:
            self.documents = pickle.load(f)

        # Load vector index
        if (self.storage_path / "vector_index.faiss").exists():
            self.vector_index = faiss.read_index(
                str(self.storage_path / "vector_index.faiss")
            )

        # Load knowledge graph
        if (self.storage_path / "knowledge_graph.gpickle").exists():
            self.knowledge_graph = nx.read_gpickle(
                self.storage_path / "knowledge_graph.gpickle"
            )

        print(f"Pipeline loaded from {self.storage_path}")


def main():
    """Example usage"""
    # Initialize pipeline
    rag = LocalRAGPipeline(
        embedding_model="all-MiniLM-L6-v2",
        llm_model="microsoft/phi-2",  # Lightweight model
        storage_path="./my_rag_storage",
    )

    # Load and process documents
    documents = rag.load_documents("./my_documents")  # Point to your document folder

    # Build indices
    rag.build_vector_index(documents)
    rag.build_knowledge_graph(documents)

    # Save for later use
    rag.save()

    # Query the system
    result = rag.query(
        "What are the main topics discussed in the documents?",
        search_type="hybrid",
        top_k=5,
    )

    print("\n" + "=" * 80)
    print("QUESTION:", result["question"])
    print("=" * 80)
    print("\nANSWER:", result["answer"])
    print("\n" + "=" * 80)
    print("RETRIEVED DOCUMENTS:")
    for i, doc in enumerate(result["retrieved_documents"], 1):
        print(f"\n{i}. Source: {doc['metadata'].get('source', 'Unknown')}")
        print(f"   Content: {doc['content'][:200]}...")


if __name__ == "__main__":
    main()
