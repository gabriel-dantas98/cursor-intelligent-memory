#!/usr/bin/env python

import os
import logging
import subprocess
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path
import glob
from datetime import datetime
from mcp.server.fastmcp import FastMCP, Context

try:
    from .prompts import get_memory_setup_prompt, get_memory_prompt
except ImportError:
    # When running directly, use absolute import
    from memory_mcp_server.prompts import get_memory_setup_prompt, get_memory_prompt

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

logger.info("Initializing Memory MCP Server")
mcp = FastMCP("Memory MCP")

@dataclass
class MemoryConfig:
    """Configuration for memory system paths."""
    base_path: str
    
    @property
    def short_term_path(self) -> str:
        return os.path.join(self.base_path, ".cursor", "memory", "short-term")
    
    @property
    def long_term_path(self) -> str:
        return os.path.join(self.base_path, ".cursor", "memory", "long-term")
    
    @property
    def rules_path(self) -> str:
        return os.path.join(self.base_path, ".cursor", "rules")

def get_memory_config() -> MemoryConfig:
    """Get memory configuration with environment variable or current working directory as base."""
    base_path = os.environ.get('CURSOR_MEMORY_BASE_PATH', os.getcwd())
    return MemoryConfig(base_path=base_path)

# Prompts are now imported from prompts.py module

@mcp.tool(description="Validates if the Cursor memory system directories exist and are properly configured. Returns setup status and guides next steps. Essential for determining if memory system initialization is needed.")
async def validate_memory_system(ctx: Context) -> Dict[str, Any]:
    """
    Validates if the Cursor memory system directories exist and are properly configured.
    
    Args:
        ctx: The MCP context.
        
    Returns:
        A dictionary containing validation status and guidance.
    """
    await ctx.info("Validating Cursor memory system setup")
    
    config = get_memory_config()
    await ctx.info(f"Memory system base path: {config.base_path}")
    
    # Check if directories exist
    short_term_exists = os.path.exists(config.short_term_path)
    long_term_exists = os.path.exists(config.long_term_path)
    rules_exists = os.path.exists(config.rules_path)
    
    # Check core files
    project_knowledge_exists = os.path.exists(os.path.join(config.long_term_path, "project-knowledge.md"))
    known_issues_exists = os.path.exists(os.path.join(config.long_term_path, "known-issues.md"))
    working_memory_exists = os.path.exists(os.path.join(config.short_term_path, "working-memory.md"))
    memory_rule_exists = os.path.exists(os.path.join(config.rules_path, "intelligent-memory.mdc"))
    
    is_configured = all([
        short_term_exists, long_term_exists, rules_exists,
        project_knowledge_exists, known_issues_exists, working_memory_exists
    ])
    
    status = {
        "configured": is_configured,
        "directories": {
            "short_term": short_term_exists,
            "long_term": long_term_exists,
            "rules": rules_exists
        },
        "core_files": {
            "project_knowledge": project_knowledge_exists,
            "known_issues": known_issues_exists,
            "working_memory": working_memory_exists,
            "memory_rule": memory_rule_exists
        },
        "base_path": config.base_path
    }
    
    if is_configured:
        await ctx.info("Memory system is fully configured and operational")
    else:
        missing_components = []
        if not short_term_exists:
            missing_components.append("short-term directory")
        if not long_term_exists:
            missing_components.append("long-term directory")
        if not project_knowledge_exists:
            missing_components.append("project-knowledge.md")
        if not known_issues_exists:
            missing_components.append("known-issues.md")
        if not working_memory_exists:
            missing_components.append("working-memory.md")
            
        await ctx.warning(f"Memory system incomplete - missing: {', '.join(missing_components)}")
    
    return status

