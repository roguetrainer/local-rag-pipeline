"""
Interactive CLI for RAG Pipeline
Provides a command-line interface to interact with your documents
"""

import argparse
from pathlib import Path
from rag_pipeline import LocalRAGPipeline
import json


class RAGInterface:
    """Interactive interface for RAG pipeline"""
    
    def __init__(self, storage_path: str = "./my_rag_storage"):
        self.storage_path = storage_path
        self.rag = None
    
    def initialize_new(self, documents_path: str, embedding_model: str, llm_model: str):
        """Initialize a new RAG pipeline"""
        print("\n🚀 Initializing new RAG pipeline...")
        
        self.rag = LocalRAGPipeline(
            embedding_model=embedding_model,
            llm_model=llm_model,
            storage_path=self.storage_path
        )
        
        print(f"\n📂 Loading documents from: {documents_path}")
        documents = self.rag.load_documents(documents_path)
        
        if not documents:
            print("❌ No documents found!")
            return False
        
        print(f"\n✅ Loaded {len(documents)} document chunks")
        
        print("\n🔧 Building vector index...")
        self.rag.build_vector_index(documents)
        
        print("\n🕸️  Building knowledge graph...")
        self.rag.build_knowledge_graph(documents)
        
        print("\n💾 Saving pipeline...")
        self.rag.save()
        
        print("\n✨ Pipeline ready!")
        return True
    
    def load_existing(self, embedding_model: str, llm_model: str):
        """Load an existing RAG pipeline"""
        print("\n📦 Loading existing RAG pipeline...")
        
        self.rag = LocalRAGPipeline(
            embedding_model=embedding_model,
            llm_model=llm_model,
            storage_path=self.storage_path
        )
        
        try:
            self.rag.load()
            print(f"✅ Loaded pipeline with {len(self.rag.documents)} documents")
            return True
        except FileNotFoundError:
            print("❌ No existing pipeline found!")
            return False
    
    def interactive_mode(self):
        """Start interactive query mode"""
        print("\n" + "="*80)
        print("🤖 RAG PIPELINE - INTERACTIVE MODE")
        print("="*80)
        print("\nCommands:")
        print("  - Type your question to get an answer")
        print("  - 'vector' - Switch to vector-only search")
        print("  - 'graph' - Switch to graph-only search")
        print("  - 'hybrid' - Switch to hybrid search (default)")
        print("  - 'stats' - Show pipeline statistics")
        print("  - 'quit' or 'exit' - Exit the program")
        print("="*80 + "\n")
        
        search_type = "hybrid"
        
        while True:
            try:
                user_input = input(f"\n[{search_type.upper()}] 💬 You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye!")
                    break
                
                elif user_input.lower() == 'vector':
                    search_type = "vector"
                    print("✅ Switched to vector search mode")
                    continue
                
                elif user_input.lower() == 'graph':
                    search_type = "graph"
                    print("✅ Switched to graph search mode")
                    continue
                
                elif user_input.lower() == 'hybrid':
                    search_type = "hybrid"
                    print("✅ Switched to hybrid search mode")
                    continue
                
                elif user_input.lower() == 'stats':
                    self.show_stats()
                    continue
                
                # Process query
                print("\n🔍 Searching...")
                result = self.rag.query(user_input, search_type=search_type, top_k=5)
                
                print("\n" + "="*80)
                print("🤖 Answer:")
                print("="*80)
                print(f"\n{result['answer']}\n")
                
                print("="*80)
                print("📚 Sources:")
                print("="*80)
                for i, doc in enumerate(result['retrieved_documents'][:3], 1):
                    print(f"\n{i}. {doc['metadata'].get('source', 'Unknown')}")
                    print(f"   {doc['content'][:150]}...")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
    
    def show_stats(self):
        """Display pipeline statistics"""
        print("\n" + "="*80)
        print("📊 PIPELINE STATISTICS")
        print("="*80)
        print(f"Total documents: {len(self.rag.documents)}")
        print(f"Knowledge graph nodes: {self.rag.knowledge_graph.number_of_nodes()}")
        print(f"Knowledge graph edges: {self.rag.knowledge_graph.number_of_edges()}")
        print(f"Vector index dimension: {self.rag.embedding_dim}")
        print("="*80)
    
    def single_query(self, question: str, search_type: str = "hybrid"):
        """Process a single query and return result"""
        result = self.rag.query(question, search_type=search_type, top_k=5)
        
        print("\n" + "="*80)
        print("QUESTION:", result['question'])
        print("="*80)
        print("\nANSWER:", result['answer'])
        print("\n" + "="*80)
        print("RETRIEVED DOCUMENTS:")
        for i, doc in enumerate(result['retrieved_documents'], 1):
            print(f"\n{i}. Source: {doc['metadata'].get('source', 'Unknown')}")
            print(f"   Content: {doc['content'][:200]}...")
        
        return result


def main():
    parser = argparse.ArgumentParser(description="Local RAG Pipeline Interface")
    
    parser.add_argument(
        '--documents',
        type=str,
        help='Path to documents directory (for initialization)'
    )
    
    parser.add_argument(
        '--storage',
        type=str,
        default='./my_rag_storage',
        help='Path to storage directory (default: ./my_rag_storage)'
    )
    
    parser.add_argument(
        '--embedding-model',
        type=str,
        default='all-MiniLM-L6-v2',
        help='Embedding model name (default: all-MiniLM-L6-v2)'
    )
    
    parser.add_argument(
        '--llm-model',
        type=str,
        default='microsoft/phi-2',
        help='LLM model name (default: microsoft/phi-2)'
    )
    
    parser.add_argument(
        '--query',
        type=str,
        help='Single query to process (non-interactive mode)'
    )
    
    parser.add_argument(
        '--search-type',
        type=str,
        choices=['vector', 'graph', 'hybrid'],
        default='hybrid',
        help='Search type (default: hybrid)'
    )
    
    parser.add_argument(
        '--force-init',
        action='store_true',
        help='Force reinitialization even if storage exists'
    )
    
    args = parser.parse_args()
    
    interface = RAGInterface(storage_path=args.storage)
    
    # Check if we need to initialize or load
    storage_exists = Path(args.storage).exists() and (Path(args.storage) / "documents.pkl").exists()
    
    if args.documents or args.force_init or not storage_exists:
        if not args.documents:
            print("❌ Error: --documents path required for initialization")
            return
        
        success = interface.initialize_new(
            args.documents,
            args.embedding_model,
            args.llm_model
        )
        if not success:
            return
    else:
        success = interface.load_existing(
            args.embedding_model,
            args.llm_model
        )
        if not success:
            return
    
    # Run query or interactive mode
    if args.query:
        interface.single_query(args.query, args.search_type)
    else:
        interface.interactive_mode()


if __name__ == "__main__":
    main()
