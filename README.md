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

### Docker Publishing

The project supports automated Docker publishing to GitHub Container Registry:

```bash
# Local publishing
make publish              # Login + build + push to ghcr.io
make build-for-ghcr      # Just build locally
make login-ghcr          # Login to GitHub Container Registry

# Testing with act (GitHub Actions locally)
make install-act         # Install act tool
make test-docker-build   # Test Docker workflow locally
make test-actions        # List available workflows
```

See [Docker Publishing Guide](docs/docker-publishing.md) for detailed instructions.

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

# Cursor Intelligent Memory MCP Server

An intelligent memory system for Cursor IDE that provides persistent context across development sessions.

## Features

- **Two-layer memory architecture**: Short-term (session-based) and long-term (persistent) memory
- **Automatic pattern recognition**: Learns from your development patterns
- **Error tracking**: Remembers and prevents repeated issues
- **Knowledge consolidation**: Promotes frequently used patterns to long-term memory
- **Debug tools**: Execute bash commands for debugging and exploration
- **MCP integration**: Seamless integration with Cursor IDE

## Installation

### Method 1: Python Package (Recommended for Development)

```bash
# Clone the repository
git clone https://github.com/gabriel-dantas98/cursor-intelligent-memory.git
cd cursor-intelligent-memory

# Install in development mode
pip install -e .
```

### Method 2: Docker Container (Recommended for Production)

```bash
# Pull the pre-built image
docker pull ghcr.io/gabriel-dantas98/cursor-intelligent-memory
```

## Configuration

Add to your Cursor MCP configuration file (`.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "memory-python": {
      "command": "python",
      "args": ["-m", "memory_mcp_server.server"],
      "cwd": ".",
      "env": {
        "PYTHONPATH": "src"
      }
    },
    "memory-docker": {
      "command": "docker",
      "args": [
        "run", 
        "--rm", 
        "-i",
        "-v", 
        "${PWD}:/workspace",
        "-w", 
        "/workspace",
        "ghcr.io/gabriel-dantas98/cursor-intelligent-memory"
      ]
    }
  }
}
```

### Configuration Explanation

#### `memory-python` (Direct Execution)
- Uses your local Python installation
- Sets `PYTHONPATH` to locate the module correctly
- Runs in your current working directory
- **Requires**: `pip install -e .` or manual installation

#### `memory-docker` (Docker Execution)  
- Mounts your current directory (`${PWD}`) to `/workspace` in the container
- Sets the container's working directory to `/workspace`
- **Critical**: The volume mount ensures the container can access your `.cursor/memory` files
- Runs as non-root user (uid 1000) for security

### Filesystem Access Requirements

Both configurations ensure the MCP server can access:
- `.cursor/memory/short-term/` (session-based memory files)
- `.cursor/memory/long-term/` (persistent knowledge base)
- `.cursor/rules/` (configuration rules)

**Important**: Without proper filesystem access, the memory system cannot read or write your project's memory files, making it non-functional.

## Available Tools

The Memory MCP Server provides the following tools for managing intelligent memory:

### Core Memory Tools

#### `validate_memory_system`
Validates if the Cursor memory system directories exist and are properly configured.
- **Returns**: Setup status and guides next steps
- **Use**: Essential for determining if memory system initialization is needed

#### `get_memory_prompt_for_current_state`
Returns the appropriate prompt based on memory system status.
- **If configured**: Returns the active memory prompt
- **If not configured**: Returns complete setup instructions
- **Use**: Get the right guidance for the current state

#### `list_memory_files`
Lists all available memory files in both short-term and long-term directories.
- **Returns**: File metadata (sizes, modification dates, basic statistics)
- **Use**: Understanding what memory content is available for loading

#### `load_memory_files`
Loads and returns the contents of specific memory files or all memory files.
- **Parameters**: 
  - `file_names` (optional): List of specific files to load
- **Use**: Reading memory content into the current context for session initialization

#### `append_to_memory`
Appends new content to a specific memory file.
- **Parameters**:
  - `file_name`: The memory file to append to
  - `content`: The content to append
  - `add_timestamp` (optional): Whether to add timestamp (default: true)
- **Use**: Persisting new learnings, errors, decisions, or insights

### Debug Tools

#### `debug_exec_command`
Executes bash commands in the container environment for debugging purposes.
- **Parameters**:
  - `command`: The bash command to execute
  - `working_directory` (optional): Directory to execute the command in
- **Security**: Only allows safe read-only commands by default
- **Timeout**: 30 seconds maximum execution time
- **Use**: Listing directories, checking file permissions, debugging filesystem issues

**Safe commands supported**:
- `ls`, `find`, `cat`, `head`, `tail`
- `pwd`, `whoami`, `id`, `df`, `du`
- `ps`, `env`, `which`, `file`, `stat`, `tree`

**Example usage**:
```bash
# List memory directory structure
debug_exec_command("find .cursor -type d")

# Check current directory contents
debug_exec_command("ls -la")

# View disk usage
debug_exec_command("df -h .")

# Check environment info
debug_exec_command("whoami && pwd")
```
