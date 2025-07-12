#!/usr/bin/env python
"""Setup script for QuantAnalysis package."""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Modern portfolio analytics for quantitative trading"

# Read requirements
def read_requirements():
    requirements = [
        "pandas>=1.3.0",
        "numpy>=1.20.0",
        "matplotlib>=3.5.0",
        "scipy>=1.7.0",
        "python-dateutil>=2.8.0",
    ]
    return requirements

setup(
    name="quantanalysis",
    use_scm_version={
        "write_to": "src/quantanalysis/_version.py",
        "fallback_version": "0.1.0"
    },
    description="Modern portfolio analytics for quantitative trading",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/quantanalysis",
    license="Apache-2.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "quantanalysis": ["fonts/*", "*.html"],
    },
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=read_requirements(),
    setup_requires=["setuptools_scm"],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "isort>=5.10.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
            "pre-commit>=2.17.0",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "myst-parser>=0.17.0",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    keywords=[
        "quant", "finance", "portfolio", "analytics", "trading", 
        "quantitative", "risk", "performance", "returns"
    ],
    zip_safe=False,
)