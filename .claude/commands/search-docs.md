---
description: Search Open Systems documentation using semantic RAG (compact output for agents)
---

Search the Open Systems documentation for: {{PROMPT}}

Use the script at `scripts/search_compact.py` to perform a hybrid semantic search.

**Instructions:**
1. Run: `python scripts/search_compact.py "{{PROMPT}}"`
2. Return ONLY the search results (no extra commentary)
3. Results are already formatted compactly for minimal context usage
4. If the user needs more details from a specific result, use the Read tool on the source file

**Important:** This is designed for efficient agent usage. Keep output minimal.
