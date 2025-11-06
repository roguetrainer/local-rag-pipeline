# RAG Pipeline Configuration
# Copy this file and customize for your use case

# Model Configuration
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Options: all-MiniLM-L6-v2, all-mpnet-base-v2
LLM_MODEL = "microsoft/phi-2"          # Options: microsoft/phi-2, mistralai/Mistral-7B-Instruct-v0.1

# Document Processing
CHUNK_SIZE = 500          # Size of text chunks (characters)
CHUNK_OVERLAP = 50        # Overlap between chunks (characters)

# Storage
STORAGE_PATH = "./my_rag_storage"  # Where to save/load indices

# Search Configuration
DEFAULT_SEARCH_TYPE = "hybrid"  # Options: vector, graph, hybrid
DEFAULT_TOP_K = 5              # Number of documents to retrieve

# Hybrid Search Weights (must sum to 1.0)
VECTOR_WEIGHT = 0.7  # Weight for vector search (0.0 to 1.0)
GRAPH_WEIGHT = 0.3   # Weight for graph search (0.0 to 1.0)

# Generation Configuration
MAX_ANSWER_LENGTH = 200  # Maximum tokens in generated answer
GENERATION_TEMPERATURE = 0.7  # Creativity (0.0 = deterministic, 1.0 = creative)

# Performance
USE_GPU = True  # Use GPU if available
BATCH_SIZE = 32  # Batch size for embedding generation

# Supported File Types
SUPPORTED_EXTENSIONS = ['.txt', '.pdf', '.docx', '.md', '.csv']

# Advanced: Text Splitter Configuration
SEPARATORS = ["\n\n", "\n", ". ", " ", ""]  # Separator hierarchy

# Advanced: Vector Index Configuration
VECTOR_INDEX_TYPE = "FlatL2"  # FAISS index type
# Options: FlatL2 (exact), IVFFlat (faster for large datasets)

# Advanced: Knowledge Graph Configuration
ENTITY_MIN_LENGTH = 5  # Minimum length for entity extraction
EXTRACT_CAPITALIZED_ONLY = True  # Only extract capitalized words as entities

# Logging
VERBOSE = True  # Print detailed progress information
LOG_FILE = None  # Optional: path to log file (e.g., "./rag.log")
