# Contributing to Local RAG Pipeline

Thank you for considering contributing to Local RAG Pipeline! This document outlines the process and guidelines for contributing.

## 🎯 Ways to Contribute

- 🐛 **Report bugs** - Help us identify issues
- 💡 **Suggest features** - Share your ideas
- 📖 **Improve documentation** - Make it clearer
- 🔧 **Submit code** - Fix bugs or add features
- ⭐ **Star the repo** - Show your support
- 📣 **Spread the word** - Share with others

## 🚀 Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/yourusername/local-rag-pipeline.git
cd local-rag-pipeline
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8 mypy
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

## 📝 Code Style

We follow PEP 8 with some modifications:

### Formatting
```bash
# Format code with black
black src/ tests/

# Check style
flake8 src/ tests/

# Type checking
mypy src/
```

### Guidelines
- Use descriptive variable names
- Add docstrings to all functions and classes
- Keep functions focused and small
- Write self-documenting code
- Add comments for complex logic

### Example

```python
def process_document(content: str, chunk_size: int = 500) -> List[str]:
    """
    Process a document into chunks for embedding.
    
    Args:
        content: The document content to process
        chunk_size: Maximum size of each chunk in characters
        
    Returns:
        List of document chunks
        
    Raises:
        ValueError: If content is empty or chunk_size is invalid
    """
    if not content:
        raise ValueError("Content cannot be empty")
    
    # Implementation here
    pass
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_pipeline.py

# Run specific test
pytest tests/test_pipeline.py::test_vector_search
```

### Writing Tests

- Write tests for all new features
- Maintain or improve code coverage
- Use descriptive test names
- Include edge cases

```python
def test_vector_search_returns_correct_number_of_results():
    """Test that vector search returns the requested number of results."""
    rag = LocalRAGPipeline()
    # Test implementation
    pass
```

## 📚 Documentation

### Code Documentation
- Add docstrings to all public functions and classes
- Use Google-style docstrings
- Include type hints
- Document exceptions

### User Documentation
- Update relevant docs in `docs/` folder
- Add examples for new features
- Update README.md if needed
- Keep CHANGELOG.md updated

## 🔄 Pull Request Process

### Before Submitting

1. **Test your changes**
   ```bash
   pytest
   black src/ tests/
   flake8 src/ tests/
   ```

2. **Update documentation**
   - Add/update docstrings
   - Update user docs
   - Add examples if needed

3. **Write clear commit messages**
   ```
   Add feature: hybrid search weighting
   
   - Implement configurable weights for vector/graph search
   - Add tests for weight validation
   - Update documentation with examples
   ```

### Submitting

1. Push your branch
   ```bash
   git push origin feature/your-feature-name
   ```

2. Create a Pull Request on GitHub

3. Fill out the PR template completely

4. Wait for review and address feedback

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
- [ ] Tests pass locally
- [ ] Added new tests
- [ ] Updated existing tests

## Documentation
- [ ] Updated docstrings
- [ ] Updated user documentation
- [ ] Added examples

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
```

## 🐛 Bug Reports

### Before Reporting
- Check existing issues
- Verify it's reproducible
- Test with latest version

### What to Include

```markdown
**Description**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Initialize pipeline with...
2. Load documents from...
3. Query with...
4. See error

**Expected Behavior**
What you expected to happen

**Actual Behavior**
What actually happened

**Environment**
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.9.7]
- Package version: [e.g., 1.0.0]

**Additional Context**
- Error messages
- Stack traces
- Screenshots
```

## 💡 Feature Requests

### What to Include

```markdown
**Problem Statement**
What problem does this solve?

**Proposed Solution**
How would you solve it?

**Alternatives Considered**
What other approaches did you think about?

**Additional Context**
Any relevant examples or references
```

## 🎨 Project Structure

```
local-rag-pipeline/
├── src/                  # Source code
│   ├── rag_pipeline.py   # Core implementation
│   ├── rag_interface.py  # CLI interface
│   └── config.py         # Configuration
├── examples/             # Usage examples
├── tests/                # Test suite
├── docs/                 # Documentation
└── .github/              # GitHub configs
```

## 🔍 Code Review Process

1. **Automated Checks**
   - CI/CD runs tests
   - Style checks run
   - Coverage measured

2. **Manual Review**
   - Code quality
   - Design decisions
   - Documentation
   - Test coverage

3. **Feedback**
   - Address comments
   - Make changes
   - Re-request review

4. **Merge**
   - Approved by maintainer
   - All checks passing
   - Up to date with main

## 📋 Commit Message Guidelines

### Format
```
<type>: <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

### Examples

```
feat: add cross-encoder reranking

- Implement cross-encoder model integration
- Add configuration options
- Include usage examples

Closes #123
```

```
fix: resolve memory leak in vector index

The FAISS index wasn't being properly released,
causing memory to accumulate over time.

Fixes #456
```

## 🎯 Development Priorities

### High Priority
- Bug fixes
- Security issues
- Documentation improvements
- Performance optimizations

### Medium Priority
- New features (aligned with roadmap)
- Code refactoring
- Test coverage improvements

### Low Priority
- Nice-to-have features
- Experimental additions
- Alternative implementations

## 🤝 Community Guidelines

### Be Respectful
- Be welcoming to newcomers
- Respect different viewpoints
- Accept constructive criticism
- Focus on what's best for the project

### Be Helpful
- Answer questions when you can
- Share your knowledge
- Help review PRs
- Mentor new contributors

### Be Professional
- Use inclusive language
- Stay on topic
- Keep discussions constructive
- Follow the code of conduct

## 📞 Getting Help

- 💬 [GitHub Discussions](https://github.com/yourusername/local-rag-pipeline/discussions)
- 🐛 [Issue Tracker](https://github.com/yourusername/local-rag-pipeline/issues)
- 📖 [Documentation](docs/)

## 🎉 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

Thank you for contributing! 🙏

---

**Questions?** Open a discussion or reach out to the maintainers.
