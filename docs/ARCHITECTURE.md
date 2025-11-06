# Architecture Documentation

## 🏗️ System Architecture Overview

The Local RAG Pipeline implements a hybrid retrieval system combining vector similarity search with knowledge graph relationships for enhanced document understanding and question answering.

---

## 📊 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface Layer                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐ │
│  │     CLI      │  │  Python API  │  │  Jupyter Notebook    │ │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘ │
└─────────┼──────────────────┼───────────────────────┼────────────┘
          │                  │                       │
          └──────────────────┼───────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      RAG Pipeline Core                           │
│  ┌────────────────────────────────────────────────────────┐    │
│  │              Document Processing Layer                  │    │
│  │  ┌────────────┐  ┌─────────────┐  ┌───────────────┐  │    │
│  │  │  Loaders   │→ │  Chunking   │→ │  Validation   │  │    │
│  │  └────────────┘  └─────────────┘  └───────────────┘  │    │
│  └────────────────────────┬───────────────────────────────┘    │
│                            ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Indexing & Storage Layer                    │   │
│  │  ┌──────────────────┐    ┌──────────────────────────┐  │   │
│  │  │  Vector Index    │    │   Knowledge Graph        │  │   │
│  │  │  (FAISS)         │    │   (NetworkX)            │  │   │
│  │  │                  │    │                          │  │   │
│  │  │  - Embeddings    │    │  - Entities              │  │   │
│  │  │  - Similarity    │    │  - Relationships         │  │   │
│  │  │  - Fast Search   │    │  - Graph Algorithms      │  │   │
│  │  └──────────────────┘    └──────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Retrieval & Ranking Layer                   │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │   │
│  │  │Vector Search │  │ Graph Search │  │Hybrid Fusion │ │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘ │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Generation Layer                            │   │
│  │  ┌────────────────────────────────────────────────┐    │   │
│  │  │  Local LLM (HuggingFace Transformers)         │    │   │
│  │  │  - Context Assembly                            │    │   │
│  │  │  - Prompt Engineering                          │    │   │
│  │  │  - Answer Generation                           │    │   │
│  │  └────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Persistence Layer                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐ │
│  │  Documents   │  │ Vector Index │  │  Knowledge Graph     │ │
│  │  (Pickle)    │  │   (FAISS)    │  │    (Gpickle)        │ │
│  └──────────────┘  └──────────────┘  └──────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔧 Component Architecture

### 1. Document Processing Pipeline

```python
Document Input
    ↓
[Format Detection]
    ↓
[Appropriate Loader]
    ├─ PDFMinerLoader (PDF)
    ├─ Docx2txtLoader (DOCX)
    ├─ TextLoader (TXT)
    ├─ UnstructuredMarkdownLoader (MD)
    └─ CSVLoader (CSV)
    ↓
[Text Extraction]
    ↓
[Chunking Strategy]
    ├─ RecursiveCharacterTextSplitter
    ├─ Configurable chunk_size
    └─ Configurable overlap
    ↓
[Metadata Preservation]
    ├─ Source file
    ├─ Chunk ID
    └─ Additional context
    ↓
Document Objects
```

**Key Design Decisions:**
- **Recursive splitting**: Maintains semantic coherence
- **Overlap**: Prevents context loss at boundaries
- **Metadata tracking**: Enables source attribution

---

### 2. Vector Index Architecture

```
┌─────────────────────────────────────────────┐
│           Sentence Transformer              │
│         (Embedding Model)                   │
│                                             │
│  Input: Text Chunks                        │
│  Output: Dense Vectors (384/768/1024 dim) │
└─────────────────┬───────────────────────────┘
                  ↓
┌─────────────────────────────────────────────┐
│              FAISS Index                    │
│           (IndexFlatL2)                     │
│                                             │
│  ┌────────────────────────────────────┐   │
│  │  Vector Storage                    │   │
│  │  - Float32 arrays                  │   │
│  │  - L2 distance metric              │   │
│  │  - O(n) search (exact)             │   │
│  └────────────────────────────────────┘   │
│                                             │
│  Query Vector → K-NN Search → Top-K Results│
└─────────────────────────────────────────────┘
```

**Specifications:**
- **Index Type**: FlatL2 (exact search)
- **Distance Metric**: L2 (Euclidean)
- **Vector Dimension**: Model-dependent (384-1024)
- **Precision**: Float32
- **Scalability**: Good for <1M vectors

**Alternative Indexes** (for scale):
- `IndexIVFFlat`: Faster for large datasets (>100K docs)
- `IndexIVFPQ`: Memory-efficient with quantization

---

### 3. Knowledge Graph Architecture

