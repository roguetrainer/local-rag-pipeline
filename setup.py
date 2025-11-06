"""
Setup configuration for Local RAG Pipeline
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Read requirements
requirements = []
with open("requirements.txt") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="local-rag-pipeline",
    version="1.0.0",
    author="Local RAG Pipeline Contributors",
    author_email="your.email@example.com",
    description="A production-ready RAG pipeline combining vector search and knowledge graphs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/local-rag-pipeline",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.990",
        ],
        "gpu": [
            "faiss-gpu>=1.7.4",
        ],
    },
    entry_points={
        "console_scripts": [
            "rag-cli=src.rag_interface:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="rag retrieval-augmented-generation vector-search knowledge-graph nlp ai machine-learning",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/local-rag-pipeline/issues",
        "Source": "https://github.com/yourusername/local-rag-pipeline",
        "Documentation": "https://github.com/yourusername/local-rag-pipeline/tree/main/docs",
    },
)
