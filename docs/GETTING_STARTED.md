# Getting Started with Local RAG Pipeline

This guide will help you get up and running with the Local RAG Pipeline in under 10 minutes.

## 📋 Prerequisites

### System Requirements
- **Operating System**: Linux, macOS, or Windows
- **Python**: 3.8 or higher
- **RAM**: 8GB minimum (16GB recommended)
- **Disk Space**: 10GB for models and data
- **GPU**: Optional but recommended (NVIDIA with CUDA)

### Verify Your Setup

```bash
# Check Python version
python --version  # Should be 3.8+

# Check pip
pip --version

# Check available RAM
free -h  # Linux/Mac
wmic OS get FreePhysicalMemory  # Windows
```

## 🚀 Installation

### Option 1: Automated Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/local-rag-pipeline.git
cd local-rag-pipeline

# Run setup script
chmod +x setup.sh
./setup.sh
```

The script will:
1. ✅ Check Python version
2. ✅ Create virtual environment
3. ✅ Install all dependencies
4. ✅ Create necessary directories

### Option 2: Manual Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/local-rag-pipeline.git
cd local-rag-pipeline

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## 📂 Prepare Your Documents

### 1. Create Documents Directory

```bash
mkdir my_documents
```

### 2. Add Your Documents

Copy your documents to the `my_documents/` folder:

```bash
cp /path/to/your/documents/* my_documents/
```

**Supported Formats:**
- 📄 PDF (`.pdf`)
- 📝 Word (`.docx`)
- 📋 Text (`.txt`)
- 📖 Markdown (`.md`)
- 📊 CSV (`.csv`)

### Example Document Structure

```
my_documents/
├── research_paper_2024.pdf
├── meeting_notes.docx
├── project_overview.md
└── data_analysis.csv
```

## 🎯 First Run

### Initialize the Pipeline

```bash
python src/rag_interface.py --documents ./my_documents
```

**What happens:**
1. 📥 Downloads required models (~5-15GB, first time only)
2. 📂 Loads and chunks your documents
3. 🔧 Builds vector index (FAISS)
4. 🕸️ Builds knowledge graph (NetworkX)
5. 💾 Saves everything for future use
6. ✨ Ready to answer questions!

**First run timing:**
- Model download: 5-15 minutes (one time)
- Index building: 1-5 minutes (depends on document count)

### Expected Output

```
🚀 Initializing RAG pipeline...
Loading embedding model: all-MiniLM-L6-v2
Loading LLM: microsoft/phi-2
RAG Pipeline initialized successfully!

📂 Loading documents from: ./my_documents
Loaded 42 document chunks

🔧 Building vector index...
Vector index built with 42 documents

🕸️  Building knowledge graph...
Knowledge graph built with 127 nodes and 234 edges

💾 Saving pipeline...
Pipeline saved to ./my_rag_storage

✨ Pipeline ready!

🤖 RAG PIPELINE - INTERACTIVE MODE
================================================================================

Commands:
  - Type your question to get an answer
  - 'stats' - Show pipeline statistics
  - 'quit' or 'exit' - Exit the program

[HYBRID] 💬 You: 
```

## 💬 Using the Pipeline

### Ask Your First Question

```
[HYBRID] 💬 You: What are the main topics in my documents?

🔍 Searching...

🤖 Answer:
The main topics include machine learning fundamentals, deep learning 
architectures, and natural language processing applications. The documents 
discuss practical implementations and recent advances in these areas.

📚 Sources:
1. ml_fundamentals.pdf
   Machine learning is a subset of artificial intelligence that enables...

2. deep_learning_guide.docx
   Deep learning uses neural networks with multiple layers to process...

3. nlp_overview.md
   Natural language processing helps computers understand human language...
```

### Try Different Commands

```
# Show statistics
[HYBRID] 💬 You: stats

📊 PIPELINE STATISTICS
Total documents: 42
Knowledge graph nodes: 127
Knowledge graph edges: 234
Vector index dimension: 384

# Switch search modes
[HYBRID] 💬 You: vector
✅ Switched to vector search mode

[VECTOR] 💬 You: graph
✅ Switched to graph search mode

[GRAPH] 💬 You: hybrid
✅ Switched to hybrid search mode

# Exit
[HYBRID] 💬 You: quit
👋 Goodbye!
```

## 🐍 Using the Python API

### Basic Usage

```python
from src.rag_pipeline import LocalRAGPipeline

# Initialize
rag = LocalRAGPipeline()

# Load documents
documents = rag.load_documents("./my_documents")

# Build indices
rag.build_vector_index(documents)
rag.build_knowledge_graph(documents)

# Save for later
rag.save()

# Query
result = rag.query(
    "What are the key findings?",
    search_type="hybrid",
    top_k=5
)

print("Answer:", result['answer'])
print("\nSources:")
for doc in result['retrieved_documents']:
    print(f"- {doc['metadata']['source']}")
```

### Loading Existing Index

```python
from src.rag_pipeline import LocalRAGPipeline

# Initialize and load existing index
rag = LocalRAGPipeline(storage_path="./my_rag_storage")
rag.load()

# Query immediately
result = rag.query("Your question here")
print(result['answer'])
```

## 📓 Using the Jupyter Notebook

```bash
# Start Jupyter
jupyter notebook examples/rag_notebook.ipynb

# Then run the cells interactively
```

The notebook includes:
- Step-by-step setup
- Interactive queries
- Visualization examples
- Knowledge graph exploration

## ⚙️ Basic Configuration

### Change Models

Edit `src/config.py`:

```python
# For faster performance (less RAM)
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # ~80MB
LLM_MODEL = "microsoft/phi-2"          # ~5GB

# For better quality (more RAM)
EMBEDDING_MODEL = "all-mpnet-base-v2"  # ~420MB
LLM_MODEL = "mistralai/Mistral-7B-Instruct-v0.1"  # ~14GB
```

### Adjust Search Behavior

```python
# More semantic similarity
VECTOR_WEIGHT = 0.8
GRAPH_WEIGHT = 0.2

# More relationship discovery
VECTOR_WEIGHT = 0.3
GRAPH_WEIGHT = 0.7
```

### Performance Tuning

```python
# Faster (fewer, larger chunks)
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100

# More precise (more, smaller chunks)
CHUNK_SIZE = 300
CHUNK_OVERLAP = 50
```

## ✅ Verify Installation

Run the example script:

```bash
python examples/example_usage.py
```

This will:
1. Create sample documents
2. Initialize the pipeline
3. Run multiple query examples
4. Show different search modes

## 🎯 Next Steps

Now that you're set up:

1. **Explore**: Try different questions with your documents
2. **Experiment**: Change search modes and configurations
3. **Learn**: Read the [User Guide](USER_GUIDE.md)
4. **Customize**: Adjust settings in `src/config.py`
5. **Extend**: Check [Architecture](ARCHITECTURE.md) for technical details

## 🆘 Troubleshooting

### Models Not Downloading

**Problem**: Models fail to download

**Solution**:
- Check internet connection
- Models download to `~/.cache/huggingface/`
- Try downloading manually or wait longer (can take 15+ minutes)

### Out of Memory

**Problem**: Process killed or memory error

**Solution**:
```python
# Use smaller models
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "microsoft/phi-2"

# Reduce chunk count
CHUNK_SIZE = 1000
```

### Slow Performance

**Problem**: Queries take too long

**Solution**:
- Install `faiss-gpu` if you have CUDA
- Use GPU: `USE_GPU = True` in config
- Reduce `TOP_K` value
- Use smaller models

### Import Errors

**Problem**: ModuleNotFoundError

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### No Documents Loaded

**Problem**: "Loaded 0 document chunks"

**Solution**:
- Check document path is correct
- Verify file extensions are supported
- Ensure files are readable
- Check file permissions

## 📚 Additional Resources

- **User Guide**: Comprehensive usage documentation
- **API Reference**: Python API details
- **Architecture**: Technical implementation details
- **Examples**: More code examples in `examples/`

## 🎉 Success!

You should now have:
- ✅ Pipeline installed and working
- ✅ Documents loaded and indexed
- ✅ Ability to ask questions
- ✅ Understanding of basic usage

**Ready to dive deeper?** Check out the [User Guide](USER_GUIDE.md)!

---

**Questions?** See [Troubleshooting](TROUBLESHOOTING.md) or open an issue.
