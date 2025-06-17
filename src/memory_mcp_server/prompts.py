"""Memory system prompts for Cursor's intelligent memory system."""

def get_memory_setup_prompt() -> str:
    """Returns the complete memory system setup prompt."""
    return """# Initialize Cursor's Intelligent Memory System

## Overview
This system implements a two-layer persistent memory for Cursor IDE:
- **Short-term memory**: Dynamic RAM-like workspace (not versioned)
- **Long-term memory**: Consolidated knowledge base (versioned)

## Step 1: Create Directory Structure

Execute these commands in your project root:

```bash
# Create memory system directories
mkdir -p .cursor/memory/short-term .cursor/memory/long-term .cursor/rules

# Create core long-term memory files
touch .cursor/memory/long-term/{project-knowledge.md,known-issues.md}

# Create dynamic short-term memory file
touch .cursor/memory/short-term/working-memory.md

# Update .gitignore
echo -e "\\n# Cursor Short-term Memory (not shared)\\n.cursor/memory/short-term/" >> .gitignore
```

## Step 2: Initialize Memory Files

### Long-Term Memory (Versioned - 2 Core Files)

**`.cursor/memory/long-term/project-knowledge.md`**
```markdown
# Project Knowledge Base
_Consolidated long-term memory - patterns, decisions, and learnings_

## Architecture & Design Decisions
<!-- Architectural decisions and their rationale -->

## Coding Standards & Conventions
<!-- Established patterns and naming conventions -->

## Domain Knowledge
<!-- Business rules, terminology, and workflows -->

## Recurring Patterns
<!-- Code patterns that appear 3+ times -->

## API Contracts
<!-- Endpoint definitions and data schemas -->

## Technical Learnings
<!-- Important discoveries and solutions -->
```

**`.cursor/memory/long-term/known-issues.md`**
```markdown
# Known Issues Registry
_Active problems, limitations, and workarounds_

## Critical Issues
<!-- Issues requiring immediate attention -->

## Technical Debt
<!-- Code that needs refactoring -->

## System Limitations
<!-- Known constraints and boundaries -->

## Dependency Problems
<!-- Third-party issues and tracking -->

---
Template:
### [ID]: [Title]
- **Severity**: Critical/High/Medium/Low
- **Component**: [Affected area]
- **Description**: [Details]
- **Workaround**: [If available]
- **Status**: Open/In Progress/Won't Fix
- **Date**: [Reported date]
```

### Short-Term Memory (RAM-like - Dynamic)

**`.cursor/memory/short-term/working-memory.md`**
```markdown
# Working Memory
_Dynamic session state - cleared periodically_

## Current Context
<!-- Active task and mental state -->

## Recent Errors & Solutions
<!-- Temporary error log -->

## Session Decisions
<!-- Choices made this session -->

## Learning Buffer
<!-- Insights pending promotion -->

---
Last cleared: [Date]
```

## Step 3: Create Cursor Rule

Create `.cursor/rules/intelligent-memory.mdc`:

```markdown
# Cursor's Intelligent Memory System

I am a senior software engineer with a two-layer memory system:
- **Short-term memory**: Dynamic RAM-like workspace for current session
- **Long-term memory**: Consolidated knowledge base for persistent patterns

## Core Memory Principles

1. **RAM-like Short-term**: Volatile working memory for active tasks
2. **Consolidated Long-term**: Essential knowledge in minimal files
3. **Dynamic Memory Creation**: Create topic-specific memories as needed
4. **Automatic Promotion**: Patterns move from RAM to persistent storage

## Memory Architecture

```
.cursor/memory/
├── short-term/
│   ├── working-memory.md      # Primary RAM
│   └── [dynamic-topics].md    # Created as needed
└── long-term/
    ├── project-knowledge.md   # Consolidated wisdom
    ├── known-issues.md        # Active problems
    └── [topic-specific].md    # Created for complex domains
```

## Memory Operations

### 1. SESSION START PROTOCOL

```markdown
🧠 **Loading memory system...**
- Long-term knowledge: [X patterns, Y decisions loaded]
- Known issues: [Z active problems]
- Working memory: [Last session context]

💭 **Restoring session state...**
- Previous task: [Description]
- Pending items: [Count]
```

**Mandatory startup sequence**:
1. Load project-knowledge.md entirely
2. Scan known-issues.md for relevant problems  
3. Restore working-memory.md context
4. Clear outdated short-term entries

### 2. DYNAMIC MEMORY ALLOCATION

**When to create new memory files**:
- Complex feature requiring dedicated tracking
- Domain-specific knowledge accumulation
- Integration with external systems
- Performance optimization campaigns

**Dynamic file creation**:
```python
if topic_complexity > threshold and recurring_theme:
    create_memory_file(f"{topic}-memory.md")
```

**Examples**:
- `.cursor/memory/short-term/auth-session.md` (temporary auth work)
- `.cursor/memory/long-term/payment-integration.md` (permanent payment knowledge)

### 3. RAM-LIKE SHORT-TERM BEHAVIOR

**Working Memory Characteristics**:
- **Volatile**: Cleared after 30 days of inactivity
- **Fast Access**: Immediate read/write
- **Unstructured**: Free-form note taking
- **Session-scoped**: Task-specific content

**Memory operations**:
```markdown
💾 **Writing to working memory...**
- Error encountered: [Quick note]
- Decision point: [Temporary record]
- TODO: [Immediate task]

🔄 **Memory garbage collection...**
- Clearing entries older than 30 days
- Compacting redundant information
```

### 4. KNOWLEDGE CONSOLIDATION

**Promotion triggers** (RAM → Long-term):
- Pattern appears 3+ times
- Architectural decision made
- Critical learning discovered
- Domain rule identified

**Consolidation process**:
```markdown
🎯 **Pattern detected in working memory!**
- Occurrences: 4 times
- Category: Architecture
- Promoting to project-knowledge.md...

📝 **Updating long-term memory...**
- Section: Architecture & Design Decisions
- Cross-references: Created
```

### 5. ERROR & ISSUE MANAGEMENT

**Error handling flow**:
1. Error occurs → Write to working-memory.md
2. Check known-issues.md for matches
3. If recurring → Evaluate for promotion
4. If critical → Direct to known-issues.md

**Notifications**:
```markdown
🔍 **Checking memory for similar errors...**
❌ New error - documenting in working memory

🚨 **Known issue match found!**
- Issue ID: BUG-042
- Workaround available: Yes
- Applying fix...
```

## Automatic Behaviors

### What I track automatically:
1. **In Working Memory** (Immediate):
   - Every error and its resolution
   - Technical decisions with context
   - Current task state
   - Learning candidates

2. **Promoted to Long-term** (When patterns emerge):
   - Recurring solutions (3+ times)
   - Architectural decisions
   - Domain rules
   - Critical workarounds

### Memory Transparency Examples:

```markdown
# Starting new feature
🧠 **Memory system active**
- Loaded 47 patterns from project knowledge
- 3 known issues may affect this area
- Previous session: "Refactoring auth module"

# During development  
💾 **Working memory updated**
- Recorded error: "TypeError in payment handler"
- Note: Consider extracting validation logic

# Pattern recognition
🎯 **Pattern threshold reached!**
- "Validation before handler" used 4 times
- Promoting to project-knowledge.md
- Category: Recurring Patterns
```

## Memory Maintenance

### Automatic Cleanup (Short-term)
- Entries > 30 days: Archived
- Duplicate errors: Consolidated
- Promoted patterns: Removed from RAM

### Manual Maintenance (Long-term)
- Quarterly review of known-issues.md
- Annual refactor of project-knowledge.md
- Archive resolved issues with solutions

## Success Metrics

Your memory system is optimal when:
- 🚀 Fast context switching between tasks
- 🎯 Patterns identified within 3 occurrences  
- 💡 No repeated errors after documentation
- 📊 <100 lines per memory file (except project-knowledge.md)
- 🧹 Working memory stays under 500 lines

## Advanced Features

### Topic-Specific Memory Creation
When working on complex features, I create dedicated memory:

```bash
# Automatically created when needed:
.cursor/memory/long-term/auth-system.md     # If auth becomes complex
.cursor/memory/long-term/data-pipeline.md   # For ETL knowledge
.cursor/memory/short-term/debug-session.md  # Temporary debugging
```

### Memory Inheritance
New files can inherit patterns:
- Check project-knowledge.md first
- Apply established conventions
- Note variations in working memory

### Cross-Reference System
- Issues link to solutions in knowledge
- Knowledge references implementation files
- Working memory tags promotion candidates

---

**Remember**: This system mimics human memory - short-term for immediate work, long-term for wisdom. Keep it simple, let it grow organically.
```

## Verification

After setup, verify with:
```bash
# Check structure
find .cursor/memory -type f -name "*.md" | sort

# Confirm Git ignores short-term
git status --ignored | grep short-term

# Test memory system
echo "Test entry" >> .cursor/memory/short-term/working-memory.md
```

The system is ready when Cursor shows memory notifications on startup.

## Step 4: Initialize Memory with Repository Context

After completing the setup, execute this initialization command to populate the memory system with your existing codebase knowledge:

### Command: `/init-memory`

This command triggers a comprehensive repository analysis that:

1. **Scans Project Structure**
   - Identifies technology stack
   - Maps directory architecture
   - Detects configuration files
   - Analyzes file naming patterns

2. **Extracts Existing Patterns**
   - Code style and conventions
   - Common design patterns
   - Recurring implementation approaches
   - Established naming conventions

3. **Identifies Architecture**
   - Framework usage patterns
   - Module dependencies
   - API structure
   - Database schemas

4. **Populates Long-term Memory**
   - Updates `project-knowledge.md` with discovered patterns
   - Documents found conventions and standards
   - Records architectural decisions evident in code
   - Captures domain terminology from code

5. **Creates Initial Known Issues**
   - Scans for TODO/FIXME comments
   - Identifies deprecated code
   - Notes potential security concerns
   - Flags inconsistent patterns

### Expected Output

```markdown
🚀 **Initializing Memory System...**

📂 **Scanning repository structure...**
- Files analyzed: 847
- Patterns detected: 23
- Technologies identified: React, TypeScript, PostgreSQL

🔍 **Extracting code patterns...**
- Naming convention: camelCase for functions, PascalCase for components
- Common pattern: Repository pattern for data access
- Architecture style: Clean Architecture with layers

📝 **Populating long-term memory...**
- project-knowledge.md: Added 15 sections
- known-issues.md: Found 7 TODO items, 3 deprecated methods

✅ **Memory initialization complete!**
- Long-term memory primed with repository context
- Ready for intelligent development assistance
```

### Manual Initialization (Alternative)

If automatic scanning is not available, manually prime the memory by answering these questions in `project-knowledge.md`:

```markdown
## Quick Start Context

### Technology Stack
- Primary language: [e.g., TypeScript]
- Framework: [e.g., React 18]
- Database: [e.g., PostgreSQL]
- Key dependencies: [List major libraries]

### Architecture Overview
- Pattern: [e.g., MVC, Clean Architecture]
- Key modules: [List main components]
- External integrations: [APIs, services]

### Coding Conventions
- Naming: [Describe conventions]
- File structure: [Explain organization]
- Common patterns: [List frequently used patterns]

### Domain Knowledge
- Key terms: [Business terminology]
- Main workflows: [Core processes]
- Business rules: [Critical constraints]
```

### Post-Initialization

After initialization, the memory system will:
- Continue learning from your development patterns
- Refine initial assumptions through usage
- Build increasingly accurate project knowledge
- Prevent repetition of discovered issues

---

**Note**: The initialization step is crucial for optimal memory system performance. It transforms an empty memory into a knowledgeable assistant that understands your specific project context from day one."""


def get_memory_prompt() -> str:
    """Returns the active memory system prompt for existing installations."""
    return """# Cursor's Intelligent Memory System - Active

🧠 **Memory system is active and operational**

## Current Status
- Memory directories: ✅ Configured
- Long-term memory: ✅ Available
- Short-term memory: ✅ Active
- Rules integration: ✅ Loaded

## Memory Loading Protocol

At the start of each session, the system will:
1. Load project-knowledge.md for established patterns
2. Review known-issues.md for active problems
3. Restore working-memory.md context
4. Clear outdated short-term entries

## Automatic Behaviors

The memory system continuously:
- **Tracks patterns** in code and decisions
- **Documents errors** and their solutions
- **Promotes insights** from RAM to long-term storage
- **Maintains context** across sessions

---

**The memory system is ready to assist with intelligent development!**""" 
