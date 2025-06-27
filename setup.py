#!/usr/bin/env python3
"""
Setup script for BrainPlay: Win or Lose
Demonstrates Python package setup and distribution.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements from requirements.txt
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    with open(requirements_file, 'r') as f:
        requirements = [
            line.strip() 
            for line in f 
            if line.strip() and not line.startswith('#')
        ]

setup(
    # Basic package information
    name="brainplay-game",
    version="1.0.0",
    author="Python AI Mentor",
    author_email="mentor@brainplay.dev",
    description="A comprehensive CLI brain training game demonstrating advanced Python concepts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/brainplay-game",
    
    # Package discovery
    packages=find_packages(exclude=["test*", "docs*"]),
    
    # Include additional files
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md", "*.json"],
        "data": ["*.json", "*.csv", "*.log"],
    },
    
    # Python version requirement
    python_requires=">=3.8",
    
    # Dependencies
    install_requires=requirements,
    
    # Optional dependencies for different use cases
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "coverage>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "docs": [
            "sphinx>=6.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
        "performance": [
            "line_profiler>=4.0.0",
            "memory_profiler>=0.60.0",
        ],
    },
    
    # Console scripts - allows running the game from command line
    entry_points={
        "console_scripts": [
            "brainplay=main:main",
            "brainplay-game=main:main",
        ],
    },
    
    # Classification
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Topic :: Games/Entertainment :: Puzzle Games",
        "Topic :: Education",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    
    # Keywords for PyPI search
    keywords=[
        "game", "cli", "brain-training", "education", "python", 
        "learning", "quiz", "math", "programming", "tutorial"
    ],
    
    # Project URLs
    project_urls={
        "Bug Reports": "https://github.com/yourusername/brainplay-game/issues",
        "Source": "https://github.com/yourusername/brainplay-game",
        "Documentation": "https://brainplay-game.readthedocs.io/",
        "Funding": "https://github.com/sponsors/yourusername",
    },
    
    # License
    license="MIT",
    
    # Zip safety
    zip_safe=False,
)