# Project Knowledge Base
_Consolidated long-term memory - patterns, decisions, and learnings_

## Architecture & Design Decisions

### Two-Layer Memory System
- **Short-term memory**: RAM-like workspace (.cursor/memory/short-term/) - not versioned
- **Long-term memory**: Consolidated knowledge base (.cursor/memory/long-term/) - versioned
- **Rules system**: Cursor-specific prompts (.cursor/rules/)

### MCP Server Architecture
- Built with FastMCP framework (Python)
- 5 core tools for memory management:
  1. validate_memory_system - Configuration validation
  2. get_memory_prompt_for_current_state - Context-aware prompts
  3. list_memory_files - File metadata listing
  4. load_memory_files - Content loading for sessions
  5. append_to_memory - Dynamic content addition

## Coding Standards & Conventions

### Python Structure
- Package: memory_mcp_server
- Main module: src/memory_mcp_server/server.py
- Prompts module: src/memory_mcp_server/prompts.py
- Uses dataclasses for configuration (MemoryConfig)
- Async/await pattern for all MCP tools
- Comprehensive logging with structured output

### File Organization
- Source in src/ directory
- Docker support with Dockerfile + Makefile
- UV for dependency management (uv.lock)
- Setup via pyproject.toml (setuptools backend)

## Domain Knowledge

### Memory Operations
- Session initialization: Load long-term → scan issues → restore working memory
- Dynamic allocation: Create topic-specific memories when needed
- Knowledge consolidation: Promote patterns (3+ occurrences) from RAM to long-term
- Garbage collection: Clear 30+ day old short-term entries

### MCP Integration
- Designed for Cursor IDE integration
- Operates on current working directory
- No external configuration required
- Docker-first deployment strategy

## Recurring Patterns

### Error Handling Pattern
```python
try:
    # Operation
    await ctx.info("Operation starting")
    result = perform_operation()
    return {"success": True, "data": result}
except Exception as e:
    await ctx.error(f"Operation failed: {str(e)}")
    return {"success": False, "error": str(e)}
```

### File Metadata Pattern
- Always include: size_bytes, size_kb, modified timestamp
- Line and character counts for text files
- Existence checks with graceful error handling

## API Contracts

### MCP Tool Response Format
```json
{
  "success": boolean,
  "data": object,
  "error": string (optional)
}
```

### Memory File Structure
- Long-term: project-knowledge.md, known-issues.md
- Short-term: working-memory.md, [dynamic-topics].md
- Rules: intelligent-memory.md

## Technical Learnings

### FastMCP Best Practices
- Use @mcp.tool decorator with detailed descriptions
- Context parameter for logging and communication
- Return structured dictionaries for tool outputs
- Async operations for all tools

### Memory File Management
- UTF-8 encoding for all text files
- Markdown format for human readability
- Timestamp prefixes for temporal tracking
- Hierarchical directory structure for organization
