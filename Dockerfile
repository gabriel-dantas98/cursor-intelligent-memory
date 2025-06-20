FROM python:3.11-slim

# Build arguments for metadata
ARG VERSION="dev"
ARG BUILD_DATE
ARG COMMIT_SHA

# Add metadata labels
LABEL org.opencontainers.image.title="Cursor Intelligent Memory MCP Server" \
      org.opencontainers.image.description="Sistema de memória inteligente para Cursor IDE" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.revision="${COMMIT_SHA}" \
      org.opencontainers.image.source="https://github.com/gabriel-dantas98/cursor-intelligent-memory"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy only dependency files first for better caching
COPY pyproject.toml ./

# Install Python dependencies (separate layer for better caching)
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -e .

# Copy source code (this layer changes more frequently)
COPY src/ ./src/
COPY README.md ./

# Create non-root user
RUN useradd -m -u 1000 mcp-user
USER mcp-user

# Expose port
EXPOSE 8000

# Set working directory to /workspace for user projects
WORKDIR /workspace

# Run the server
CMD ["python", "-m", "memory_mcp_server.server"] 
