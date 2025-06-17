# Memory MCP Server

MCP server for Cursor's intelligent memory system. Provides tools for managing persistent memory across development sessions.

## Features

- **Two-layer memory architecture**: Short-term (RAM-like) and long-term (consolidated) storage
- **Automatic memory validation**: Check if memory system is properly configured
- **Dynamic prompt generation**: Context-aware prompts based on memory state
- **File management**: List, load, and append to memory files
- **Session persistence**: Maintain context across Cursor sessions

## Tools

The server provides 5 MCP tools:

1. **`validate_memory_system`** - Validates memory system configuration
2. **`get_memory_prompt_for_current_state`** - Returns appropriate setup or active prompts
3. **`list_memory_files`** - Lists available memory files with metadata
4. **`load_memory_files`** - Loads memory file contents for session initialization
5. **`append_to_memory`** - Adds new content to memory files with timestamps

## Development

### Test Tool Discovery
```bash
# Test that all tools are properly registered and configured
make test-tools
```

This will show all available tools, their descriptions, and parameters - useful for development and debugging.

### Development Mode
```bash
# Start with MCP Inspector for interactive testing
make dev
```

### Installation

#### Option 1: From Source
```bash
# Clone the repository
git clone <repo-url>
cd cursor-intelligent-memory

# Install in development mode
pip install -e .
```

#### Option 2: Using Docker (Recommended)
```bash
# Pull and run the Docker image
docker build -t memory-mcp-server .
docker run -it memory-mcp-server
```

### Building
```bash
# Build the package
make build

# Or build Docker image
make build-image
```

## Memory System Setup

The memory system requires a specific directory structure in your project:

```
.cursor/
├── memory/
│   ├── short-term/          # Volatile working memory
│   │   └── working-memory.md
│   └── long-term/           # Persistent consolidated memory
│       ├── project-knowledge.md
│       └── known-issues.md
└── rules/
    └── intelligent-memory.mdc
```

Use the `get_memory_prompt_for_current_state` tool to get complete setup instructions or active memory prompts based on your current configuration state.

## Docker Support

### Quick Start with Docker

```bash
# Build the Docker image
docker build -t memory-mcp-server .

# Run the container (interactive mode)
docker run -it --rm memory-mcp-server

# Or run as MCP server on port 8000
docker run -p 8000:8000 memory-mcp-server
```

### Using Make Commands

```bash
# Build Docker image using Make
make build-image

# Run other development commands
make dev      # Start with MCP Inspector
make test-tools  # Test tool discovery
```

## Configuration

### MCP Client Configuration

To use this server with Cursor or other MCP clients, add to your MCP configuration:

```json
{
  "mcpServers": {
    "memory": {
      "command": "python",
      "args": ["-m", "memory_mcp_server.server"],
      "cwd": "/path/to/your/project"
    }
  }
}
```

Or use Docker:

```json
{
  "mcpServers": {
    "memory": {
      "command": "docker",
      "args": ["run", "--rm", "-v", "$(pwd):/workspace", "-w", "/workspace", "memory-mcp-server"]
    }
  }
}
```

### Server Configuration

No external configuration required - the server operates on the current working directory's `.cursor/memory/` structure.

## Integration with Cursor

This MCP server is designed to be called at the beginning of Cursor chat sessions to:
1. Load existing memory context
2. Determine if memory system needs initialization
3. Provide appropriate guidance for memory management

The server enables Cursor to maintain intelligent memory across sessions, learning from patterns and preserving important context.

## Environment Variables

None required - the server operates on the current working directory's `.cursor/memory` structure.

## Development

The server follows FastMCP patterns with comprehensive logging and error handling. Each tool includes detailed descriptions for optimal AI integration. 
