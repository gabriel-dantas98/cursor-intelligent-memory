#!/usr/bin/env python3
"""Test script for Memory MCP server tool discovery."""

import asyncio
from src.memory_mcp_server.server import mcp

async def test_discovery():
    """Test the discovery of MCP tools."""
    print("🔍 Testing Memory MCP server tool discovery...")
    
    tools = await mcp.list_tools()
    print(f"📋 Found {len(tools)} tools:")
    
    for tool in tools:
        print(f"  🔧 {tool.name}")
        print(f"     Description: {tool.description}")
        if tool.inputSchema and 'properties' in tool.inputSchema:
            params = list(tool.inputSchema['properties'].keys())
            print(f"     Parameters: {', '.join(params)}")
        print()
    
    print("✅ Tool discovery test completed successfully!")

if __name__ == "__main__":
    asyncio.run(test_discovery()) 
