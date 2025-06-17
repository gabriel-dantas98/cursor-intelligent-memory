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

## 2025-06-17 16:17:54
## CI/CD & Deployment Architecture

### GitHub Actions Pipeline (Implemented)
- **Multi-architecture builds**: linux/amd64 and linux/arm64
- **Auto-publish to GitHub Container Registry**: `ghcr.io`
- **Intelligent tagging strategy**:
  - `latest` (main branch)
  - `develop` (develop branch) 
  - `v1.0.0`, `1.0`, `1` (semver tags)
  - `pr-123` (pull requests)
  - `{branch}-{sha}` (commit-based)
- **Build optimization**: GitHub Actions Cache for Docker layers (~70% faster builds)

### Docker Publishing Workflow
- **Registry**: GitHub Container Registry (ghcr.io)
- **Local commands**: `make publish`, `make build-for-ghcr`, `make login-ghcr`
- **Automatic extraction**: Git remote → user/repo for image naming
- **Security**: GitHub token-based authentication with `write:packages` scope

### Local Testing with act
- **act configured** for testing GitHub Actions locally
- **Colima integration** for Docker environment
- **Safe testing commands**: 
  - `make test-actions` - List workflows
  - `make test-docker-build` - Test Docker builds
  - `make test-pr-build` - Test PR workflows
- **Configuration files**: `.actrc`, `.secrets` for local testing

## Operations & Debugging

### Debug Command System
- **MCP debug tool**: `debug_exec_command` for container debugging
- **Safe command whitelist**: File system, system info commands only
- **Security features**: Timeout protection (30s), command logging, directory validation
- **Common use cases**: Memory system debugging, file system exploration, environment validation

### Container Operations
- **Multi-platform support**: Intel (amd64) and Apple Silicon (arm64)
- **Volume mounting**: `-v $(pwd):/workspace` pattern for project access
- **MCP server integration**: Docker run commands for Cursor MCP config

## Deployment Patterns

### Environment-based Deployment
- **Development**: Local builds with `make build-image`
- **Staging**: Push to `develop` → `develop` tag
- **Production**: Git tags `v*` → versioned images + `latest`
- **Testing**: Pull requests → build-only (no publish)

### CI/CD Trigger Strategy
| Event | Action | Result |
|-------|--------|--------|
| Push → main | Build + Publish | `latest` tag |
| Push → develop | Build + Publish | `develop` tag |
| Tag `v1.0.0` | Build + Publish | `v1.0.0`, `1.0`, `1` |
| Pull Request | Build only | `pr-{number}` |
| Any branch push | Build + Publish | `{branch}-{sha}` |

## 2025-06-17 16:18:09
## Additional Recurring Patterns

### Makefile Command Pattern
```makefile
# Consistent command structure across all operations
{operation}-{target}: prerequisite
	@command with --flags
	@echo "Success message"
```

### Docker Multi-stage Build Pattern
- **Base stage**: Common dependencies and setup
- **Development stage**: Additional dev tools and debugging
- **Production stage**: Minimal runtime environment

### Debug Command Safety Pattern
```python
SAFE_COMMANDS = ['ls', 'find', 'cat', 'head', 'tail', 'pwd', 'whoami']
if command.split()[0] not in SAFE_COMMANDS:
    await ctx.warn(f"Command {command} not in safe list")
```

### Container Registry Naming Convention
- **Format**: `{registry}/{owner}/{repository}:{tag}`
- **Auto-extraction**: Git remote URL → owner/repo extraction
- **Tag strategy**: Event-driven tagging for traceability

## DevOps Best Practices

### Local Development Workflow
1. **Code changes** → Test locally
2. **act testing** → Validate GitHub Actions
3. **Local build** → `make build-image`
4. **Integration test** → `make test-docker-build`
5. **Push to branch** → Automated CI/CD

### Troubleshooting Workflow
1. **Debug commands** → `make debug-memory-system`
2. **Container inspection** → `docker exec -it <container> bash`
3. **Log analysis** → GitHub Actions logs + local act logs
4. **Environment validation** → `whoami && pwd && env`

### Security Considerations
- **Token scoping**: `write:packages` for registry access
- **Command restrictions**: Safe-list approach for debug tools
- **Container isolation**: Mounted volumes with read-only where possible
- **Audit logging**: All debug commands logged with timestamps

## 2025-06-17 16:32:23
## Tool Architecture Update

### Memory Management Philosophy Change
- **Previous approach**: Direct file manipulation via `append_to_memory`
- **New approach**: Suggestion-based memory management via `suggest_memory_update`
- **Rationale**: User-controlled memory curation with AI assistance

### New Tool: suggest_memory_update
- **Purpose**: Returns formatted prompts suggesting memory additions
- **Benefits**: 
  - User maintains control over memory content
  - Transparent memory management process
  - Follows intelligent-memory.mdc principles
  - Enables review before consolidation
- **Response format**: Structured suggestion with target file, formatted content, and action guidance

### Memory Workflow Evolution
1. **AI identifies** patterns/insights worth remembering
2. **suggest_memory_update** generates formatted suggestion
3. **User reviews** and manually adds to memory files
4. **Memory system** maintains integrity through user curation