@mcp.tool(description="Returns the appropriate prompt based on memory system status. If memory system exists, returns the active memory prompt. If not configured, returns the complete setup instructions. Use this to get the right guidance for the current state.")
async def get_memory_prompt_for_current_state(ctx: Context) -> Dict[str, Any]:
    """
    Returns the appropriate prompt based on memory system status.
    If configured, returns the active memory prompt. If not, returns setup instructions.
    
    Args:
        ctx: The MCP context.
        
    Returns:
        A dictionary containing the appropriate prompt and system status.
    """
    await ctx.info("Determining appropriate memory prompt for current state")
    
    # First validate the current state
    validation_result = await validate_memory_system(ctx)
    
    if validation_result["configured"]:
        await ctx.info("Memory system is configured - returning active memory prompt")
        prompt = get_memory_prompt()
        prompt_type = "active"
    else:
        await ctx.info("Memory system not configured - returning setup instructions")
        prompt = get_memory_setup_prompt()
        prompt_type = "setup"
    
    return {
        "prompt": prompt,
        "prompt_type": prompt_type,
        "system_status": validation_result
    }

@mcp.tool(description="Lists all available memory files in both short-term and long-term directories with their metadata. Shows file sizes, modification dates, and basic statistics. Essential for understanding what memory content is available for loading and consultation.")
async def list_memory_files(ctx: Context) -> Dict[str, Any]:
    """
    Lists all available memory files in both short-term and long-term directories.
    
    Args:
        ctx: The MCP context.
        
    Returns:
        A dictionary containing lists of memory files with metadata.
    """
    await ctx.info("Listing all available memory files")
    
    config = get_memory_config()
    
    def get_file_info(file_path: str) -> Dict[str, Any]:
        """Get metadata for a memory file."""
        try:
            stat = os.stat(file_path)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                line_count = len(content.splitlines())
                char_count = len(content)
            
            return {
                "path": file_path,
                "name": os.path.basename(file_path),
                "size_bytes": stat.st_size,
                "size_kb": round(stat.st_size / 1024, 2),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "line_count": line_count,
                "char_count": char_count,
                "exists": True
            }
        except Exception as e:
            return {
                "path": file_path,
                "name": os.path.basename(file_path),
                "error": str(e),
                "exists": False
            }
    
    # Get short-term memory files
    short_term_files = []
    if os.path.exists(config.short_term_path):
        for file_path in glob.glob(os.path.join(config.short_term_path, "*.md")):
            short_term_files.append(get_file_info(file_path))
    
    # Get long-term memory files
    long_term_files = []
    if os.path.exists(config.long_term_path):
        for file_path in glob.glob(os.path.join(config.long_term_path, "*.md")):
            long_term_files.append(get_file_info(file_path))
    
    # Get memory rules
    memory_rules = []
    if os.path.exists(config.rules_path):
        for file_path in glob.glob(os.path.join(config.rules_path, "*memory*.mdc")):
            memory_rules.append(get_file_info(file_path))
    
    total_files = len(short_term_files) + len(long_term_files) + len(memory_rules)
    total_size = sum(f.get("size_bytes", 0) for f in short_term_files + long_term_files + memory_rules if f.get("exists", False))
    
    await ctx.info(f"Found {total_files} memory files totaling {round(total_size/1024, 2)} KB")
    
    return {
        "short_term_files": short_term_files,
        "long_term_files": long_term_files,
        "memory_rules": memory_rules,
        "summary": {
            "total_files": total_files,
            "total_size_kb": round(total_size / 1024, 2),
            "short_term_count": len(short_term_files),
            "long_term_count": len(long_term_files),
            "rules_count": len(memory_rules)
        }
    }

