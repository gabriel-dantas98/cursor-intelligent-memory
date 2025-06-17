FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy source code
COPY src/ ./src/
COPY pyproject.toml ./
COPY README.md ./

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Create non-root user
RUN useradd -m -u 1000 mcp-user
USER mcp-user

# Expose port
EXPOSE 8000

# Set working directory to /workspace for user projects
WORKDIR /workspace

# Run the server
CMD ["python", "-m", "memory_mcp_server.server"] 