```
┌─────────────────────────────────────────────────────────┐
│              NetworkX DiGraph Structure                  │
│                                                          │
│  Nodes:                                                  │
│  ┌──────────────────┐      ┌──────────────────────┐   │
│  │  Document Nodes  │      │   Entity Nodes       │   │
│  │  - doc_id        │      │   - entity_name      │   │
│  │  - content       │      │   - type: entity     │   │
│  │  - type: document│      │   - metadata         │   │
│  │  - metadata      │      │                      │   │
│  └──────────────────┘      └──────────────────────┘   │
│                                                          │
│  Edges:                                                  │
│  ┌──────────────────┐      ┌──────────────────────┐   │
│  │  contains        │      │   same_source        │   │
│  │  (doc → entity)  │      │   (doc → doc)       │   │
│  └──────────────────┘      └──────────────────────┘   │
│                                                          │
│  Graph Algorithms:                                       │
│  - PageRank (node importance)                           │
│  - Degree Centrality (connectivity)                     │
│  - Shortest Path (relationship discovery)               │
│  - Community Detection (clustering)                     │
└─────────────────────────────────────────────────────────┘
```

**Entity Extraction Strategy:**
1. **Simple Heuristic** (current):
   - Capitalized words
   - Minimum length threshold
   - Co-occurrence tracking

2. **Advanced Options** (extensible):
   - spaCy NER
   - Custom entity recognizers
   - Relation extraction models

**Graph Queries:**
- Neighbor traversal
- Subgraph extraction
- Centrality-based ranking
- Path-based reasoning

---

### 4. Hybrid Search Architecture

```
┌──────────────────────────────────────────────────────────┐
│                     Query Processing                      │
└─────────────────────┬────────────────────────────────────┘
                      ↓
        ┌─────────────┴─────────────┐
        ↓                           ↓
┌──────────────────┐        ┌──────────────────┐
│  Vector Search   │        │   Graph Search   │
│                  │        │                  │
│  1. Encode query │        │  1. Extract      │
│  2. K-NN search  │        │     entities     │
│  3. Distance     │        │  2. Find related │
│     scoring      │        │     nodes        │
│  4. Return top-K │        │  3. Rank by      │
│                  │        │     centrality   │
│                  │        │  4. Return top-K │
└────────┬─────────┘        └────────┬─────────┘
         │                           │
         │    ┌───────────────────┐  │
         └───→│  Fusion Layer     │←─┘
              │                   │
              │ Score = α·V + β·G │
              │ where α+β = 1     │
              │                   │
              │ Default: α=0.7    │
              │          β=0.3    │
              └─────────┬─────────┘
                        ↓
              ┌─────────────────┐
              │  Unified Ranking│
              │  - Merge results│
              │  - Sort by score│
              │  - Deduplicate  │
              └─────────┬───────┘
                        ↓
                  Top-K Documents
```

**Fusion Algorithm:**
```python
def hybrid_search(query, vector_weight=0.7, graph_weight=0.3):
    # Vector scores (normalized inverse distance)
    vector_results = vector_search(query, k=k*2)
    vector_scores = {doc_id: 1/(1+distance) for doc_id, distance in vector_results}
    
    # Graph scores (normalized rank)
    graph_results = graph_search(query, k=k*2)
    graph_scores = {doc_id: 1/(rank+1) for rank, doc_id in enumerate(graph_results)}
    
    # Combine scores
    all_docs = set(vector_scores.keys()) | set(graph_scores.keys())
    combined = {
        doc_id: vector_weight * vector_scores.get(doc_id, 0) + 
                graph_weight * graph_scores.get(doc_id, 0)
        for doc_id in all_docs
    }
    
    # Return top-K
    return sorted(combined.items(), key=lambda x: x[1], reverse=True)[:k]
```

---

### 5. Generation Architecture

```
┌──────────────────────────────────────────────────────┐
│              Context Assembly                         │
│                                                       │
│  Retrieved Documents (Top-K)                         │
│       ↓                                              │
│  ┌─────────────────────────────────────────────┐   │
│  │ Context Window Management                   │   │
│  │ - Select top 3-5 documents                  │   │
│  │ - Truncate if exceeds model limit          │   │
│  │ - Preserve source attribution              │   │
│  └─────────────────────────────────────────────┘   │
└──────────────────┬───────────────────────────────────┘
                   ↓
┌──────────────────────────────────────────────────────┐
│              Prompt Engineering                       │
│                                                       │
│  Template:                                           │
│  ┌──────────────────────────────────────────────┐  │
│  │ Based on the following context, answer       │  │
│  │ the question.                                │  │
│  │                                              │  │
│  │ Context:                                     │  │
│  │ {document_1}                                 │  │
│  │ {document_2}                                 │  │
│  │ ...                                          │  │
│  │                                              │  │
│  │ Question: {query}                            │  │
│  │                                              │  │
│  │ Answer:                                      │  │
│  └──────────────────────────────────────────────┘  │
└──────────────────┬───────────────────────────────────┘
                   ↓
┌──────────────────────────────────────────────────────┐
│         HuggingFace Transformers Pipeline            │
│                                                       │
│  ┌────────────────────────────────────────────┐    │
│  │  Tokenization                              │    │
│  │  - Convert text to tokens                  │    │
│  │  - Add special tokens                      │    │
│  │  - Create attention masks                  │    │
│  └────────────────────────────────────────────┘    │
│                   ↓                                  │
│  ┌────────────────────────────────────────────┐    │
│  │  Model Inference                           │    │
│  │  - Forward pass                            │    │
│  │  - Auto-regressive generation              │    │
│  │  - Temperature sampling                    │    │
│  └────────────────────────────────────────────┘    │
│                   ↓                                  │
│  ┌────────────────────────────────────────────┐    │
│  │  Decoding                                  │    │
│  │  - Token to text conversion                │    │
│  │  - Special token removal                   │    │
│  │  - Post-processing                         │    │
│  └────────────────────────────────────────────┘    │
└──────────────────┬───────────────────────────────────┘
                   ↓
              Generated Answer
```

