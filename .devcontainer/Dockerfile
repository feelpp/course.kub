# Development container for KUB Course
# Using Microsoft's Python devcontainer base (Ubuntu 24.04, Python 3.12, GLIBC 2.39)
# This image is Codespaces-ready with vscode user already configured
FROM mcr.microsoft.com/devcontainers/python:3.12

# Install additional system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast Python package management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set environment variables for uv
ENV UV_SYSTEM_PYTHON=1

# Install Python dependencies using uv (10-100x faster than pip)
RUN uv pip install --system \
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