@mcp.tool(description="Loads and returns the contents of specific memory files or all memory files if no specific files are requested. Essential for reading memory content into the current context. Supports both individual file loading and bulk loading for session initialization.")
async def load_memory_files(ctx: Context, file_names: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Loads and returns the contents of specific memory files or all memory files.
    
    Args:
        ctx: The MCP context.
        file_names: Optional list of specific file names to load. If None, loads all memory files.
        
    Returns:
        A dictionary containing the loaded memory file contents.
    """
    if file_names:
        await ctx.info(f"Loading specific memory files: {', '.join(file_names)}")
    else:
        await ctx.info("Loading all available memory files")
    
    config = get_memory_config()
    loaded_files = {}
    
    async def load_file_content(file_path: str, category: str) -> None:
        """Load content from a memory file."""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    file_name = os.path.basename(file_path)
                    loaded_files[file_name] = {
                        "content": content,
                        "category": category,
                        "path": file_path,
                        "size": len(content),
                        "lines": len(content.splitlines())
                    }
                    await ctx.debug(f"Loaded {file_name} ({len(content)} chars)")
        except Exception as e:
            await ctx.error(f"Failed to load {file_path}: {str(e)}")
    
    # If specific files requested, load only those
    if file_names:
        for file_name in file_names:
            # Try to find the file in short-term, long-term, or rules directories
            possible_paths = [
                os.path.join(config.short_term_path, file_name),
                os.path.join(config.long_term_path, file_name),
                os.path.join(config.rules_path, file_name)
            ]
            
            found = False
            for path in possible_paths:
                if os.path.exists(path):
                    if "short-term" in path:
                        await load_file_content(path, "short-term")
                    elif "long-term" in path:
                        await load_file_content(path, "long-term")
                    else:
                        await load_file_content(path, "rules")
                    found = True
                    break
            
            if not found:
                await ctx.warning(f"Memory file not found: {file_name}")
    
    else:
        # Load all memory files
        # Load short-term files
        if os.path.exists(config.short_term_path):
            for file_path in glob.glob(os.path.join(config.short_term_path, "*.md")):
                await load_file_content(file_path, "short-term")
        
        # Load long-term files
        if os.path.exists(config.long_term_path):
            for file_path in glob.glob(os.path.join(config.long_term_path, "*.md")):
                await load_file_content(file_path, "long-term")
        
        # Load memory rules
        if os.path.exists(config.rules_path):
            for file_path in glob.glob(os.path.join(config.rules_path, "*memory*.mdc")):
                await load_file_content(file_path, "rules")
    
    total_content = sum(f["size"] for f in loaded_files.values())
    total_lines = sum(f["lines"] for f in loaded_files.values())
    
    await ctx.info(f"Successfully loaded {len(loaded_files)} memory files - {total_content} chars, {total_lines} lines")
    
    return {
        "loaded_files": loaded_files,
        "summary": {
            "files_loaded": len(loaded_files),
            "total_characters": total_content,
            "total_lines": total_lines
        }
    }

@mcp.tool(description="Updates memory files - returns executable script")
async def memory_update(ctx: Context, file_name: str, content: str, add_timestamp: bool = True, memory_type: str = "short-term") -> Dict[str, Any]:
    """
    Returns an executable script for memory updates.
    """
    timestamp_prefix = ""
    if add_timestamp:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        timestamp_prefix = f"## {timestamp}\n"
    
    formatted_content = f"{timestamp_prefix}{content}"
    file_path = f".cursor/memory/{memory_type}/{file_name}"
    
    # Gerar script Python
    python_script = f'''#!/usr/bin/env python3
import os
from pathlib import Path

# Memory update script
file_path = "{file_path}"
content = """{formatted_content}"""

# Create directory if it doesn't exist
Path(file_path).parent.mkdir(parents=True, exist_ok=True)

# Append to file
mode = "a" if os.path.exists(file_path) else "w"
with open(file_path, mode) as f:
    if mode == "a" and os.path.getsize(file_path) > 0:
        f.write("\\n\\n")
    f.write(content)

print(f"✅ Memory updated: {{file_path}}")
'''
    
    # Gerar comando bash
    bash_command = f"""mkdir -p $(dirname "{file_path}") && cat >> "{file_path}" << 'EOF'

{formatted_content}
EOF"""
    
    return {
        "instruction": f"Run this script to update memory at {file_path}:",
        "python_script": python_script,
        "bash_command": bash_command,
        "file_path": file_path
    }

def main():
    """Main entry point for the Memory MCP server."""
    mcp.run()

if __name__ == "__main__":
    main() 