**Generation Parameters:**
- `max_new_tokens`: 200 (default)
- `temperature`: 0.7 (balanced creativity)
- `do_sample`: True (non-deterministic)
- `top_p`: 0.9 (nucleus sampling)

---

## 💾 Data Flow Diagram

```
User Query
    ↓
┌─────────────────────────────┐
│  Query Understanding        │
│  - Intent detection         │
│  - Entity extraction        │
└─────────────┬───────────────┘
              ↓
    ┌─────────┴─────────┐
    ↓                   ↓
[Vector Search]    [Graph Search]
    │                   │
    └─────────┬─────────┘
              ↓
    ┌─────────────────┐
    │ Hybrid Ranking  │
    │ (Weighted Fusion)│
    └────────┬─────────┘
             ↓
    ┌────────────────┐
    │ Context Assembly│
    └────────┬────────┘
             ↓
    ┌────────────────┐
    │ LLM Generation │
    └────────┬────────┘
             ↓
    ┌────────────────┐
    │ Answer + Sources│
    └────────────────┘
             ↓
        User Response
```

---

## 🔄 State Management

```
┌─────────────────────────────────────────────┐
│          Pipeline State                      │
│                                              │
│  ┌────────────────────────────────────┐    │
│  │  In-Memory State                   │    │
│  │  - documents: List[Document]       │    │
│  │  - vector_index: FAISS Index       │    │
│  │  - knowledge_graph: NetworkX Graph │    │
│  │  - embedding_model: SentenceTransf.│    │
│  │  - llm: HuggingFace Model          │    │
│  └────────────────────────────────────┘    │
│                                              │
│  ┌────────────────────────────────────┐    │
│  │  Persistent State                  │    │
│  │  - documents.pkl                   │    │
│  │  - vector_index.faiss              │    │
│  │  - knowledge_graph.gpickle         │    │
│  └────────────────────────────────────┘    │
│                                              │
│  Operations:                                 │
│  - save(): Serialize to disk                │
│  - load(): Deserialize from disk            │
│  - update(): Add new documents              │
└─────────────────────────────────────────────┘
```

---

## ⚡ Performance Characteristics

### Time Complexity

| Operation | Complexity | Notes |
|-----------|-----------|--------|
| Document Loading | O(n·m) | n=files, m=avg size |
| Embedding Generation | O(n·d) | n=chunks, d=dimension |
| Vector Index Build | O(n·d) | n=vectors, d=dimension |
| Vector Search | O(n·d) | Linear scan (FlatL2) |
| Graph Build | O(n²) | Worst case for edges |
| Graph Search | O(V+E) | V=vertices, E=edges |
| LLM Generation | O(k·l) | k=context, l=output length |

### Space Complexity

| Component | Space | Notes |
|-----------|-------|--------|
| Document Storage | O(n·s) | n=docs, s=avg size |
| Vector Index | O(n·d·4) | 4 bytes per float32 |
| Knowledge Graph | O(V+E) | Vertices + Edges |
| Model Weights | Fixed | 80MB-14GB |

### Optimization Opportunities

1. **Vector Search**: Use IVF index for O(√n) search
2. **Batching**: Process documents in parallel
3. **Caching**: Cache frequently accessed embeddings
4. **Quantization**: Use int8 for reduced memory
5. **Pruning**: Remove low-importance graph edges

---

## 🔒 Security Architecture

