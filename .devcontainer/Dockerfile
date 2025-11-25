# Development container for KUB Course
FROM python:3.11-slim-bookworm

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Install uv for fast package management
RUN pip install --no-cache-dir uv

# Set working directory
WORKDIR /workspace

# Copy only dependency files first for layer caching
COPY pyproject.toml .

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

USER $USERNAME

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV JUPYTER_ENABLE_LAB=yes

CMD ["/bin/bash"]
