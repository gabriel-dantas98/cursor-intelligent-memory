# Cursor Intelligent Memory MCP Server

Intelligent memory system for Cursor IDE that maintains persistent context between development sessions.

## What does it do?

- **2-layer memory**: Short-term (current session) and long-term (consolidated knowledge)
- **Pattern recognition**: Learns from your development patterns
- **Error prevention**: Remembers and avoids recurring problems
- **Cursor integration**: Works automatically with the IDE

## Quick Installation

### Via Docker (Recommended)
```bash
# Configure in .cursor/mcp.json
{
  "mcpServers": {
    "memory-docker": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "-v", "./:/workspace",
        "-w", "/workspace",
        "ghcr.io/gabriel-dantas98/cursor-intelligent-memory:main"
      ],
      "cwd": "."
    }
  }
}
```

### Via Python
```bash
git clone https://github.com/gabriel-dantas98/cursor-intelligent-memory.git
cd cursor-intelligent-memory
pip install -e .

# Configure in .cursor/mcp.json
{
  "mcpServers": {
    "memory": {
      "command": "python",
      "args": ["-m", "memory_mcp_server.server"],
      "env": {
        "CURSOR_MEMORY_BASE_PATH": "/Users/gabriel.dantas/git/gdantas/cursor-intelligent-memory"
      }
    },
  }
}
```

## How to use?

1. **Configure** one of the options above in `.cursor/mcp.json`
2. **Restart** Cursor
3. **Start chatting** - the system will automatically create:
   ```
   .cursor/memory/
   ├── short-term/working-memory.md    # Session memory
   └── long-term/
       ├── project-knowledge.md        # Consolidated knowledge
       └── known-issues.md            # Known issues
   ```

## Available Tools

- `validate_memory_system` - Validates memory system configuration
- `get_memory_prompt_for_current_state` - Returns prompts based on current state
- `list_memory_files` - Lists memory files with metadata
- `load_memory_files` - Loads memory file contents
- `memory_update` - Updates memory files with new content

## Development

```bash
# Install dependencies and test tools
make test-tools

# Development with MCP Inspector
make dev

# Build Docker image
make build-image

# Publish to GitHub Container Registry  
make push-to-ghcr

# Auxiliary commands
make install          # Install dependencies
make run             # Run MCP server
make clean           # Clean build artifacts
make test-actions     # Test GitHub Actions locally
make login-ghcr       # Login to GitHub Container Registry
make install-act      # Install act for local testing
```

## How does it work?

The system works like human memory:
- **Short-term**: Current session information (volatile)
- **Long-term**: Patterns and consolidated knowledge (persistent)
- **Automatic promotion**: Recurring patterns (3+ times) become permanent knowledge

## Repository

- **GitHub**: https://github.com/gabriel-dantas98/cursor-intelligent-memory
- **Docker**: `ghcr.io/gabriel-dantas98/cursor-intelligent-memory:main`
- **License**: MIT