```
┌─────────────────────────────────────────────┐
│         Security Layers                      │
│                                              │
│  ┌────────────────────────────────────┐    │
│  │  Data Privacy                      │    │
│  │  - No external API calls           │    │
│  │  - Local processing only           │    │
│  │  - No telemetry                    │    │
│  └────────────────────────────────────┘    │
│                                              │
│  ┌────────────────────────────────────┐    │
│  │  Input Validation                  │    │
│  │  - File type checking              │    │
│  │  - Size limits                     │    │
│  │  - Path traversal prevention       │    │
│  └────────────────────────────────────┘    │
│                                              │
│  ┌────────────────────────────────────┐    │
│  │  Storage Security                  │    │
│  │  - File permissions                │    │
│  │  - Encrypted filesystem support    │    │
│  │  - Isolated storage paths          │    │
│  └────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

---

## 🔌 Extension Points

### 1. Custom Document Loaders
```python
# In rag_pipeline.py, _load_single_file()
loaders = {
    '.xml': CustomXMLLoader,
    '.json': CustomJSONLoader,
    # Add your custom loaders
}
```

### 2. Enhanced Entity Extraction
```python
# In build_knowledge_graph()
import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp(text)
entities = [(ent.text, ent.label_) for ent in doc.ents]
```

### 3. Custom Reranking
```python
# In hybrid_search()
from sentence_transformers import CrossEncoder
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
scores = reranker.predict([(query, doc.content) for doc in results])
```

### 4. Streaming Generation
```python
# In generate_answer()
from transformers import TextIteratorStreamer
streamer = TextIteratorStreamer(tokenizer)
# Implement streaming logic
```

---

## 📈 Scalability Considerations

### Current Limits (Default Config)
- Documents: ~10,000 efficiently
- Vector Index: ~1M vectors (FlatL2)
- Graph Nodes: ~100K efficiently
- Memory: 8-16GB RAM

### Scaling Strategies

**For More Documents:**
1. Use IVF FAISS index
2. Implement document batching
3. Use approximate search

**For Lower Memory:**
1. Use smaller embedding models
2. Implement vector quantization
3. Prune knowledge graph

**For Better Performance:**
1. GPU acceleration
2. Parallel document processing
3. Distributed search (future)

---

## 🧪 Testing Architecture

```
tests/
├── test_pipeline.py      # Integration tests
├── test_search.py        # Search functionality
├── test_graph.py         # Graph operations
└── test_generation.py    # LLM generation

Coverage Goals:
- Unit tests: >80%
- Integration tests: Critical paths
- End-to-end: Full pipeline
```

---

## 📦 Deployment Architecture

```
┌─────────────────────────────────────────────┐
│          Deployment Options                  │
│                                              │
│  1. Local Installation                       │
│     - pip install from repo                  │
│     - Direct Python execution                │
│                                              │
│  2. Docker Container (future)                │
│     - Containerized deployment               │
│     - Reproducible environment               │
│                                              │
│  3. API Server (future)                      │
│     - FastAPI/Flask wrapper                  │
│     - RESTful endpoints                      │
│                                              │
│  4. Web UI (future)                          │
│     - Gradio interface                       │
│     - Browser-based access                   │
└─────────────────────────────────────────────┘
```

---

## 🔍 Monitoring & Observability

**Metrics to Track:**
- Query latency (p50, p95, p99)
- Search accuracy (relevance)
- Memory usage
- GPU utilization (if applicable)
- Cache hit rates

**Logging Strategy:**
- INFO: Query processing steps
- DEBUG: Detailed search scores
- ERROR: Failures and exceptions
- Structured logging for analysis

---

## 🚀 Future Enhancements

### Short Term
- [ ] Advanced NER with spaCy
- [ ] Cross-encoder reranking
- [ ] Streaming responses
- [ ] Query caching

### Medium Term
- [ ] Multi-modal support (images, tables)
- [ ] Incremental indexing
- [ ] Web UI with Gradio
- [ ] API server

### Long Term
- [ ] Distributed processing
- [ ] Cloud deployment options
- [ ] Fine-tuning capabilities
- [ ] Advanced graph algorithms

---

## 📚 Technology Stack Details

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Embeddings** | Sentence-Transformers | ≥2.2.0 | Text encoding |
| **Vector Store** | FAISS | ≥1.7.4 | Similarity search |
| **Graph DB** | NetworkX | ≥3.0 | Relationship modeling |
| **LLM** | Transformers | ≥4.30.0 | Answer generation |
| **Doc Loading** | LangChain | ≥0.1.0 | Multi-format support |
| **Framework** | Python | ≥3.8 | Core language |

---

## 🎯 Design Principles

1. **Privacy First**: No external API calls, local processing
2. **Modularity**: Clean separation of concerns
3. **Extensibility**: Easy to add custom components
4. **Performance**: Efficient algorithms and data structures
5. **Usability**: Simple API, clear documentation
6. **Reliability**: Error handling, validation, testing

---

This architecture supports the core requirements of privacy, performance, and extensibility while maintaining simplicity for users and developers.
