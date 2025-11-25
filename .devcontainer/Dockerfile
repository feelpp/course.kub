# Development container for KUB Course
# Using Microsoft's Python devcontainer base (Ubuntu 24.04, Python 3.12, GLIBC 2.39)
# This image is Codespaces-ready with vscode user already configured
FROM mcr.microsoft.com/devcontainers/python:3.12

# Install additional system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    fmpy \
    pandas \
    plotly \
    scipy \
    numpy \
    ipykernel \
    tabulate \
    jupyter \
    jupyterlab \
    pytest \
    pytest-cov \
    ruff \
    mypy \
    build
