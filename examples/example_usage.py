"""
Example usage of the RAG Pipeline
This script demonstrates basic operations
"""

from rag_pipeline import LocalRAGPipeline
from pathlib import Path
import json


def example_1_basic_setup():
    """Example 1: Basic setup and query"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Basic Setup and Query")
    print("="*80)
    
    # Initialize the RAG pipeline
    rag = LocalRAGPipeline(
        embedding_model="all-MiniLM-L6-v2",  # Fast, lightweight model
        llm_model="microsoft/phi-2",         # Small but capable LLM
        chunk_size=500,
        chunk_overlap=50,
        storage_path="./example_storage"
    )
    
    # Create some example documents
    example_docs_dir = Path("./example_documents")
    example_docs_dir.mkdir(exist_ok=True)
    
    # Create sample documents
    (example_docs_dir / "ai_basics.txt").write_text("""
    Artificial Intelligence (AI) is the simulation of human intelligence by machines.
    Machine learning is a subset of AI that enables systems to learn from data.
    Deep learning uses neural networks with multiple layers to process complex patterns.
    Natural language processing (NLP) helps computers understand human language.
    """)
    
    (example_docs_dir / "python_guide.txt").write_text("""
    Python is a high-level programming language known for its simplicity.
    It supports multiple programming paradigms including object-oriented and functional.
    Python is widely used in data science, machine learning, and web development.
    Popular libraries include NumPy, Pandas, and TensorFlow.
    """)
    
    (example_docs_dir / "data_science.txt").write_text("""
    Data science combines statistics, programming, and domain knowledge.
    It involves collecting, cleaning, analyzing, and visualizing data.
    Key skills include Python, R, SQL, and statistical analysis.
    Data scientists build predictive models and extract insights from data.
    """)
    
    # Load and process documents
    print("\n📂 Loading documents...")
    documents = rag.load_documents(str(example_docs_dir))
    
    # Build indices
    print("\n🔧 Building vector index...")
    rag.build_vector_index(documents)
    
    print("\n🕸️  Building knowledge graph...")
    rag.build_knowledge_graph(documents)
    
    # Save the pipeline
    print("\n💾 Saving pipeline...")
    rag.save()
    
    # Query the system
    print("\n🔍 Querying the system...")
    result = rag.query(
        "What is machine learning and how does it relate to AI?",
        search_type="hybrid",
        top_k=3
    )
    
    print("\n✅ ANSWER:")
    print(result['answer'])
    print("\n📚 SOURCES:")
    for i, doc in enumerate(result['retrieved_documents'], 1):
        print(f"{i}. {doc['metadata']['source']}")


def example_2_different_search_types():
    """Example 2: Compare different search types"""
    print("\n" + "="*80)
    print("EXAMPLE 2: Comparing Search Types")
    print("="*80)
    
    # Load existing pipeline
    rag = LocalRAGPipeline(storage_path="./example_storage")
    rag.load()
    
    query = "Tell me about Python programming"
    
    print(f"\n📝 Query: {query}\n")
    
    # Vector search
    print("🔵 VECTOR SEARCH:")
    vector_results = rag.query(query, search_type="vector", top_k=3)
    print(f"Answer: {vector_results['answer'][:200]}...")
    
    # Graph search
    print("\n🔶 GRAPH SEARCH:")
    graph_results = rag.query(query, search_type="graph", top_k=3)
    print(f"Answer: {graph_results['answer'][:200]}...")
    
    # Hybrid search
    print("\n🟣 HYBRID SEARCH:")
    hybrid_results = rag.query(query, search_type="hybrid", top_k=3)
    print(f"Answer: {hybrid_results['answer'][:200]}...")


def example_3_custom_weights():
    """Example 3: Custom search weights"""
    print("\n" + "="*80)
    print("EXAMPLE 3: Custom Search Weights")
    print("="*80)
    
    rag = LocalRAGPipeline(storage_path="./example_storage")
    rag.load()
    
    query = "What skills are important for data science?"
    
    # More weight on vector search
    print("\n⚖️  80% Vector, 20% Graph:")
    results1 = rag.hybrid_search(query, top_k=3, vector_weight=0.8, graph_weight=0.2)
    print(f"Top result: {results1[0].content[:150]}...")
    
    # More weight on graph search
    print("\n⚖️  30% Vector, 70% Graph:")
    results2 = rag.hybrid_search(query, top_k=3, vector_weight=0.3, graph_weight=0.7)
    print(f"Top result: {results2[0].content[:150]}...")


def example_4_batch_queries():
    """Example 4: Process multiple queries"""
    print("\n" + "="*80)
    print("EXAMPLE 4: Batch Query Processing")
    print("="*80)
    
    rag = LocalRAGPipeline(storage_path="./example_storage")
    rag.load()
    
    queries = [
        "What is artificial intelligence?",
        "How is Python used in data science?",
        "What are neural networks?",
    ]
    
    results = []
    for query in queries:
        print(f"\n📝 Query: {query}")
        result = rag.query(query, search_type="hybrid", top_k=2)
        print(f"✅ Answer: {result['answer'][:150]}...")
        results.append(result)
    
    # Save results
    output_file = "./batch_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to {output_file}")


def example_5_inspect_knowledge_graph():
    """Example 5: Inspect the knowledge graph"""
    print("\n" + "="*80)
    print("EXAMPLE 5: Knowledge Graph Inspection")
    print("="*80)
    
    rag = LocalRAGPipeline(storage_path="./example_storage")
    rag.load()
    
    print(f"\n📊 Graph Statistics:")
    print(f"Nodes: {rag.knowledge_graph.number_of_nodes()}")
    print(f"Edges: {rag.knowledge_graph.number_of_edges()}")
    
    # Find most connected entities
    print("\n🔗 Most Connected Entities:")
    degrees = dict(rag.knowledge_graph.degree())
    top_entities = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:10]
    
    for entity, degree in top_entities:
        node_type = rag.knowledge_graph.nodes[entity].get('type', 'unknown')
        print(f"  {entity} ({node_type}): {degree} connections")
    
    # Show relationships
    print("\n🔀 Sample Relationships:")
    sample_edges = list(rag.knowledge_graph.edges(data=True))[:5]
    for src, dst, data in sample_edges:
        relation = data.get('relation', 'related_to')
        print(f"  {src} --[{relation}]--> {dst}")


def main():
    """Run all examples"""
    print("\n" + "🚀"*40)
    print("RAG PIPELINE EXAMPLES")
    print("🚀"*40)
    
    try:
        # Run examples
        example_1_basic_setup()
        
        input("\n\nPress Enter to continue to Example 2...")
        example_2_different_search_types()
        
        input("\n\nPress Enter to continue to Example 3...")
        example_3_custom_weights()
        
        input("\n\nPress Enter to continue to Example 4...")
        example_4_batch_queries()
        
        input("\n\nPress Enter to continue to Example 5...")
        example_5_inspect_knowledge_graph()
        
        print("\n\n✨ All examples completed!")
        
    except KeyboardInterrupt:
        print("\n\n⏸️  Examples interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
