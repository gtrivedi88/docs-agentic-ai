# Working with AI: Complete Prompt Library for Lyra Implementation
## Copy-Paste Ready Prompts for Every Sprint

**Purpose**: Complete, exhaustive prompts you can copy-paste directly to implement Lyra. No placeholders - everything filled in.

**How to use**: Copy the prompt for your current sprint, paste it to your AI, and follow the instructions.

---

## 📋 Quick Reference

| Sprint | Prompt Section | What It Does |
|--------|---------------|--------------|
| **Sprint 1** | [Section 1](#sprint-1-complete-prompts) | Release notes (Jira + GitHub) |
| **Sprint 2** | [Section 2](#sprint-2-complete-prompts) | Add Confluence |
| **Sprint 3** | [Section 3](#sprint-3-complete-prompts) | Add Audit capability |
| **Sprint 4** | [Section 4](#sprint-4-complete-prompts) | Add Help docs |
| **Sprint 5** | [Section 5](#sprint-5-complete-prompts) | Add GitLab, Slack, Google Docs |
| **Sprint 6** | [Section 6](#sprint-6-complete-prompts) | Complete CRUD |

---

## Sprint 1: Complete Prompts

### SPRINT 1 - KICKOFF PROMPT

**Copy-paste this to start Sprint 1**:

```
=== SPRINT 1: CORE RELEASE NOTES (FOUNDATION) ===

I'm starting Sprint 1 of Lyra Phase 1 implementation.

REFERENCE DOCUMENTS:
- @phase1_implementation_plan.md (5650 lines) - Complete code reference
- @phase1_incremental_sprints.md (1312 lines) - Sprint execution order

SPRINT 1 GOAL:
Create a working end-to-end release notes generator using ONLY Jira and GitHub data sources.

SPRINT 1 SCOPE (from phase1_incremental_sprints.md, lines 64-724):

FILES TO IMPLEMENT:
1. Phase 0 - Scaffolding (from reference plan):
   - Directory structure
   - pyproject.toml (lines 232-302)
   - .env.example (lines 306-358)
   - src/config/settings.py (lines 362-452)
   - src/utils/logger.py (lines 456-521)
   - src/__init__.py (lines 525-529)
   - .gitignore (lines 596-655)
   - src/schemas/data_models.py (lines 672-815)

2. Tools Layer - Jira + GitHub ONLY:
   - src/tools/base_tool.py (lines 817-904)
   - src/tools/jira_tool.py (lines 906-1167)
   - src/tools/github_tool.py (lines 1169-1437)
   - src/tools/smart_tools.py (lines 2081-2375) - Jira + GitHub only
   - src/tools/tool_registry.py (lines 2046-2158) - Sprint 1 version (11 tools only)

3. Knowledge Service - Basic:
   - src/services/vector_store.py (lines 2547-2696)
   - src/services/knowledge_service.py (lines 2698-2840) - Simplified Sprint 1 version

4. Agent Core - Complete (All 4 Nodes):
   - src/schemas/agent_state.py (lines 2851-2895)
   - src/agents/node_utils.py (lines 2897-2987)
   - src/agents/planner_node.py (lines 2989-3070)
   - src/agents/executor_node.py (lines 3072-3160)
   - src/agents/synthesizer_node.py (lines 3162-3248)
   - src/agents/critic_node.py (lines 3250-3346)
   - src/agents/controller.py (lines 3348-3480)
   - src/utils/metrics.py (lines 3482-3529)

5. Operations - Release Notes Only:
   - src/operations/doc_creator.py (lines 3584-3777) - create_release_notes method ONLY

6. CLI - Create Command Only:
   - src/main.py (lines 4189-4419) - create-release-notes command ONLY

7. Templates:
   - data/templates/release_notes.md (lines 4760-4820)

SPRINT 1 CONSTRAINTS:
❌ DO NOT implement: Confluence, GitLab, Slack, Google Docs tools
❌ DO NOT implement: Update, delete, audit operations  
❌ DO NOT implement: Help docs, API docs, tutorials
✅ ONLY implement: Jira + GitHub tools for release notes

SPRINT 1 EXPECTED OUTCOME:
After completion, this command should work:
`lyra create-release-notes v2.1 --project=openshift`

And it should:
- Search Jira for tickets in release v2.1
- Find related GitHub PRs
- Use smart tools to distill knowledge
- Generate release notes markdown file
- Save to: ./outputs/generated_docs/openshift/release_notes/v2.1.md

IMPLEMENTATION RULES:
1. Use EXACT code from phase1_implementation_plan.md at the line numbers specified above
2. Do NOT modify, optimize, or improve any code
3. Copy character-for-character from reference
4. For Sprint 1 versions (tool_registry, knowledge_service), use simplified versions from phase1_incremental_sprints.md
5. If you find a discrepancy, STOP and ask me

READY TO START:
Let's implement file by file in order.

First file: Create directory structure and pyproject.toml

Confirm you understand Sprint 1 scope before proceeding.
```

---

### SPRINT 1 - FILE 1: SCAFFOLDING PROMPT

**Copy-paste this after kickoff confirmed**:

```
=== SPRINT 1 - FILE 1: Project Scaffolding ===

Create the complete project directory structure and pyproject.toml.

STEP 1: Create Directory Structure

Run this command to create all directories:

mkdir -p lyra-agent/{data/{existing_docs,templates,vector_db,cache},notebooks,tests/{unit,integration,fixtures},src/{config,schemas,tools,services,agents,operations,utils},outputs/{generated_docs,logs,reports}}

STEP 2: Create pyproject.toml

Reference: @phase1_implementation_plan.md lines 232-302

Use EXACT content from those lines. This includes:
- All dependencies (langchain, langgraph, langchain-mistralai, jira, PyGithub, etc.)
- All configuration
- No modifications

Create the file and show me:
- First 20 lines
- Last 10 lines
- Total line count (should be ~71 lines)

After I verify, we'll move to .env.example
```

---

### SPRINT 1 - FILE 2: ENVIRONMENT CONFIG

```
=== SPRINT 1 - FILE 2: .env.example ===

Create the environment configuration template.

Reference: @phase1_implementation_plan.md lines 306-358

Use EXACT content from those lines.

This file includes placeholders for:
- PROJECT_NAME, PROJECT_KEY
- MISTRAL_API_KEY, MISTRAL_MODEL
- JIRA_SERVER, JIRA_USER, JIRA_API_TOKEN
- GITHUB_TOKEN, GITHUB_ORG, GITHUB_REPOS
- And all other configurations (including ones we won't use until later sprints)

NOTE: We include ALL config variables now (even for Confluence, Slack, etc.) 
even though we only use Jira/GitHub in Sprint 1. This is by design.

Create the file and show me:
- First 15 lines
- Total line count (should be ~53 lines)
```

---

### SPRINT 1 - FILE 3: SETTINGS

```
=== SPRINT 1 - FILE 3: src/config/settings.py ===

Create the Pydantic settings class.

Reference: @phase1_implementation_plan.md lines 362-452

Use EXACT content from those lines.

This includes:
- Settings class with all fields
- All data source configurations
- Computed properties for parsing comma-separated values
- Global settings instance

Create the file and show me:
- First 30 lines (imports + start of Settings class)
- Lines with computed properties
- Total line count (should be ~91 lines)
```

---

### SPRINT 1 - FILE 4: LOGGER

```
=== SPRINT 1 - FILE 4: src/utils/logger.py ===

Create the logging utility with Rich formatting.

Reference: @phase1_implementation_plan.md lines 456-521

Use EXACT content from those lines.

Includes:
- setup_logger function
- RichHandler for console
- FileHandler for log files
- Global logger instance

Create the file and show me:
- First 20 lines
- Total line count (should be ~66 lines)
```

---

### SPRINT 1 - FILE 5: DATA MODELS

```
=== SPRINT 1 - FILE 5: src/schemas/data_models.py ===

Create ALL Pydantic data models.

Reference: @phase1_implementation_plan.md lines 672-815

Use EXACT content from those lines.

This includes models for:
- SourceReference
- JiraTicket, JiraComment
- GitHubPR
- ConfluencePage (for later sprints)
- SlackMessage (for later sprints)
- GoogleDoc (for later sprints)
- Citation
- DocDraft
- AuditResult

NOTE: We create ALL models now even though Sprint 1 only uses Jira and GitHub.
This is intentional - saves refactoring later.

Create the file and show me:
- First 30 lines
- The JiraTicket model (should start around line 695)
- Total line count (should be ~144 lines)
```

---

### SPRINT 1 - FILE 6: BASE TOOL

```
=== SPRINT 1 - FILE 6: src/tools/base_tool.py ===

Create the base tool class with caching.

Reference: @phase1_implementation_plan.md lines 817-904

Use EXACT content from those lines.

Includes:
- BaseTool abstract class
- _cache_key method
- _get_cached method
- _set_cached method
- _handle_error method

Create the file and show me:
- First 25 lines
- The _cache_key method
- Total line count (should be ~88 lines)
```

---

### SPRINT 1 - FILE 7: JIRA TOOL

```
=== SPRINT 1 - FILE 7: src/tools/jira_tool.py ===

Create the complete Jira tool with comment reading and link following.

Reference: @phase1_implementation_plan.md lines 906-1167

Use EXACT content from those lines.

This is a large file (~262 lines) that includes:
- JiraTool class with:
  - search_tickets
  - get_ticket_details
  - get_tickets_for_release
  - follow_linked_issues
  - _issue_to_model (parses comments!)
- LangChain tool wrappers:
  - search_jira_tickets
  - get_jira_ticket
  - get_jira_release_tickets
  - get_linked_jira_tickets

CRITICAL: This tool MUST read Jira comments (see _issue_to_model method)

Create the file and show me:
- First 30 lines
- The get_ticket_details method (around line 985-1010)
- The _issue_to_model method (includes comment parsing)
- Total line count (should be ~262 lines)
```

---

### SPRINT 1 - FILE 8: GITHUB TOOL

```
=== SPRINT 1 - FILE 8: src/tools/github_tool.py ===

Create the complete GitHub tool.

Reference: @phase1_implementation_plan.md lines 1169-1437

Use EXACT content from those lines.

Includes (~269 lines):
- GitHubTool class with:
  - search_prs
  - get_pr_details
  - find_prs_for_ticket
  - get_file_content
  - check_file_exists
  - _pr_to_model
- LangChain tool wrappers:
  - search_github_prs
  - get_github_pr
  - find_github_prs_for_ticket
  - check_github_file_exists

Create the file and show me:
- First 30 lines
- The find_prs_for_ticket method
- Total line count (should be ~269 lines)
```

---

### SPRINT 1 - FILE 9: SMART TOOLS (SPRINT 1 VERSION)

```
=== SPRINT 1 - FILE 9: src/tools/smart_tools.py (Sprint 1 Version) ===

Create smart tools for Jira + GitHub ONLY.

IMPORTANT: This is a SIMPLIFIED version for Sprint 1.

Reference: @phase1_incremental_sprints.md lines 114-330

Use EXACT content from those lines for Sprint 1 version.

This version includes:
- SmartToolOrchestrator class with ONLY:
  - distill_ticket_decision (Jira)
  - distill_pr_impact (GitHub)
  - get_release_knowledge (Jira + GitHub)
- Three LangChain tool wrappers:
  - get_smart_release_knowledge
  - get_ticket_decision_summary
  - get_pr_impact_summary

DO NOT include Confluence distillation (that's Sprint 2).

Create the file and show me:
- First 30 lines
- The distill_ticket_decision method
- The get_release_knowledge method
- Total line count (should be ~217 lines for Sprint 1 version)
```

---

### SPRINT 1 - FILE 10: TOOL REGISTRY (SPRINT 1 VERSION)

```
=== SPRINT 1 - FILE 10: src/tools/tool_registry.py (Sprint 1 Version) ===

Create tool registry with Jira + GitHub tools ONLY.

IMPORTANT: This is Sprint 1 version - simplified.

Reference: @phase1_incremental_sprints.md lines 332-384

Use EXACT content from those lines.

This version should have:
- Imports for Jira tools only (4 tools)
- Imports for GitHub tools only (4 tools)
- Imports for smart tools (3 tools)
- get_all_tools() returning exactly 11 tools

DO NOT import: Confluence, GitLab, Slack, Google Docs tools yet.

Expected tools count: 11 (3 smart + 4 Jira + 4 GitHub)

Create the file and show me:
- All imports
- The get_all_tools() function showing all 11 tools
- Total line count (should be ~28 lines for Sprint 1)
- Confirm: Exactly 11 tools, no more, no less
```

---

### SPRINT 1 - FILE 11: VECTOR STORE SERVICE

```
=== SPRINT 1 - FILE 11: src/services/vector_store.py ===

Create vector store service with ChromaDB.

Reference: @phase1_implementation_plan.md lines 2547-2696

Use EXACT content from those lines.

Includes:
- VectorStoreService class
- index_documents method
- search method
- clear_source method

Create the file and show me:
- First 30 lines
- The search method
- Total line count (should be ~150 lines)
```

---

### SPRINT 1 - FILE 12: KNOWLEDGE SERVICE (SPRINT 1 VERSION)

```
=== SPRINT 1 - FILE 12: src/services/knowledge_service.py (Sprint 1 Version) ===

Create SIMPLIFIED knowledge service for Sprint 1.

IMPORTANT: Use Sprint 1 version from incremental sprints doc.

Reference: @phase1_incremental_sprints.md lines 406-459

Use EXACT content from those lines.

This simplified version includes:
- index_existing_docs method (for style examples)
- get_style_examples method
- Does NOT include index_jira_data or search_knowledge yet

Create the file and show me:
- The complete class (should be small ~54 lines)
- All methods
- Confirm: Only has index_existing_docs and get_style_examples
```

---

### SPRINT 1 - FILE 13: AGENT STATE

```
=== SPRINT 1 - FILE 13: src/schemas/agent_state.py ===

Create the LangGraph agent state definition.

Reference: @phase1_implementation_plan.md lines 2851-2895

Use EXACT content from those lines.

Includes:
- AgentState TypedDict with all fields
- Annotated fields for LangGraph reducers

Create the file and show me:
- The complete AgentState class
- Total line count (should be ~45 lines)
```

---

### SPRINT 1 - FILE 14: NODE UTILITIES

```
=== SPRINT 1 - FILE 14: src/agents/node_utils.py ===

Create shared utility functions for agent nodes.

Reference: @phase1_implementation_plan.md lines 2897-2987

Use EXACT content from those lines.

Includes helper functions:
- load_prompts()
- summarize_knowledge()
- format_knowledge_for_synthesis()
- extract_title_from_content()
- has_enough_knowledge()

Create the file and show me:
- First 20 lines
- All function names
- Total line count (should be ~91 lines)
```

---

### SPRINT 1 - FILE 15: PLANNER NODE

```
=== SPRINT 1 - FILE 15: src/agents/planner_node.py ===

Create the planner node (decides what info to gather).

Reference: @phase1_implementation_plan.md lines 2989-3070

Use EXACT content from those lines.

Includes:
- Module-level LLM initialization
- planner_node function
- Decision logic for next action

Create the file and show me:
- First 30 lines (imports + initialization)
- The planner_node function signature and return
- Total line count (should be ~82 lines)
```

---

### SPRINT 1 - FILE 16: EXECUTOR NODE

```
=== SPRINT 1 - FILE 16: src/agents/executor_node.py ===

Create the executor node (runs tool calls).

Reference: @phase1_implementation_plan.md lines 3072-3160

Use EXACT content from those lines.

Includes:
- Module-level tools initialization
- executor_node function
- Tool execution logic with error handling

Create the file and show me:
- The executor_node function
- Error handling section
- Total line count (should be ~89 lines)
```

---

### SPRINT 1 - FILE 17: SYNTHESIZER NODE

```
=== SPRINT 1 - FILE 17: src/agents/synthesizer_node.py ===

Create the synthesizer node (generates documentation).

Reference: @phase1_implementation_plan.md lines 3162-3248

Use EXACT content from those lines.

Includes:
- Module-level LLM initialization (temperature 0.3 for creative writing)
- synthesizer_node function
- Draft creation logic

Create the file and show me:
- The synthesizer_node function
- Draft creation section
- Total line count (should be ~87 lines)
```

---

### SPRINT 1 - FILE 18: CRITIC NODE

```
=== SPRINT 1 - FILE 18: src/agents/critic_node.py ===

Create the critic node (reviews quality).

Reference: @phase1_implementation_plan.md lines 3250-3346

Use EXACT content from those lines.

Includes:
- Module-level LLM initialization (temperature 0.1 for consistent critique)
- critic_node function
- Quality scoring logic

Create the file and show me:
- The critic_node function
- Approval logic
- Total line count (should be ~97 lines)
```

---

### SPRINT 1 - FILE 19: CONTROLLER

```
=== SPRINT 1 - FILE 19: src/agents/controller.py ===

Create the controller (graph assembler).

Reference: @phase1_implementation_plan.md lines 3348-3480

Use EXACT content from those lines.

This is the SIMPLIFIED controller that just assembles the graph.
All node logic is in separate files.

Includes:
- Routing functions (route_after_planning, route_after_synthesis, route_after_critique)
- create_lyra_agent() function that wires everything together

Create the file and show me:
- All routing functions
- The create_lyra_agent function showing graph assembly
- Total line count (should be ~133 lines)
```

---

### SPRINT 1 - FILE 20: METRICS

```
=== SPRINT 1 - FILE 20: src/utils/metrics.py ===

Create metrics tracking utility.

Reference: @phase1_implementation_plan.md lines 3482-3529

Use EXACT content from those lines.

Includes:
- AgentMetrics dataclass
- Duration property
- log_summary method

Create the file and show me:
- The complete AgentMetrics class
- Total line count (should be ~48 lines)
```

---

### SPRINT 1 - FILE 21: DOC CREATOR (SPRINT 1 VERSION)

```
=== SPRINT 1 - FILE 21: src/operations/doc_creator.py (Sprint 1 Version) ===

Create document creator with ONLY create_release_notes method.

IMPORTANT: Sprint 1 version - simplified.

Reference: @phase1_incremental_sprints.md lines 462-541

Use EXACT content from those lines.

This version includes:
- DocumentCreator class
- create_release_notes method ONLY
- _save_draft method
- DO NOT include: create_help_doc, create_api_reference yet

Create the file and show me:
- The class initialization
- The create_release_notes method
- Total line count (should be ~79 lines for Sprint 1)
- Confirm: Only has create_release_notes, no other create methods
```

---

### SPRINT 1 - FILE 22: CLI (SPRINT 1 VERSION)

```
=== SPRINT 1 - FILE 22: src/main.py (Sprint 1 Version) ===

Create CLI with ONLY create-release-notes command.

IMPORTANT: Sprint 1 version - simplified.

Reference: @phase1_incremental_sprints.md lines 545-623

Use EXACT content from those lines.

This version includes:
- Typer app setup
- create_release_notes command ONLY
- version command
- DO NOT include: update, delete, audit commands yet

Create the file and show me:
- The imports (should only import doc_creator, not doc_updater, doc_deleter, doc_auditor)
- The create_release_notes command
- Total line count (should be ~78 lines for Sprint 1)
- Confirm: Only has create_release_notes and version commands
```

---

### SPRINT 1 - FILE 23: RELEASE NOTES TEMPLATE

```
=== SPRINT 1 - FILE 23: data/templates/release_notes.md ===

Create release notes template.

Reference: @phase1_incremental_sprints.md lines 625-664 (or @phase1_implementation_plan.md lines 4760-4820)

Use EXACT content.

This is the template the synthesizer will use as a style reference.

Create the file and show me:
- First 20 lines
- Total line count
```

---

### SPRINT 1 - FILE 24: PROMPTS CONFIG

```
=== SPRINT 1 - FILE 24: src/config/prompts.yaml ===

Create all agent prompts.

Reference: @phase1_implementation_plan.md lines 5138-5225

Use EXACT content from those lines.

Includes prompts for:
- controller_system_prompt
- planner_prompt
- synthesizer_prompt
- critic_prompt
- audit_prompt (for later)

Create the file and show me:
- The controller_system_prompt
- The synthesizer_prompt
- Total line count
```

---

### SPRINT 1 - FILE 25-28: INIT FILES

```
=== SPRINT 1 - FILES 25-28: __init__.py files ===

Create empty __init__.py files in:
- src/tools/__init__.py
- src/services/__init__.py
- src/agents/__init__.py
- src/operations/__init__.py
- src/config/__init__.py
- src/schemas/__init__.py
- src/utils/__init__.py
- tests/__init__.py

These can be empty or contain:
```python
"""Module docstring."""
```

Create all these files.
```

---

### SPRINT 1 - TESTING PROMPT

```
=== SPRINT 1 - TESTING ===

Create Sprint 1 test file.

Reference: @phase1_incremental_sprints.md lines 666-704

Create: tests/test_sprint1.py

This includes:
- test_create_release_notes_basic
- test_tools_loaded (should verify exactly 11 tools)
- test_agent_graph_creates

After creating, run: pytest tests/test_sprint1.py

Expected results:
- test_tools_loaded should PASS (verifies 11 tools)
- test_agent_graph_creates should PASS
- test_create_release_notes_basic might fail (needs credentials)

Show me test results.
```

---

### SPRINT 1 - COMPLETION VERIFICATION PROMPT

```
=== SPRINT 1 - COMPLETION VERIFICATION ===

Sprint 1 implementation complete. Let's verify everything.

VERIFICATION CHECKLIST:

1. File Count Check:
   Expected: ~28 files created
   Count your files in:
   - src/config/ (2 files: settings.py, prompts.yaml)
   - src/schemas/ (2 files: data_models.py, agent_state.py)
   - src/tools/ (4 files: base_tool.py, jira_tool.py, github_tool.py, smart_tools.py, tool_registry.py = 5)
   - src/services/ (2 files: vector_store.py, knowledge_service.py)
   - src/agents/ (6 files: node_utils.py, planner_node.py, executor_node.py, synthesizer_node.py, critic_node.py, controller.py)
   - src/operations/ (1 file: doc_creator.py)
   - src/utils/ (2 files: logger.py, metrics.py)
   - src/ (1 file: main.py, __init__.py = 2)
   - data/templates/ (1 file: release_notes.md)
   - Plus __init__.py files and config files

2. Tool Count Check:
   Run this Python code:
   ```python
   from src.tools.tool_registry import get_all_tools
   tools = get_all_tools()
   print(f"Total tools: {len(tools)}")
   print("Tool names:", [t.name for t in tools])
   ```
   
   Expected: Exactly 11 tools
   - 3 smart tools (get_smart_release_knowledge, get_ticket_decision_summary, get_pr_impact_summary)
   - 4 Jira tools (search_jira_tickets, get_jira_ticket, get_jira_release_tickets, get_linked_jira_tickets)
   - 4 GitHub tools (search_github_prs, get_github_pr, find_github_prs_for_ticket, check_github_file_exists)

3. Agent Graph Check:
   Run this:
   ```python
   from src.agents.controller import create_lyra_agent
   graph = create_lyra_agent()
   print("Agent created successfully")
   ```
   
   Expected: No errors

4. CLI Check:
   Run: lyra --help
   Expected: Shows help with create-release-notes command

5. SUCCESS CRITERIA (from phase1_incremental_sprints.md lines 706-713):
   ✅ Can run: lyra create-release-notes v2.1 --project=openshift (or shows proper error if no credentials)
   ✅ Agent uses: Jira and GitHub tools (verified in step 2)
   ✅ Smart tools work: Distills decisions and PR impacts (if you have test credentials, try it)
   ✅ Output: Readable markdown release notes
   ✅ No errors: Clean execution end-to-end

DECISION:
- All checks pass → Ready for Sprint 2
- Any checks fail → Debug before proceeding

Report results for each check.
```

---

## Sprint 2: Complete Prompts

### SPRINT 2 - KICKOFF PROMPT

```
=== SPRINT 2: ADD CONFLUENCE INTELLIGENCE ===

PREREQUISITE CHECK:
Sprint 1 MUST be complete and working before starting Sprint 2.

Verify Sprint 1:
- Run: pytest tests/test_sprint1.py
- Run: lyra create-release-notes v2.1 --project=openshift
- Both should work (or fail gracefully with credential errors, not code errors)

If Sprint 1 has ANY code errors → Fix them first before Sprint 2.

SPRINT 2 GOAL:
Add Confluence as a data source for better style consistency in release notes.

SPRINT 2 SCOPE (from phase1_incremental_sprints.md, lines 728-881):

FILES TO ADD/MODIFY:
1. NEW: src/tools/confluence_tool.py
2. MODIFY: src/tools/smart_tools.py (add Confluence distillation)
3. MODIFY: src/tools/tool_registry.py (add Confluence tools)
4. MODIFY: src/services/knowledge_service.py (add Confluence indexing)

WHAT NOT TO TOUCH:
❌ Do NOT modify: Jira tool, GitHub tool (already working)
❌ Do NOT add: GitLab, Slack, Google Docs yet
❌ Do NOT add: Audit, update, delete operations yet

EXPECTED OUTCOME:
After Sprint 2:
- Tool count: 14 (was 11, adding 3 Confluence tools)
- Agent can search Confluence for existing docs
- Release notes have better style consistency

Let's implement file by file.

First: Create src/tools/confluence_tool.py

Confirm you understand Sprint 2 scope before proceeding.
```

---

### SPRINT 2 - FILE 1: CONFLUENCE TOOL

```
=== SPRINT 2 - FILE 1: src/tools/confluence_tool.py ===

Create Confluence tool for searching pages and reading content.

Reference: @phase1_implementation_plan.md lines 1439-1625

Use EXACT content from those lines.

Includes (~187 lines):
- ConfluenceTool class with:
  - search_pages
  - get_page_details
  - get_pages_in_space
- LangChain tool wrappers:
  - search_confluence_pages
  - get_confluence_page

Create the file and show me:
- First 30 lines
- The search_pages method
- Total line count (should be ~187 lines)
```

---

### SPRINT 2 - FILE 2: UPDATE SMART TOOLS

```
=== SPRINT 2 - FILE 2: Update src/tools/smart_tools.py ===

Add Confluence distillation to smart tools.

Reference: @phase1_incremental_sprints.md lines 750-788

ADD this code to the existing SmartToolOrchestrator class:
- distill_confluence_key_points method
- get_confluence_key_points tool wrapper

DO NOT remove or modify existing Jira/GitHub methods.

After updating, show me:
- The new distill_confluence_key_points method
- The new tool wrapper
- Confirm: Jira + GitHub methods still intact
- New total tool wrappers: 4 (was 3, added 1)
```

---

### SPRINT 2 - FILE 3: UPDATE TOOL REGISTRY

```
=== SPRINT 2 - FILE 3: Update src/tools/tool_registry.py ===

Add Confluence tools to the registry.

Reference: @phase1_incremental_sprints.md lines 790-822

ADD these changes:
1. Import Confluence tools at top
2. Add 3 new tools to get_all_tools() list:
   - get_confluence_key_points (smart tool)
   - search_confluence_pages (raw tool)
   - get_confluence_page (raw tool)

After updating, show me:
- All imports (should now include Confluence)
- The complete get_all_tools() function
- Tool count: Should now be 14 (was 11, added 3)
- Logger should say: "Loaded 14 tools (Sprint 2: + Confluence)"
```

---

### SPRINT 2 - FILE 4: UPDATE KNOWLEDGE SERVICE

```
=== SPRINT 2 - FILE 4: Update src/services/knowledge_service.py ===

Add Confluence page indexing to knowledge service.

Reference: @phase1_incremental_sprints.md lines 824-853

ADD this method to the KnowledgeService class:
- index_confluence_pages method

DO NOT modify existing methods (index_existing_docs, get_style_examples).

After updating, show me:
- The new index_confluence_pages method
- Confirm: Original methods unchanged
- New total methods: 3 (was 2, added 1)
```

---

### SPRINT 2 - TESTING PROMPT

```
=== SPRINT 2 - TESTING ===

Create Sprint 2 tests.

Reference: @phase1_incremental_sprints.md lines 855-873

Create: tests/test_sprint2.py

Tests should verify:
- Confluence tools are now loaded (14 total tools)
- Sprint 1 still works (regression test)

Then run:
1. pytest tests/test_sprint1.py (should still pass - regression check)
2. pytest tests/test_sprint2.py (new tests)

Show me results.
```

---

### SPRINT 2 - COMPLETION VERIFICATION

```
=== SPRINT 2 - COMPLETION VERIFICATION ===

SUCCESS CRITERIA (from phase1_incremental_sprints.md lines 875-880):
✅ Sprint 1 still works: lyra create-release-notes v2.1 (no regressions)
✅ Confluence accessible: Agent can search Confluence pages
✅ Style consistency: Release notes can reference Confluence docs
✅ Tool count: 14 tools (was 11, added 3)

Run these verifications:

1. Regression check:
   pytest tests/test_sprint1.py
   Expected: PASS

2. Tool count:
   ```python
   from src.tools.tool_registry import get_all_tools
   print(len(get_all_tools()))
   ```
   Expected: 14

3. Confluence import:
   ```python
   from src.tools.confluence_tool import confluence_tool
   print("Confluence tool loaded")
   ```
   Expected: No errors

DECISION:
- All pass → Sprint 2 complete, ready for Sprint 3
- Any fail → Debug Sprint 2

Report results.
```

---

## Sprint 3: Complete Prompts

### SPRINT 3 - KICKOFF PROMPT

```
=== SPRINT 3: ADD AUDIT CAPABILITY ===

PREREQUISITE CHECK:
Sprints 1 AND 2 must be complete.

Verify:
- Sprint 1 tests pass: pytest tests/test_sprint1.py
- Sprint 2 tests pass: pytest tests/test_sprint2.py
- Tool count is 14

If any fail → Fix before Sprint 3.

SPRINT 3 GOAL:
Add documentation audit capability to find outdated docs.

SPRINT 3 SCOPE (from phase1_incremental_sprints.md, lines 884-965):

FILES TO ADD/MODIFY:
1. NEW: src/operations/doc_auditor.py
2. MODIFY: src/main.py (add audit command)

WHAT NOT TO TOUCH:
❌ Do NOT modify: Tools (already working)
❌ Do NOT modify: Agent core (already working)
❌ Do NOT add: Help docs, update, delete yet

EXPECTED OUTCOME:
After Sprint 3, this command should work:
`lyra audit ./docs --project=openshift`

And it should:
- Scan all markdown files in directory
- Extract API endpoints/features mentioned
- Check if they still exist in GitHub
- Generate audit report

Let's implement.

First: Create src/operations/doc_auditor.py

Confirm you understand Sprint 3 scope.
```

---

### SPRINT 3 - FILE 1: DOC AUDITOR

```
=== SPRINT 3 - FILE 1: src/operations/doc_auditor.py ===

Create document auditor for finding outdated docs.

Reference: @phase1_implementation_plan.md lines 4001-4185

Use EXACT content from those lines.

Includes (~185 lines):
- DocumentAuditor class
- audit_documentation method
- _audit_single_doc method
- _extract_mentioned_items method
- _verify_item_exists method (uses GitHub tool)
- _generate_audit_report method

IMPORTANT: This reuses the existing github_tool (check_file_exists method)

Create the file and show me:
- First 30 lines
- The _verify_item_exists method (shows GitHub integration)
- Total line count (should be ~185 lines)
```

---

### SPRINT 3 - FILE 2: UPDATE CLI

```
=== SPRINT 3 - FILE 2: Update src/main.py ===

Add audit command to CLI.

Reference: @phase1_implementation_plan.md lines 4362-4408

ADD to existing main.py:
1. Import doc_auditor at top
2. Add audit command (full implementation in reference)

DO NOT modify existing create_release_notes command.

After updating, show me:
- All imports (should now include doc_auditor)
- The new audit command
- Confirm: create_release_notes command unchanged
- New command count: 3 (create_release_notes, audit, version)
```

---

### SPRINT 3 - COMPLETION VERIFICATION

```
=== SPRINT 3 - COMPLETION VERIFICATION ===

SUCCESS CRITERIA (from phase1_incremental_sprints.md lines 959-964):
✅ New command works: lyra audit ./docs
✅ Finds outdated docs: Correctly identifies deprecated content
✅ Generates report: Creates audit report file
✅ Sprints 1+2 still work: No regressions

Run these verifications:

1. Regression check:
   pytest tests/test_sprint1.py && pytest tests/test_sprint2.py
   Expected: Both PASS

2. CLI commands:
   lyra --help
   Expected: Shows create-release-notes AND audit commands

3. Audit test (if you have test docs):
   lyra audit ./data/existing_docs --project=test
   Expected: Generates report in ./outputs/reports/

DECISION:
- All pass → Sprint 3 complete, ready for Sprint 4
- Any fail → Debug Sprint 3

Report results.
```

---

## Sprint 4: Complete Prompts

### SPRINT 4 - KICKOFF PROMPT

```
=== SPRINT 4: ADD HELP DOCUMENTATION ===

PREREQUISITE CHECK:
Sprints 1, 2, AND 3 must be complete.

Verify:
- All previous tests pass
- Commands work: create-release-notes, audit

SPRINT 4 GOAL:
Add ability to create help documentation (different doc type).

SPRINT 4 SCOPE (from phase1_incremental_sprints.md, lines 968-1104):

FILES TO ADD/MODIFY:
1. NEW: data/templates/help_doc.md
2. MODIFY: src/operations/doc_creator.py (add create_help_doc method)
3. MODIFY: src/main.py (add create-help-doc command)

WHAT NOT TO TOUCH:
❌ Do NOT modify: Tools (all working)
❌ Do NOT modify: Agent (all working)
❌ Do NOT add: Other doc types yet
❌ Do NOT add: Update, delete operations yet

EXPECTED OUTCOME:
After Sprint 4, this command should work:
`lyra create-help-doc "OAuth Authentication" --project=openshift`

This proves the system can generalize to different doc types.

Let's implement.

Confirm you understand Sprint 4 scope.
```

---

### SPRINT 4 - FILE 1: HELP DOC TEMPLATE

```
=== SPRINT 4 - FILE 1: data/templates/help_doc.md ===

Create help documentation template.

Reference: @phase1_incremental_sprints.md lines 980-1016 
(or @phase1_implementation_plan.md lines 4822-4901)

Use EXACT content.

This template structure is different from release notes.

Create the file and show me:
- The complete template
- Confirm it's different structure from release_notes.md
```

---

### SPRINT 4 - FILE 2: UPDATE DOC CREATOR

```
=== SPRINT 4 - FILE 2: Update src/operations/doc_creator.py ===

Add create_help_doc method to DocumentCreator class.

Reference: @phase1_incremental_sprints.md lines 1018-1056
(or full implementation at @phase1_implementation_plan.md lines 3668-3714)

ADD to existing DocumentCreator class:
- create_help_doc method

DO NOT modify: create_release_notes method (already working)

After updating, show me:
- The new create_help_doc method
- Confirm: create_release_notes unchanged
- Method count: 3 methods now (create_release_notes, create_help_doc, _save_draft)
```

---

### SPRINT 4 - FILE 3: UPDATE CLI

```
=== SPRINT 4 - FILE 3: Update src/main.py ===

Add create-help-doc command.

Reference: @phase1_incremental_sprints.md lines 1058-1096
(or @phase1_implementation_plan.md lines 4280-4318 for similar structure)

ADD to main.py:
- create_help_doc command

After updating, show me:
- The new command
- CLI command count: 4 (create_release_notes, create_help_doc, audit, version)
```

---

### SPRINT 4 - COMPLETION VERIFICATION

```
=== SPRINT 4 - COMPLETION VERIFICATION ===

SUCCESS CRITERIA (from phase1_incremental_sprints.md lines 1098-1103):
✅ Help docs work: Can create help documentation
✅ Different format: Help docs different from release notes
✅ Same agent: Uses same agent core (no agent changes)
✅ All previous sprints work: No regressions

Run these verifications:

1. Regression check:
   pytest tests/test_sprint1.py && pytest tests/test_sprint2.py
   Expected: PASS

2. New command:
   lyra --help
   Expected: Shows create-release-notes, create-help-doc, audit commands

3. Help doc creation (if you have credentials):
   lyra create-help-doc "Test Topic" --project=test
   Expected: Creates help doc (different format from release notes)

DECISION:
- All pass → Sprint 4 complete, ready for Sprint 5
- Any fail → Debug Sprint 4

Report results.
```

---

## Sprint 5: Complete Prompts

### SPRINT 5 - KICKOFF PROMPT

```
=== SPRINT 5: ADD REMAINING DATA SOURCES ===

PREREQUISITE CHECK:
Sprints 1-4 must ALL be complete and working.

Verify:
- All previous tests pass
- All commands work (create-release-notes, create-help-doc, audit)
- Tool count is currently 14

SPRINT 5 GOAL:
Add GitLab, Slack, and Google Docs as data sources for comprehensive data coverage.

SPRINT 5 STRATEGY:
We'll add these ONE AT A TIME to avoid integration hell:
- Day 1 Morning: GitLab
- Day 1 Afternoon: Slack
- Day 2: Google Docs

SPRINT 5 SCOPE (from phase1_incremental_sprints.md, lines 1107-1161):

FILES TO ADD:
1. NEW: src/tools/gitlab_tool.py
2. NEW: src/tools/slack_tool.py
3. NEW: src/tools/gdocs_tool.py
4. MODIFY: src/tools/tool_registry.py (add each tool incrementally)

WHAT NOT TO TOUCH:
❌ Do NOT modify: Jira, GitHub, Confluence tools (working)
❌ Do NOT modify: Agent, operations (working)

INCREMENTAL APPROACH:
Step 1: Add GitLab → Test → Verify no breaks
Step 2: Add Slack → Test → Verify no breaks
Step 3: Add Google Docs → Test → Verify no breaks

EXPECTED OUTCOME:
After Sprint 5:
- Tool count: 19 (adding 5 new tools)
- Agent can search all 6 data sources
- Release notes can include info from any source

Let's start with GitLab.

Confirm you understand Sprint 5 scope and incremental strategy.
```

---

### SPRINT 5 - STEP 1: GITLAB

```
=== SPRINT 5 - STEP 1A: Add GitLab Tool ===

Create GitLab tool.

Reference: @phase1_implementation_plan.md lines 1627-1770

Use EXACT content from those lines.

Includes (~144 lines):
- GitLabTool class
- search_merge_requests method
- LangChain tool wrapper

Create the file and show me:
- First 30 lines
- Total line count (should be ~144 lines)
```

```
=== SPRINT 5 - STEP 1B: Update Tool Registry for GitLab ===

Add GitLab to tool registry.

Reference: @phase1_incremental_sprints.md lines 1144-1154

ADD to src/tools/tool_registry.py:
1. Import: from src.tools.gitlab_tool import search_gitlab_merge_requests
2. Add to tools list: search_gitlab_merge_requests

After updating:
- Tool count should be: 15 (was 14, added 1)
- Logger should say: "Loaded 15 tools"

Test:
```python
from src.tools.tool_registry import get_all_tools
print(len(get_all_tools()))  # Should be 15
```

If test passes → Proceed to Slack
If test fails → Debug GitLab integration
```

---

### SPRINT 5 - STEP 2: SLACK

```
=== SPRINT 5 - STEP 2A: Add Slack Tool ===

Create Slack tool.

Reference: @phase1_implementation_plan.md lines 1772-1891

Use EXACT content from those lines.

Includes (~120 lines):
- SlackTool class (gracefully handles missing credentials)
- search_messages method
- LangChain tool wrapper

Create the file and show me:
- First 30 lines
- The search_messages method
- Total line count (should be ~120 lines)
```

```
=== SPRINT 5 - STEP 2B: Update Tool Registry for Slack ===

Add Slack to tool registry.

Reference: @phase1_incremental_sprints.md lines 1144-1154

ADD to src/tools/tool_registry.py:
1. Import: from src.tools.slack_tool import search_slack_messages
2. Add to tools list: search_slack_messages

After updating:
- Tool count should be: 16 (was 15, added 1)

Test:
```python
from src.tools.tool_registry import get_all_tools
print(len(get_all_tools()))  # Should be 16
```

If test passes → Proceed to Google Docs
If test fails → Debug Slack integration
```

---

### SPRINT 5 - STEP 3: GOOGLE DOCS

```
=== SPRINT 5 - STEP 3A: Add Google Docs Tool ===

Create Google Docs tool.

Reference: @phase1_implementation_plan.md lines 1893-2079

Use EXACT content from those lines.

Includes (~187 lines):
- GoogleDocsTool class (gracefully handles missing credentials)
- search_documents method
- get_document method
- _extract_text helper
- Two LangChain tool wrappers

Create the file and show me:
- First 30 lines
- The _extract_text method
- Total line count (should be ~187 lines)
```

```
=== SPRINT 5 - STEP 3B: Update Tool Registry for Google Docs ===

Add Google Docs to tool registry.

Reference: @phase1_incremental_sprints.md lines 1144-1154

ADD to src/tools/tool_registry.py:
1. Import: from src.tools.gdocs_tool import search_google_docs, get_google_doc
2. Add to tools list: search_google_docs, get_google_doc

After updating:
- Tool count should be: 18 (was 16, added 2)

Test:
```python
from src.tools.tool_registry import get_all_tools
print(len(get_all_tools()))  # Should be 18
```
```

---

### SPRINT 5 - COMPLETION VERIFICATION

```
=== SPRINT 5 - COMPLETION VERIFICATION ===

SUCCESS CRITERIA (from phase1_incremental_sprints.md lines 1156-1161):
✅ 3 new sources work: GitLab, Slack, Google Docs accessible
✅ Agent uses them: Can call these tools
✅ Not overwhelming: Agent still picks right tools (18 is manageable)
✅ All previous sprints work: No regressions

Run these verifications:

1. Complete tool count:
   ```python
   from src.tools.tool_registry import get_all_tools
   tools = get_all_tools()
   print(f"Total: {len(tools)}")  # Should be 18
   print("New tools:", [t.name for t in tools if 'gitlab' in t.name or 'slack' in t.name or 'google' in t.name])
   ```
   Expected: 18 tools total, shows gitlab, slack, google tools

2. Regression tests:
   pytest tests/
   Expected: All previous tests still pass

3. All commands still work:
   lyra --help
   Expected: create-release-notes, create-help-doc, audit all shown

DECISION:
- All pass → Sprint 5 complete, ready for Sprint 6
- Any fail → Debug Sprint 5

Report results.
```

---

## Sprint 6: Complete Prompts

### SPRINT 6 - KICKOFF PROMPT

```
=== SPRINT 6: COMPLETE CRUD OPERATIONS ===

PREREQUISITE CHECK:
Sprints 1-5 must ALL be complete.

Verify:
- All tests pass
- Tool count is 18
- All commands work (create-release-notes, create-help-doc, audit)

SPRINT 6 GOAL:
Add UPDATE and DELETE operations for complete documentation lifecycle management.

SPRINT 6 SCOPE (from phase1_incremental_sprints.md, lines 1165-1227):

FILES TO ADD/MODIFY:
1. NEW: src/operations/doc_updater.py
2. NEW: src/operations/doc_deleter.py
3. MODIFY: src/main.py (add update and delete commands)

WHAT NOT TO TOUCH:
❌ Do NOT modify: Tools (all 18 working perfectly)
❌ Do NOT modify: Agent (working perfectly)
❌ Do NOT modify: doc_creator, doc_auditor (working)

EXPECTED OUTCOME:
After Sprint 6, these commands should work:
- `lyra update ./docs/file.md --project=openshift`
- `lyra delete ./docs/old.md --project=openshift --reason="Deprecated"`

Full CRUD complete: Create, Read (audit), Update, Delete

Let's implement.

Confirm you understand Sprint 6 scope.
```

---

### SPRINT 6 - FILE 1: DOC UPDATER

```
=== SPRINT 6 - FILE 1: src/operations/doc_updater.py ===

Create document updater for modifying existing docs.

Reference: @phase1_implementation_plan.md lines 3779-3902

Use EXACT content from those lines.

Includes (~124 lines):
- DocumentUpdater class
- update_document method
- _read_existing_doc method
- _infer_doc_type method
- _save_updated_doc method (creates backup)

Create the file and show me:
- First 30 lines
- The _save_updated_doc method (shows backup creation)
- Total line count (should be ~124 lines)
```

---

### SPRINT 6 - FILE 2: DOC DELETER

```
=== SPRINT 6 - FILE 2: src/operations/doc_deleter.py ===

Create document deleter for deprecating/removing docs.

Reference: @phase1_implementation_plan.md lines 3904-3999

Use EXACT content from those lines.

Includes (~96 lines):
- DocumentDeleter class
- delete_document method
- _hard_delete method (archives before deleting)
- _add_deprecation_notice method

Create the file and show me:
- The delete_document method
- The _add_deprecation_notice method
- Total line count (should be ~96 lines)
```

---

### SPRINT 6 - FILE 3: UPDATE CLI (FINAL)

```
=== SPRINT 6 - FILE 3: Update src/main.py (Final Updates) ===

Add update and delete commands to complete CLI.

Reference: @phase1_implementation_plan.md lines 4282-4359 (update command)
Reference: @phase1_implementation_plan.md lines 4320-4359 (delete command)

ADD to src/main.py:
1. Imports: doc_updater, doc_deleter
2. update command (full implementation in reference)
3. delete command (full implementation in reference)

After updating, show me:
- All imports (should have: doc_creator, doc_updater, doc_deleter, doc_auditor)
- All commands
- Final command count: 6 (create-release-notes, create-help-doc, update, delete, audit, version)

This is the FINAL CLI - no more commands after this.
```

---

### SPRINT 6 - COMPLETION VERIFICATION (FINAL)

```
=== SPRINT 6 - COMPLETION VERIFICATION (PHASE 1 COMPLETE!) ===

This is the FINAL sprint verification. If this passes, Phase 1 is complete!

SUCCESS CRITERIA (from phase1_incremental_sprints.md lines 1221-1226):
✅ Update works: Can update existing docs
✅ Delete works: Can deprecate or remove docs
✅ Full CRUD: Create, Read (audit), Update, Delete all work
✅ All sprints work: Complete system with no regressions

COMPLETE VERIFICATION:

1. All Previous Tests:
   pytest tests/
   Expected: ALL PASS

2. Tool Count (Final):
   ```python
   from src.tools.tool_registry import get_all_tools
   print(f"Total tools: {len(get_all_tools())}")
   ```
   Expected: 18 tools

3. All Commands Available:
   lyra --help
   Expected output should show:
   - create-release-notes
   - create-help-doc  
   - update
   - delete
   - audit
   - version

4. Test Each Command Type:
   a) Create: lyra create-release-notes v2.1 --project=test
   b) Audit: lyra audit ./data/existing_docs --project=test
   c) Update: (create a test file first, then update it)
   d) Delete: (create a test file first, then delete it)

5. FINAL FILE COUNT:
   Count all files in src/
   Expected: ~30+ Python files

6. PHASE 1 COMPLETE CHECKLIST (from phase1_implementation_plan.md lines 5292-5300):
   ✅ Can generate release notes for any version
   ✅ Can create help docs for any topic
   ✅ Can update existing docs accurately
   ✅ Can audit and identify outdated docs
   ✅ Agent explores multiple sources autonomously
   ✅ Citations are accurate and traceable
   ✅ Handles one project completely

FINAL DECISION:
If ALL verifications pass → PHASE 1 COMPLETE! 🎉
If ANY fail → Debug before declaring complete

Report complete verification results.
```

---

## Emergency Recovery Prompts

### If AI Goes Off Track During ANY Sprint

```
STOP. RESET CONTEXT.

We are implementing Lyra Phase 1 using incremental sprints.

CHECK THESE TWO DOCUMENTS:
@phase1_implementation_plan.md - Complete reference (5650 lines)
@phase1_incremental_sprints.md - Sprint order (1312 lines)

CURRENT STATUS - FILL THIS IN:
Current Sprint: [1/2/3/4/5/6]
Sprint Goal: [state the goal]

Completed Sprints:
[X] Sprint 1: Release notes - COMPLETE
[X] Sprint 2: Confluence - COMPLETE  
[ ] Sprint 3: Not started
[ ] Sprint 4: Not started
[ ] Sprint 5: Not started
[ ] Sprint 6: Not started

Files completed THIS sprint:
[List files you've created so far]

SCOPE CONSTRAINT:
What we SHOULD be doing:
[Paste scope from current sprint section of phase1_incremental_sprints.md]

What we should NOT be doing:
- Anything from future sprints
- Any "improvements" not in the plan
- Any new features not in current sprint scope

Please confirm you understand where we are and what we're working on.
```

---

### If Implementation Doesn't Match Reference

```
STOP. CODE MISMATCH DETECTED.

File: [file_path]

Expected implementation from @phase1_implementation_plan.md lines [X]-[Y]:

[Paste the EXACT code from reference that should be there]

What you created instead:

[Paste what AI generated]

Differences I see:
1. [List specific difference]
2. [List specific difference]

INSTRUCTION:
Regenerate this file to match the reference EXACTLY.
Use @phase1_implementation_plan.md lines [X]-[Y].
Copy character-for-character.

Do not proceed to next file until this matches.
```

---

### If AI Suggests Adding Features Not in Sprint

```
FEATURE SCOPE CHECK.

You suggested: [what AI suggested]

Let me check if this is in current sprint scope.

Current Sprint: [number]
Sprint Scope from @phase1_incremental_sprints.md lines [X]-[Y]:

[Paste exact scope section]

Is your suggestion in this scope?
- If YES → Proceed (show me where in the scope it's mentioned)
- If NO → This is for a later sprint or not in plan at all

RULE: Only implement what current sprint explicitly specifies.

Please confirm: Is this feature in current sprint scope or not?
```

---

## Progress Tracking Template

**Update this after each file and paste at start of each conversation**:

```
=== LYRA IMPLEMENTATION PROGRESS ===

Reference: @phase1_implementation_plan.md (5650 lines)
Sprint Guide: @phase1_incremental_sprints.md (1312 lines)

OVERALL PROGRESS:
✅ Sprint 1: COMPLETE (Release notes working)
✅ Sprint 2: COMPLETE (Confluence added)
✅ Sprint 3: COMPLETE (Audit working)
⏳ Sprint 4: IN PROGRESS
⬜ Sprint 5: Not started
⬜ Sprint 6: Not started

CURRENT SPRINT: 4
Sprint 4 Goal: Add help documentation capability

SPRINT 4 FILES:
✅ data/templates/help_doc.md (DONE)
✅ src/operations/doc_creator.py - added create_help_doc (DONE)
⏳ src/main.py - adding create-help-doc command (IN PROGRESS)

NEXT ACTION:
Complete src/main.py update with create-help-doc command

CONSTRAINTS FOR THIS SESSION:
1. Only work on Sprint 4 files
2. Do NOT modify Sprint 1-3 files (already working)
3. Do NOT jump ahead to Sprint 5
4. Use exact code from reference lines specified

Ready to continue with: src/main.py update for create-help-doc command

Confirm you understand current state before proceeding.

=== END PROGRESS ===
```

**Update the checkmarks [✅⏳⬜] and file lists after each file.**

---

## Quick Command Reference

### Verification Commands to Run After Each Sprint

**After Sprint 1**:
```bash
# Test basic structure
pytest tests/test_sprint1.py

# Test CLI
lyra --help

# Check tool count
python -c "from src.tools.tool_registry import get_all_tools; print(len(get_all_tools()))"
# Expected: 11
```

**After Sprint 2**:
```bash
pytest tests/test_sprint1.py tests/test_sprint2.py
python -c "from src.tools.tool_registry import get_all_tools; print(len(get_all_tools()))"
# Expected: 14
```

**After Sprint 3**:
```bash
pytest tests/
lyra --help  # Should show: create-release-notes, create-help-doc, audit
```

**After Sprint 4**:
```bash
pytest tests/
lyra --help  # Should show: create-release-notes, create-help-doc, audit
```

**After Sprint 5**:
```bash
python -c "from src.tools.tool_registry import get_all_tools; print(len(get_all_tools()))"
# Expected: 18
```

**After Sprint 6 (FINAL)**:
```bash
pytest tests/
lyra --help  # Should show all 6 commands
python -c "from src.tools.tool_registry import get_all_tools; print(len(get_all_tools()))"
# Expected: 18

# Test all operations:
lyra create-release-notes v1.0 --project=test
lyra create-help-doc "Test" --project=test
lyra audit ./data/existing_docs --project=test
```

---

## How to Use These Prompts

### Day-by-Day Implementation Guide

**Day 1 (Sprint 1 Start)**:
1. Copy "SPRINT 1 - KICKOFF PROMPT" → Paste to AI
2. Wait for AI confirmation
3. Copy "SPRINT 1 - FILE 1: SCAFFOLDING" → Paste to AI
4. Verify output
5. Copy "SPRINT 1 - FILE 2: ENVIRONMENT" → Paste to AI
6. Continue file-by-file through Sprint 1

**Day 2 (Sprint 1 Complete)**:
1. Copy "SPRINT 1 - COMPLETION VERIFICATION" → Paste to AI
2. Run all verification commands
3. If pass → Sprint 1 DONE ✅
4. Update progress template

**Day 3 (Sprint 2)**:
1. Copy "SPRINT 2 - KICKOFF PROMPT" → Paste to AI
2. Continue file-by-file
3. Verify completion

**Continue through Sprint 6...**

---

## The Complete System

### What You Have

1. **phase1_implementation_plan.md**: All the code (5650 lines)
2. **phase1_incremental_sprints.md**: When to build what (1312 lines)
3. **THIS DOCUMENT**: Exact prompts to copy-paste (no thinking required)

### How to Succeed

1. **Don't deviate**: Use prompts exactly as written
2. **Verify after each file**: Use the "show me" checks in each prompt
3. **Run tests after each sprint**: Use completion verification prompts
4. **Update progress template**: Keep AI aligned across sessions
5. **If stuck**: Use emergency recovery prompts

### Expected Timeline

- **Sprint 1**: 2 days (most files, proves architecture)
- **Sprint 2**: 1 day (add 1 source)
- **Sprint 3**: 1 day (add 1 operation)
- **Sprint 4**: 1 day (add 1 doc type)
- **Sprint 5**: 1-2 days (add 3 sources incrementally)
- **Sprint 6**: 1 day (add 2 operations)

**Total**: 7-9 days to complete Phase 1

---

**You now have COMPLETE, COPY-PASTE READY prompts for the entire implementation. Just follow sprint by sprint, use the prompts exactly, and verify after each step.** 🎯

**Start with Sprint 1 Kickoff Prompt above!**
