# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-11-06

### Added
- Initial release of Local RAG Pipeline
- Vector search using FAISS
- Knowledge graph using NetworkX
- Hybrid search combining both approaches
- Support for PDF, DOCX, TXT, MD, CSV formats
- Interactive CLI interface
- Python API for programmatic access
- Jupyter notebook examples
- Comprehensive documentation (40KB+)
- Automated setup script
- Save/load functionality for indices
- Configurable search weights
- Multiple LLM support via HuggingFace
- GPU acceleration support
- Extensive error handling
- Unit tests and CI/CD pipeline

### Features
- Multi-format document support
- Persistent storage
- Three search modes (vector, graph, hybrid)
- Customizable chunk sizes
- Progress indicators
- Statistics dashboard
- Example usage scripts
- Production-ready error handling

### Documentation
- README with quick start guide
- Getting started tutorial
- Complete API reference
- Architecture documentation
- Contributing guidelines
- Troubleshooting guide
- Code examples
- Jupyter notebooks

### Technical
- Python 3.8+ support
- Cross-platform (Linux, macOS, Windows)
- Virtual environment support
- GPU acceleration ready
- Type hints throughout
- Comprehensive docstrings

## [Unreleased]

### Planned
- [ ] Advanced NER integration with spaCy
- [ ] Cross-encoder reranking
- [ ] Multi-modal support (images, tables)
- [ ] Web UI with Gradio
- [ ] RESTful API server
- [ ] Docker containerization
- [ ] Incremental indexing
- [ ] Multi-language support
- [ ] Streaming LLM responses
- [ ] Advanced graph algorithms
- [ ] Custom entity extractors
- [ ] Batch processing utilities
- [ ] Performance monitoring
- [ ] Export to various formats
- [ ] Integration with vector databases

### Future Considerations
- Cloud deployment options
- Distributed processing
- Real-time indexing
- Advanced visualization
- Plugin system
- Model fine-tuning utilities

---

## Version Guidelines

- **Major version** (X.0.0): Incompatible API changes
- **Minor version** (0.X.0): New features, backwards compatible
- **Patch version** (0.0.X): Bug fixes, backwards compatible

## How to Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to this project.

## Links

- [GitHub Repository](https://github.com/yourusername/local-rag-pipeline)
- [Documentation](docs/)
- [Issue Tracker](https://github.com/yourusername/local-rag-pipeline/issues)
- [Discussions](https://github.com/yourusername/local-rag-pipeline/discussions)
